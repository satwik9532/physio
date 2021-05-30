from django.shortcuts import render
from Physiotherapist.models import pp_physiotherapist_master
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from Physiotherapist.serializers import pp_physiotherapist_masterSerializer
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from Auth.models import User
from Auth.serializer import UserSerializer
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
import jwt , datetime




@csrf_exempt
@api_view(['POST'])
def Reg_physio(request):
  
    user_data = request.data['user']
    profile_data = request.data['profile']

    email = user_data['email']
    password = user_data['password']

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


    payload = {
        'id':user.id,
        }   

    token =  jwt.encode(payload,'secret_key',algorithm='HS256')
   
    
    response = Response(status=status.HTTP_201_CREATED)   
    response.set_cookie(key='jwt',value=token,expires=datetime.datetime.utcnow()+datetime.timedelta(days=1),httponly=True)

    response.data={
        'jwt':token
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











@csrf_exempt
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



        






   
   









    
