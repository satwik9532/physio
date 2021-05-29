from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
# Create your models here.
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("User must have email")

        user =self.model(
            email=self.normalize_email(email),
            **extra_fields

        )   


        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):


        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff-true')


        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser-true')


        return self.create_user(email, password,**extra_fields)


class User(AbstractUser):

    username            = None
    email               = models.EmailField(("email_address"), unique = True) 
    first_name          =None
    last_name           =None
    
    
    USERNAME_FIELD   = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    

 