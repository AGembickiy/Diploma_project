from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, EmailVerification
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .services import EmailService


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True}
        }
    
    def validate_email(self, value):
        """Проверяем, что email уникален"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
    
    def validate_password(self, value):
        """Валидируем пароль"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, attrs):
        """Проверяем совпадение паролей"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs
    
    def create(self, validated_data):
        """Создаем пользователя и отправляем email для подтверждения"""
        validated_data.pop('password_confirm')
        
        # Генерируем уникальный username
        base_username = validated_data.get('username') or validated_data['email'].split('@')[0]
        username = base_username
        counter = 1
        
        # Проверяем уникальность username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        # Создаем пользователя как неактивного
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Пользователь неактивен до подтверждения email
        )
        
        # Создаем токен для подтверждения email
        expires_at = timezone.now() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
        verification = EmailVerification.objects.create(
            user=user,
            expires_at=expires_at
        )
        
        # Отправляем email с токеном подтверждения
        EmailService.send_verification_email(user, verification)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя"""
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        """Проверяем учетные данные"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Используем email как username для аутентификации
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Неверный email или пароль.")
            if not user.is_active:
                raise serializers.ValidationError("Аккаунт не активирован. Проверьте email для подтверждения.")
            if not user.email_verified:
                raise serializers.ValidationError("Email не подтвержден. Проверьте email для подтверждения.")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Необходимо указать email и пароль.")
        
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    """Сериализатор для подтверждения email"""
    
    token = serializers.UUIDField()
    
    def validate_token(self, value):
        """Проверяем токен"""
        try:
            verification = EmailVerification.objects.get(token=value, is_used=False)
            if verification.is_expired():
                raise serializers.ValidationError("Токен истек.")
            self.verification = verification
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Неверный токен подтверждения.")
        return value
    
    def save(self):
        """Активируем пользователя"""
        verification = self.verification
        user = verification.user
        
        user.is_active = True
        user.email_verified = True
        user.save()
        
        verification.is_used = True
        verification.save()
        
        # Отправляем приветственное письмо
        EmailService.send_welcome_email(user)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения пользователя"""
    
    # Добавляем вычисляемое поле для отображения логина
    login_display = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email_verified', 'date_joined', 'login_display']
        read_only_fields = ['id', 'email_verified', 'date_joined']
    
    def get_login_display(self, obj):
        """Возвращаем email как логин для отображения"""
        return obj.email 