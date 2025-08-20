import logging
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import Newsletter, NewsletterRecipient
from users.models import User

logger = logging.getLogger(__name__)


class NewsletterService:
    """Сервис для работы с новостными рассылками"""
    
    @staticmethod
    def create_recipients(newsletter):
        """Создать записи получателей для рассылки"""
        recipients = newsletter.get_recipients()
        
        # Создаем записи получателей
        recipient_objects = []
        for user in recipients:
            recipient_objects.append(
                NewsletterRecipient(
                    newsletter=newsletter,
                    user=user,
                    status='pending'
                )
            )
        
        # Массовое создание записей
        NewsletterRecipient.objects.bulk_create(
            recipient_objects, 
            ignore_conflicts=True
        )
        
        # Обновляем общее количество получателей
        newsletter.total_recipients = newsletter.recipients.count()
        newsletter.save(update_fields=['total_recipients'])
        
        return newsletter.recipients.count()
    
    @staticmethod
    def send_newsletter(newsletter):
        """Отправить рассылку"""
        if newsletter.status != 'draft':
            raise ValueError("Можно отправлять только черновики")
        
        # Обновляем статус
        newsletter.status = 'sending'
        newsletter.save(update_fields=['status'])
        
        try:
            # Получаем всех получателей со статусом 'pending'
            recipients = newsletter.recipients.filter(status='pending')
            
            if not recipients.exists():
                newsletter.status = 'sent'
                newsletter.sent_at = timezone.now()
                newsletter.save(update_fields=['status', 'sent_at'])
                return 0
            
            # Подготавливаем данные для массовой отправки
            email_data = []
            for recipient in recipients:
                try:
                    # Формируем HTML контент
                    html_content = render_to_string(
                        'newsletters/email/newsletter.html',
                        {
                            'user': recipient.user,
                            'newsletter': newsletter,
                            'unsubscribe_url': f"{settings.SITE_URL}/unsubscribe/{recipient.id}/"
                        }
                    )
                    
                    email_data.append((
                        newsletter.subject,
                        html_content,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient.user.email]
                    ))
                    
                    # Обновляем статус получателя
                    recipient.status = 'sent'
                    recipient.sent_at = timezone.now()
                    recipient.save(update_fields=['status', 'sent_at'])
                    
                except Exception as e:
                    logger.error(f"Ошибка отправки письма {recipient.user.email}: {e}")
                    recipient.status = 'failed'
                    recipient.error_message = str(e)
                    recipient.save(update_fields=['status', 'error_message'])
            
            # Отправляем письма
            if email_data:
                send_mass_mail(email_data, fail_silently=False)
            
            # Обновляем статистику
            sent_count = newsletter.recipients.filter(status='sent').count()
            failed_count = newsletter.recipients.filter(status='failed').count()
            
            newsletter.sent_count = sent_count
            newsletter.failed_count = failed_count
            newsletter.status = 'sent'
            newsletter.sent_at = timezone.now()
            newsletter.save(update_fields=['sent_count', 'failed_count', 'status', 'sent_at'])
            
            return sent_count
            
        except Exception as e:
            logger.error(f"Ошибка отправки рассылки {newsletter.id}: {e}")
            newsletter.status = 'draft'
            newsletter.save(update_fields=['status'])
            raise
    
    @staticmethod
    def cancel_newsletter(newsletter):
        """Отменить рассылку"""
        if newsletter.status not in ['draft', 'sending']:
            raise ValueError("Можно отменить только черновики или отправляющиеся рассылки")
        
        newsletter.status = 'cancelled'
        newsletter.save(update_fields=['status'])
        
        # Отменяем все ожидающие отправки
        newsletter.recipients.filter(status='pending').update(status='cancelled')
        
        return True
    
    @staticmethod
    def duplicate_newsletter(newsletter):
        """Дублировать рассылку"""
        new_newsletter = Newsletter.objects.create(
            title=f"{newsletter.title} (копия)",
            content=newsletter.content,
            subject=newsletter.subject,
            send_to_all=newsletter.send_to_all,
            send_to_active=newsletter.send_to_active,
            send_to_new=newsletter.send_to_new,
            created_by=newsletter.created_by
        )
        
        return new_newsletter
    
    @staticmethod
    def get_stats():
        """Получить статистику рассылок"""
        newsletters = Newsletter.objects.all()
        
        stats = {
            'total_newsletters': newsletters.count(),
            'draft_count': newsletters.filter(status='draft').count(),
            'sending_count': newsletters.filter(status='sending').count(),
            'sent_count': newsletters.filter(status='sent').count(),
            'cancelled_count': newsletters.filter(status='cancelled').count(),
            'total_recipients': sum(n.total_recipients for n in newsletters),
            'total_sent': sum(n.sent_count for n in newsletters),
            'total_failed': sum(n.failed_count for n in newsletters),
        }
        
        # Вычисляем процент успешных отправок
        total_attempts = stats['total_sent'] + stats['total_failed']
        if total_attempts > 0:
            stats['success_rate'] = (stats['total_sent'] / total_attempts) * 100
        else:
            stats['success_rate'] = 0.0
        
        return stats
    
    @staticmethod
    def preview_newsletter(newsletter):
        """Предварительный просмотр рассылки"""
        recipients = newsletter.get_recipients()
        recipients_preview = [
            f"{user.username} ({user.email})" 
            for user in recipients[:10]
        ]
        
        return {
            'subject': newsletter.subject,
            'content': newsletter.content,
            'recipients_count': recipients.count(),
            'recipients_preview': recipients_preview
        }


class NewsletterScheduler:
    """Планировщик рассылок"""
    
    @staticmethod
    def process_scheduled_newsletters():
        """Обработать запланированные рассылки"""
        now = timezone.now()
        scheduled_newsletters = Newsletter.objects.filter(
            status='draft',
            scheduled_at__lte=now
        )
        
        for newsletter in scheduled_newsletters:
            try:
                NewsletterService.send_newsletter(newsletter)
                logger.info(f"Отправлена запланированная рассылка {newsletter.id}")
            except Exception as e:
                logger.error(f"Ошибка отправки запланированной рассылки {newsletter.id}: {e}")
    
    @staticmethod
    def cleanup_old_newsletters(days=30):
        """Очистить старые рассылки"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        # Удаляем старые рассылки и связанные записи
        old_newsletters = Newsletter.objects.filter(
            created_at__lt=cutoff_date,
            status__in=['sent', 'cancelled']
        )
        
        count = old_newsletters.count()
        old_newsletters.delete()
        
        logger.info(f"Удалено {count} старых рассылок")
        return count
