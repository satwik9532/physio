from django.contrib import admin
from Auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from Auth.forms import CustomUserCreationsForm,CustomuserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationsForm
    form = CustomuserChangeForm
    model = User
    list_display = ['email','is_staff','is_active']
    list_filter = ['email','is_staff','is_active']

    fieldsets = (
     (None,{
         'fields':('email','password')}),
        ('permissions',{'fields':('is_staff','is_active')}),
    )

    add_fieldsets = (
     (None,{
         'fields':('wide',),
         'fields':('email','password1','password2','is_staff','is_active')
     }),
    )
    

    search_fields = ('email',)
    ordering = ('email',)


    



admin.site.register(User,CustomUserAdmin)
