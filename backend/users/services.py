from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailVerification


class EmailService:
    """Сервис для отправки email"""
    
    @staticmethod
    def send_verification_email(user, verification):
        """Отправляет email для подтверждения регистрации"""
        
        # Создаем ссылку для подтверждения
        verification_url = f"{settings.SITE_URL}/verify-email?token={verification.token}"
        
        # HTML версия письма
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Подтверждение регистрации - MMORPG</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #667eea; color: white; 
                          padding: 12px 30px; text-decoration: none; border-radius: 5px; 
                          margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .token {{ background: #e9ecef; padding: 10px; border-radius: 5px; 
                         font-family: monospace; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎮 MMORPG</h1>
                    <p>Подтверждение регистрации</p>
                </div>
                <div class="content">
                    <h2>Здравствуйте, {user.username or user.email.split('@')[0]}!</h2>
                    
                    <p>Спасибо за регистрацию на нашем игровом портале MMORPG!</p>
                    
                    <p>Для завершения регистрации и активации вашего аккаунта, пожалуйста, 
                    подтвердите ваш email одним из способов:</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">
                            Подтвердить Email
                        </a>
                    </div>
                    
                    <p><strong>Или скопируйте токен подтверждения:</strong></p>
                    <div class="token">{verification.token}</div>
                    
                    <p><strong>Важно:</strong></p>
                    <ul>
                        <li>Токен действителен в течение {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} часов</li>
                        <li>Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо</li>
                        <li>После подтверждения вы сможете войти в свой аккаунт</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>С уважением,<br>Команда MMORPG</p>
                    <p>Это автоматическое письмо, не отвечайте на него</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Текстовая версия письма
        text_message = f"""
Здравствуйте, {user.username or user.email.split('@')[0]}!

Спасибо за регистрацию на нашем игровом портале MMORPG!

Для завершения регистрации и активации вашего аккаунта, пожалуйста, подтвердите ваш email.

Ссылка для подтверждения: {verification_url}

Токен подтверждения: {verification.token}

Токен действителен в течение {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} часов.

Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.

С уважением,
Команда MMORPG
        """
        
        try:
            send_mail(
                subject='🎮 Подтверждение регистрации - MMORPG',
                message=strip_tags(text_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False
    
    @staticmethod
    def send_welcome_email(user):
        """Отправляет приветственное письмо после подтверждения email"""
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Добро пожаловать в MMORPG!</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #28a745; color: white; 
                          padding: 12px 30px; text-decoration: none; border-radius: 5px; 
                          margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Добро пожаловать!</h1>
                    <p>Ваш аккаунт успешно активирован</p>
                </div>
                <div class="content">
                    <h2>Поздравляем, {user.username or user.email.split('@')[0]}!</h2>
                    
                    <p>Ваш аккаунт в MMORPG успешно активирован! 🎮</p>
                    
                    <p>Теперь вы можете:</p>
                    <ul>
                        <li>Войти в свой аккаунт</li>
                        <li>Создавать объявления</li>
                        <li>Отвечать на объявления других игроков</li>
                        <li>Участвовать в игровом сообществе</li>
                    </ul>
                    
                    <div style="text-align: center;">
                        <a href="{settings.SITE_URL}" class="button">
                            Перейти на сайт
                        </a>
                    </div>
                    
                    <p>Удачной игры! 🚀</p>
                </div>
                <div class="footer">
                    <p>С уважением,<br>Команда MMORPG</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_message = f"""
Поздравляем, {user.username or user.email.split('@')[0]}!

Ваш аккаунт в MMORPG успешно активирован!

Теперь вы можете войти в свой аккаунт и начать использовать все возможности нашего игрового портала.

Перейти на сайт: {settings.SITE_URL}

Удачной игры!

С уважением,
Команда MMORPG
        """
        
        try:
            send_mail(
                subject='🎉 Добро пожаловать в MMORPG!',
                message=strip_tags(text_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Ошибка отправки приветственного email: {e}")
            return False 