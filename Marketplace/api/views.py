from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .decorators import validate_required_fields
from . import serializers, models
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from twilio.rest import Client
from app import models as appmodel
from drf_yasg import openapi
import os



@swagger_auto_schema(method='post', request_body=CustomUserSerializer)
@api_view(['POST'])
def SignUpView(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='post', request_body=serializers.MessageSerializer)
@api_view(['POST'])
@validate_required_fields(["name", "age"])
@permission_classes([IsAuthenticated])
def message_create_view(request):
   
    if request.method == 'POST':
        serializer = serializers.MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            success_message = "created successfully."
            return Response({'message': success_message, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_list_view(request):
    if request.method == 'GET':
        queryset = models.Message.objects.all()
        serializer = serializers.MessageSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
@swagger_auto_schema(method='post', request_body=serializers.OtpGenerationSerializer)
@api_view(['POST'])

def generate_otp_view(request):
    serializer = serializers.OtpGenerationSerializer(data=request.data)
    if serializer.is_valid():
        TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
        TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
        TWILIO_VERIFY_SID = os.environ.get('TWILIO_VERIFY_SID')

        verified_number = serializer.validated_data['phone_number']

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        try:
            user = appmodel.CustomUser.objects.filter(mobile_number=verified_number).first()
            if not user:
                return Response({'status': 'mobile number does not match with any user'}, status=404)
            verification = client.verify.v2.services(TWILIO_VERIFY_SID).verifications.create(to=verified_number, channel="sms")
            if verification.status == 'pending':
                return Response({'status': 'success'})
            else:
                return Response({'status': 'failure'})
        except Exception as e:
            # Log the exception
            return Response({'status': 'failure', 'message': str(e)}, status=500)
    else:
        return Response(serializer.errors, status=400)
    

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['phone_number', 'otp'],
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
        'otp': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['POST'])
def verify_otp_view(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    
    # Ensure phone_number and otp are present
    if not phone_number or not otp:
        return Response({'status': 'phone_number and otp are required'}, status=400)
    
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_VERIFY_SID = os.environ.get('TWILIO_VERIFY_SID')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        user = appmodel.CustomUser.objects.filter(mobile_number=phone_number).first()
        if not user:
            return Response({'status': 'mobile number does not match with any user'}, status=404)
        
        verification_check = client.verify \
            .services(TWILIO_VERIFY_SID) \
            .verification_checks \
            .create(to=phone_number, code=otp)
        
        if verification_check.status == 'approved':
            user.is_active = True
            user.save()
            return Response({'status': 'verified successfully'}, status=200)
        else:
            return Response({'status': 'OTP verification failed'}, status=400)
    except Exception as e:
        return Response({'status': 'failure', 'message': str(e)}, status=500)