#!/usr/bin/env python3
"""
Простой тест для проверки отправки email
"""
import os
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Тестируем отправку email"""
    try:
        print("🔍 Тестируем отправку email...")
        print(f"📧 EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"📧 EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"📧 EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"📧 DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        # Отправляем тестовое письмо
        send_mail(
            subject='Тест отправки email - MMORPG Backend',
            message='Это тестовое письмо для проверки настроек email.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Отправляем себе
            fail_silently=False,
        )
        
        print("✅ Email успешно отправлен!")
        
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        print(f"🔍 Тип ошибки: {type(e).__name__}")

if __name__ == '__main__':
    test_email() 