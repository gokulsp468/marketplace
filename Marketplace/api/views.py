from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .decorators import validate_required_fields
from . import serializers, models
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer


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