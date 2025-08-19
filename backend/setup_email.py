#!/usr/bin/env python
"""
Скрипт для безопасной настройки email пароля
"""
import os
import sys
import getpass
import re

def update_settings_with_password():
    """Обновляет settings.py с паролем приложения"""
    
    print("🔧 Настройка Gmail SMTP для отправки email")
    print("=" * 50)
    
    # Проверяем, что файл settings.py существует
    settings_file = 'mmorpg_backend/settings.py'
    if not os.path.exists(settings_file):
        print(f"❌ Файл {settings_file} не найден!")
        return
    
    # Запрашиваем пароль приложения
    print("\n📧 Введите пароль приложения Gmail:")
    print("(Пароль будет скрыт при вводе)")
    app_password = getpass.getpass("Пароль приложения: ")
    
    if not app_password:
        print("❌ Пароль не может быть пустым!")
        return
    
    if len(app_password) != 16:
        print("⚠️  Внимание: Пароль приложения Gmail должен содержать 16 символов")
        print("Убедитесь, что вы ввели правильный пароль приложения, а не обычный пароль Gmail")
        
        confirm = input("Продолжить? (y/n): ").lower()
        if confirm != 'y':
            return
    
    # Читаем файл settings.py
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return
    
    # Заменяем placeholder на реальный пароль
    old_pattern = r"EMAIL_HOST_PASSWORD = 'YOUR_APP_PASSWORD_HERE'"
    new_pattern = f"EMAIL_HOST_PASSWORD = '{app_password}'"
    
    if old_pattern in content:
        new_content = content.replace(old_pattern, new_pattern)
        
        # Создаем резервную копию
        backup_file = f"{settings_file}.backup"
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Создана резервная копия: {backup_file}")
        except Exception as e:
            print(f"⚠️  Не удалось создать резервную копию: {e}")
        
        # Записываем обновленный файл
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ Настройки email обновлены!")
        except Exception as e:
            print(f"❌ Ошибка записи файла: {e}")
            return
        
        print("\n🎉 Настройка завершена!")
        print("Теперь можно тестировать отправку email:")
        print("python test_email.py")
        
    else:
        print("❌ Не найден placeholder 'YOUR_APP_PASSWORD_HERE' в settings.py")
        print("Убедитесь, что вы обновили файл settings.py согласно инструкции")

if __name__ == '__main__':
    update_settings_with_password() 