#!/usr/bin/env python
"""
Скрипт для тестирования отправки email
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_sending():
    """Тестирует отправку email"""
    
    # Проверяем настройки
    print("=== Настройки Email ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Не настроен')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Не настроен')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Не настроен')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Не настроен')}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Тестовые данные
    test_email = input("Введите email для тестирования: ")
    
    try:
        # Отправляем тестовое письмо
        print(f"Отправляем тестовое письмо на {test_email}...")
        
        send_mail(
            subject='🎮 Тест отправки email - MMORPG',
            message=f"""
Здравствуйте!

Это тестовое письмо для проверки настройки SMTP в проекте MMORPG.

Если вы получили это письмо, значит настройка SMTP работает корректно!

С уважением,
Команда MMORPG
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Тестовое письмо отправлено успешно!")
        print("Проверьте вашу почту (включая папку 'Спам')")
        
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        print("\nВозможные причины:")
        print("1. Неправильный email или пароль приложения")
        print("2. Двухфакторная аутентификация не включена")
        print("3. Пароль приложения не создан")
        print("4. Блокировка со стороны Gmail")

if __name__ == '__main__':
    test_email_sending() 