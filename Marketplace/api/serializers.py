from rest_framework import serializers
from . import models
from app import models as appModel



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
        

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    username = serializers.CharField(read_only=True)

    class Meta:
        model = appModel.CustomUser
        fields = ['first_name', 'last_name', 'email', 'user_type', 'mobile_number', 'password', 'username']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('first_name')+ validated_data.get('last_name')
        validated_data['username'] = username
        user = appModel.CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OtpGenerationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15) 