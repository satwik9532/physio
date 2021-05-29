from Auth.models import User
from rest_framework import serializers
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,write_only=True,required=True)

    

    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)    

    def validate_password(self,value):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        if not re.search(reg, value):
            raise serializers.ValidationError("please enter strong password")
        return value    