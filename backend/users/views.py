from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    EmailVerificationSerializer,
    UserSerializer
)
from .models import User


# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация пользователя"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        return Response({
            'message': 'Регистрация успешна! Проверьте email для подтверждения аккаунта.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Вход пользователя"""
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Создаем или получаем токен
        token, created = Token.objects.get_or_create(user=user)
        
        # Логиним пользователя
        login(request, user)
        
        return Response({
            'message': 'Вход выполнен успешно!',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Подтверждение email"""
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Создаем токен для автоматического входа
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Email подтвержден! Аккаунт активирован.',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_profile(request):
    """Получение профиля пользователя"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def logout(request):
    """Выход пользователя"""
    try:
        # Удаляем токен
        request.user.auth_token.delete()
    except:
        pass
    
    return Response({'message': 'Выход выполнен успешно!'}, status=status.HTTP_200_OK)
