from django.db import models
from Auth.models import User,UserManager
from phone_field import PhoneField
from Auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class pp_physiotherapist_master(models.Model):
    pp_pm_id          = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name        = models.CharField( max_length=50)
    middle_name       = models.CharField( max_length=50,blank=True)
    last_name         = models.CharField( max_length=50) 
    Doctor_type       = models.IntegerField()
    Address_1         = models.CharField( max_length=150)
    Address_2         = models.CharField( max_length=150,blank=True)
    Address_3         = models.CharField( max_length=150,blank=True)
    city              = models.CharField( max_length=50)
    state             = models.CharField( max_length=50)
    country           = models.CharField( max_length=50)
    mobile_no         = models.CharField( max_length=15)
    whatsapp_no       = models.CharField( max_length=12)
    landline          = models.CharField( max_length=12)
    facebook          = models.CharField( max_length=50, blank=True, null=True, default=None)
    linkedin          = models.CharField( max_length=50, blank=True, null=True, default=None)
    regd_no_1         = models.CharField(max_length=50,unique = True)
    regd_no_2         = models.CharField(max_length=50,unique=True, blank=True, null=True, default=None)
    degree            = models.CharField( max_length=12)
    expertise_1       = models.CharField( max_length=50) 
    expertise_2       = models.CharField( max_length=50,blank=True) 
    expertise_3       = models.CharField( max_length=50,blank=True)
    start_date        = models.DateTimeField(auto_now=False, auto_now_add=False) 
    end_date          = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True)
    status_flag       = models.IntegerField()
    roleId            = models.IntegerField()
  
  
    class Meta:
        db_table='pp_physiotherapist_master'

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender,instance,created, **kwargs):
    #     if created:
    #         pp_physiotherapist_master.objects.create(pp_pm_id=instance)
        
    
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender,instance, **kwargs):
    #     instance.pp_physiotherapist_master.save()
        
            
        
    
            

    
    
    

