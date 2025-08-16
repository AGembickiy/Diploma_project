from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class User(AbstractUser):
    """Кастомная модель пользователя"""
    
    # Дополнительные поля
    email = models.EmailField(unique=True, verbose_name='Email')
    email_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
    verification_token = models.UUIDField(default=uuid.uuid4, verbose_name='Токен подтверждения')
    verification_token_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания токена')
    
    # Переопределяем username как необязательное поле
    username = models.CharField(max_length=150, unique=True, null=True, blank=True, verbose_name='Имя пользователя')
    
    # Используем email для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username or self.email
    
    def get_short_name(self):
        return self.username or self.email.split('@')[0]


class EmailVerification(models.Model):
    """Модель для хранения токенов подтверждения email"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    token = models.UUIDField(default=uuid.uuid4, verbose_name='Токен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expires_at = models.DateTimeField(verbose_name='Дата истечения')
    is_used = models.BooleanField(default=False, verbose_name='Использован')
    
    class Meta:
        verbose_name = 'Подтверждение email'
        verbose_name_plural = 'Подтверждения email'
    
    def __str__(self):
        return f"Подтверждение для {self.user.email}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
