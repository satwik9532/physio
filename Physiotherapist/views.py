from django.shortcuts import render
from Physiotherapist.models import pp_physiotherapist_master,pp_otp
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,schema
from Physiotherapist.serializers import pp_physiotherapist_masterSerializer,pp_otpSerializer,mobileSerilizer
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from Auth.models import User
from Auth.serializer import UserSerializer ,emaiSerializer

from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
import jwt , datetime
from django.core.mail import send_mail
from rest_framework.schemas import AutoSchema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema








token_param_config = openapi.Parameter(None,in_ = openapi.IN_QUERY,description = 'Description',type = openapi.TYPE_STRING)
user_response = openapi.Response('response description', {'message':'created'})
@csrf_exempt
@swagger_auto_schema(methods=['post'],request_body=pp_physiotherapist_masterSerializer)
@api_view(['POST'])
def Reg_physio(request):
  
    user_data = request.data['user']
    profile_data = request.data['profile']

    email = user_data['email']
    password = generate_password()
    user_data['password'] = password

    user = UserSerializer(data=user_data)

    if not user.is_valid():
        return Response(user.errors)
    user=user.save()
    profile_data['pp_pm_id'] = user.id
    serializer = pp_physiotherapist_masterSerializer(data=profile_data)


    if not serializer.is_valid():
        data = User.objects.filter(email=user.email)
        data.delete()
        return Response(serializer.errors)

    serializer.save()
    try:
        otp = otpgen()
        otp_data = {}
        otp_data['otp'] = otp
        otp_data['email'] = user_data['email']
        otpserializer = pp_otpSerializer(data = otp_data)
        if otpserializer.is_valid():
            otpserializer.save()
        else:
            print(otpserializer.errors)    
        send_mail('email varification',
        'your password is '+password,'mishra.satwik9532@gmail.com',[user_data['email']],fail_silently=False)
        
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)

 
   
    
    response = Response(status=status.HTTP_201_CREATED)   
  #  response.set_cookie(key='jwt',value=token,expires=datetime.datetime.utcnow()+datetime.timedelta(days=1),httponly=True)

    response.data={
        'message':'user created',
        'role':'physio'
    }
    return response  

    
   
    




@csrf_exempt
@api_view(['GET'])
def get_physio(request,id):
   
    
    try:
        data = pp_physiotherapist_master.objects.get(regd_no_1=id)
        serializer = pp_physiotherapist_masterSerializer(data)
        request.session['uid'] = serializer.data
        return Response(serializer.data)


    except pp_physiotherapist_master.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



@csrf_exempt
@api_view(['GET'])

def profile(request):
    token = request.COOKIES.get('jwt')
    #sess = request.session['id']
   

    if not token:
       raise exceptions.AuthenticationFailed('unauthenticated')

    try:
        payload = jwt.decode(token,'secret_key',algorithms=['HS256'])  

    except jwt.ExpiredSignatureError:
       raise exceptions.AuthenticationFailed('unauthenticated')

    user = pp_physiotherapist_master.objects.filter(pp_pm_id=payload['id']).first()   
    serializer = pp_physiotherapist_masterSerializer(user)
    return Response(serializer.data) 











token_param_config = openapi.Parameter('first_name',in_ = openapi.IN_QUERY,description = 'Description',type = openapi.TYPE_STRING)
user_response = openapi.Response('response description', {'message':'created'})
@csrf_exempt
@swagger_auto_schema(manual_parameters = [token_param_config],methods=['post'],request_body=UserSerializer)
@api_view(['POST'])
def login(request):

    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect password') 

    payload = {
        'id':user.id,
        
        
    }   

    token =  jwt.encode(payload,'secret_key',algorithm='HS256')
   
   # print(token)
    response = Response()   
    response.set_cookie(key='jwt',value=token,expires=datetime.datetime.utcnow()+datetime.timedelta(days=1),httponly=True)
    request.session['id']=user.id
    request.session.set_expiry(86400)

    response.data={
        'jwt':token
    }
    return response     





