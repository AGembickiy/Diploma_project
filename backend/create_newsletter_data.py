#!/usr/bin/env python
"""
Скрипт для создания тестовых данных новостных рассылок
"""

import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_backend.settings')
django.setup()

from newsletters.models import Newsletter, NewsletterTemplate
from users.models import User


def create_newsletter_templates():
    """Создать шаблоны рассылок"""
    templates_data = [
        {
            'name': 'Приветствие новых пользователей',
            'subject': 'Добро пожаловать в MMORPG Board!',
            'content': '''
Добро пожаловать в мир MMORPG Board!

Мы рады приветствовать вас в нашем сообществе игроков. Здесь вы можете:

🎮 Создавать объявления о поиске команды
👥 Находить единомышленников для совместной игры
📢 Обмениваться опытом и стратегиями
🏆 Участвовать в турнирах и событиях

Не забудьте заполнить свой профиль и создать первое объявление!

Удачной игры!
Команда MMORPG Board
            '''
        },
        {
            'name': 'Еженедельная сводка',
            'subject': 'Еженедельная сводка MMORPG Board',
            'content': '''
Еженедельная сводка MMORPG Board

📊 Статистика за неделю:
• Новых пользователей: {new_users_count}
• Создано объявлений: {advertisements_count}
• Успешных откликов: {responses_count}

🔥 Популярные категории:
{popular_categories}

🎯 Рекомендации:
• Обновляйте свои объявления регулярно
• Отвечайте на отклики своевременно
• Участвуйте в обсуждениях

Спасибо за активность!
Команда MMORPG Board
            '''
        },
        {
            'name': 'Уведомление о турнире',
            'subject': 'Новый турнир в MMORPG Board!',
            'content': '''
🏆 Новый турнир в MMORPG Board!

Приглашаем всех участников принять участие в новом турнире!

📅 Дата: {tournament_date}
⏰ Время: {tournament_time}
🎮 Игра: {game_name}
💰 Призовой фонд: {prize_pool}

📋 Правила:
• Команды по 5 человек
• Один игрок - одна команда
• Регистрация до {registration_deadline}

🎯 Регистрация: {registration_link}

Не упустите возможность показать свои навыки!
Команда MMORPG Board
            '''
        },
        {
            'name': 'Обновление системы',
            'subject': 'Обновление системы MMORPG Board',
            'content': '''
🔄 Обновление системы MMORPG Board

Мы обновили нашу платформу! Вот что нового:

✨ Новые функции:
• Улучшенный поиск объявлений
• Фильтрация по времени
• Статистика активности
• Уведомления в реальном времени

🐛 Исправления:
• Улучшена производительность
• Исправлены мелкие ошибки
• Обновлен дизайн

📱 Мобильная версия:
• Адаптивный дизайн
• Быстрая загрузка
• Удобная навигация

Спасибо за терпение!
Команда MMORPG Board
            '''
        }
    ]
    
    created_templates = []
    for template_data in templates_data:
        template, created = NewsletterTemplate.objects.get_or_create(
            name=template_data['name'],
            defaults=template_data
        )
        if created:
            print(f"✅ Создан шаблон: {template.name}")
        else:
            print(f"ℹ️  Шаблон уже существует: {template.name}")
        created_templates.append(template)
    
    return created_templates


def create_newsletters():
    """Создать тестовые рассылки"""
    # Получаем администратора
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("❌ Не найден администратор для создания рассылок")
        return
    
    newsletters_data = [
        {
            'title': 'Добро пожаловать в MMORPG Board!',
            'subject': 'Добро пожаловать в наше сообщество',
            'content': '''
Дорогие игроки!

Добро пожаловать в MMORPG Board - вашу платформу для поиска команды и единомышленников в мире MMORPG игр!

🎮 Что вы можете делать:
• Создавать объявления о поиске команды
• Откликаться на объявления других игроков
• Общаться с единомышленниками
• Участвовать в турнирах и событиях

📋 Начните прямо сейчас:
1. Заполните свой профиль
2. Создайте первое объявление
3. Найдите команду для совместной игры

Удачной игры!
Команда MMORPG Board
            ''',
            'send_to_new': True
        },
        {
            'title': 'Еженедельная сводка активности',
            'subject': 'Ваша активность за неделю',
            'content': '''
Привет, игроки!

Вот сводка активности за прошедшую неделю:

📊 Статистика:
• Новых объявлений: 47
• Успешных откликов: 23
• Активных пользователей: 156

🔥 Популярные категории:
1. Танки - 15 объявлений
2. ДД - 12 объявлений
3. Хилы - 8 объявлений

🎯 Рекомендации:
• Обновляйте объявления каждые 3-5 дней
• Отвечайте на отклики в течение 24 часов
• Участвуйте в обсуждениях

Спасибо за активность!
Команда MMORPG Board
            ''',
            'send_to_active': True
        },
        {
            'title': 'Новый турнир: "Битва кланов"',
            'subject': 'Регистрация на турнир открыта!',
            'content': '''
🏆 Турнир "Битва кланов" - регистрация открыта!

Приглашаем всех участников MMORPG Board принять участие в новом турнире!

📅 Дата: 15 декабря 2024
⏰ Время: 20:00 МСК
🎮 Формат: 5x5 командные бои
💰 Призовой фонд: 50,000 рублей

📋 Правила турнира:
• Команды по 5 человек
• Один игрок - одна команда
• Регистрация до 10 декабря
• Предварительные матчи 12-14 декабря

🎯 Регистрация: https://mmorpg-board.ru/tournament

Не упустите возможность показать свои навыки и выиграть призы!

Удачи в бою!
Команда MMORPG Board
            ''',
            'send_to_all': True
        }
    ]
    
    created_newsletters = []
    for newsletter_data in newsletters_data:
        newsletter, created = Newsletter.objects.get_or_create(
            title=newsletter_data['title'],
            defaults={
                **newsletter_data,
                'created_by': admin_user,
                'status': 'draft'
            }
        )
        if created:
            print(f"✅ Создана рассылка: {newsletter.title}")
        else:
            print(f"ℹ️  Рассылка уже существует: {newsletter.title}")
        created_newsletters.append(newsletter)
    
    return created_newsletters


def main():
    """Основная функция"""
    print("🚀 Создание тестовых данных для новостных рассылок...")
    
    # Создаем шаблоны
    print("\n📝 Создание шаблонов рассылок...")
    templates = create_newsletter_templates()
    
    # Создаем рассылки
    print("\n📧 Создание тестовых рассылок...")
    newsletters = create_newsletters()
    
    print(f"\n✅ Готово! Создано:")
    print(f"   • Шаблонов: {len(templates)}")
    print(f"   • Рассылок: {len(newsletters)}")
    print(f"\n🌐 Доступ к админке: http://localhost:8000/admin/")
    print(f"📊 API рассылок: http://localhost:8000/api/newsletters/")


if __name__ == '__main__':
    main()
