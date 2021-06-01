"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from rest_framework_simplejwt import views as jwt_views
from Physiotherapist import views
from django.conf.urls import  handler500,handler404



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_physio/', views.Reg_physio),
   
   # path('api/login/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('api/login/',views.login),
    path('api/logout/',views.logout),
    path('api/update_profile/',views.update_profile),
    path('api/profile',views.profile),
    path('api/validate_email/',views.validate_email),
    path('api/validate_mobile/',views.validate_mobile),
    path('api/email-varification/',views.otp_varification),
    path('api/send/',views.mail),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
   
  
]
handler500 = 'Physiotherapist.views.error_500'
handler404 = 'Physiotherapist.views.error_404'