@csrf_exempt
@api_view(['POST'])
def logout(request):

    if not request.COOKIES.get('jwt'):
       raise exceptions.AuthenticationFailed('login required')

    response = Response()
    
    request.session.flush()
    request.session.clear_expired()
    response.delete_cookie('jwt')

    return response



@csrf_exempt
@api_view(['PUT'])
def update_profile(request):

    if not request.COOKIES.get('jwt'):
        raise exceptions.AuthenticationFailed('unauthenticated')
    token = request.COOKIES.get('jwt')
    try:
        payload = jwt.decode(token,'secret_key',algorithms=['HS256'])  

    except jwt.ExpiredSignatureError:
       raise exceptions.AuthenticationFailed('unauthenticated')

    data = pp_physiotherapist_master.objects.filter(pp_pm_id=payload['id']).first() 
    serializer = pp_physiotherapist_masterSerializer(data,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'data updated'},status=status.HTTP_200_OK)  

    return Response(serializer.errors)     






token_config = openapi.Parameter(None,in_ = openapi.IN_QUERY,description = 'Description',type = openapi.TYPE_STRING)
user_response = openapi.Response('response description', {'message':'created'})
@csrf_exempt
@swagger_auto_schema(manual_parameters = [token_param_config],methods=['post'],request_body=emaiSerializer)
@api_view(['POST'])
def validate_email(request):

    try:

        if User.objects.filter(email = request.data['email']).exists():
            return Response({'message':'email already exists'},status = status.HTTP_409_CONFLICT)

        else:
            return Response(status = status.HTTP_200_OK)     
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)            




        
@csrf_exempt
@swagger_auto_schema(methods=['post'],request_body=mobileSerilizer)
@api_view(['POST'])
def validate_mobile(request):

    try:
        if pp_physiotherapist_master.objects.filter(mobile_no = request.data['mobile_no']).exists():
            return Response({'message':'mobile number already exists'},status = status.HTTP_409_CONFLICT)

        else:
            return Response(status = status.HTTP_200_OK)    
    except:
        return Response(status = status.HTTP_400_BAD_REQUEST)            



        
import random as r
# function for otp generation
def otpgen():
    otp=""
    for i in range(4):
        otp+=str(r.randint(1,9))
    return otp





token_param_config_ = openapi.Parameter('email',in_ = openapi.IN_QUERY,description = 'Description',type = openapi.TYPE_STRING)   
@csrf_exempt
@swagger_auto_schema(manual_parameters = [token_param_config_],methods=['post'],request_body=pp_otpSerializer)
@api_view(['POST'])
def mail(request):
       otp = otpgen()
       send_mail('hello , just for testing',
       'your otp is'+str(otp),'mishra.satwik9532@gmail.com',[request.data['email']],fail_silently=False)
       return Response(status = status.HTTP_200_OK)




@csrf_exempt
@api_view(['POST'])
def otp_varification(request):
    
    if pp_otp.objects.filter(email = request.data['email']).exists():
        data = pp_otp.objects.filter(email = request.data['email']).first()
        serializer = pp_otpSerializer(data)
        print(serializer.data)
        if serializer.data['otp'] == request.data['otp']:
            data.delete()
            return Response({'message':'email varified'},status = status.HTTP_200_OK)
        else:     
            return Response({'msg':'wrong OTP'},status = status.HTTP_200_OK)
    return Response({'msg':'error'},status = status.HTTP_400_BAD_REQUEST)    


from django.http import JsonResponse
@csrf_exempt
def error_500(request):
    return JsonResponse({"message": "internal server error"}, status=500)

@csrf_exempt    
def error_404(request, exception):
    return JsonResponse({"message": "invalide API"}, status=404)



import array
def generate_password():
    MAX_LEN = 12
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']                 
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    rand_digit = r.choice(DIGITS)
    rand_upper = r.choice(UPCASE_CHARACTERS)
    rand_lower = r.choice(LOCASE_CHARACTERS)
    rand_symbol = r.choice(SYMBOLS)      
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol  
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + r.choice(COMBINED_LIST)
 
    # convert temporary password into array and shuffle to
    # prevent it from having a consistent pattern
    # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        r.shuffle(temp_pass_list)
    password = ""
    for x in temp_pass_list:
        password = password + x        

    return password                



@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    pass



