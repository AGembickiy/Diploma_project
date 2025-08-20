#!/usr/bin/env python
"""
Скрипт для создания тестовых данных
"""
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_backend.settings')
django.setup()

from users.models import User
from advertisements.models import Advertisement
from responses.models import Response

def create_test_data():
    """Создает тестовые данные"""
    
    # Создаем тестового пользователя
    try:
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123',
            email_verified=True
        )
        pass
    except Exception as e:
        test_user = User.objects.get(username='testuser')
    
    # Создаем тестовые объявления
    categories = ['Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры']
    
    advertisements = []
    for i, category in enumerate(categories):
        try:
            ad = Advertisement.objects.create(
                title=f'Тестовое объявление {i+1} - {category}',
                description=f'Описание для объявления {i+1} в категории {category}. Ищем игроков для совместной игры.',
                category=category,
                author=test_user
            )
            advertisements.append(ad)
            pass
        except Exception as e:
            ad = Advertisement.objects.get(title__contains=f'Тестовое объявление {i+1}')
            advertisements.append(ad)
    
    # Создаем тестовые отклики
    response_texts = [
        "Привет! Я заинтересован в вашем объявлении. У меня есть опыт в этой роли.",
        "Здравствуйте! Хотел бы присоединиться к вашей команде. Играю уже 2 года.",
        "Приветствую! Ищу команду для совместной игры. Готов к обсуждению деталей.",
        "Добрый день! Заинтересован в вашем предложении. Есть вопросы по условиям.",
        "Привет! Хотел бы узнать больше о вашем проекте. Готов к сотрудничеству."
    ]
    
    for i, ad in enumerate(advertisements):
        try:
            response = Response.objects.create(
                advertisement=ad,
                author=test_user,
                text=response_texts[i % len(response_texts)],
                status='new' if i % 2 == 0 else 'accepted'
            )
            pass
        except Exception as e:
            pass
    
    print("🎉 Тестовые данные созданы успешно!")
    print(f"📊 Статистика:")
    print(f"   - Пользователей: {User.objects.count()}")
    print(f"   - Объявлений: {Advertisement.objects.count()}")
    print(f"   - Откликов: {Response.objects.count()}")

if __name__ == '__main__':
    create_test_data()
