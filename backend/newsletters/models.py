from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Newsletter(models.Model):
    """Модель для новостных рассылок"""
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('sending', 'Отправляется'),
        ('sent', 'Отправлено'),
        ('cancelled', 'Отменено'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    subject = models.CharField(max_length=200, verbose_name='Тема письма')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name='Статус'
    )
    
    # Настройки отправки
    send_to_all = models.BooleanField(
        default=False, 
        verbose_name='Отправить всем пользователям'
    )
    send_to_active = models.BooleanField(
        default=False, 
        verbose_name='Отправить только активным пользователям'
    )
    send_to_new = models.BooleanField(
        default=False, 
        verbose_name='Отправить только новым пользователям (зарегистрированным за последние 7 дней)'
    )
    
    # Метаданные
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_newsletters',
        verbose_name='Создатель'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    scheduled_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Запланированная дата отправки'
    )
    sent_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Дата отправки'
    )
    
    # Статистика
    total_recipients = models.IntegerField(
        default=0, 
        verbose_name='Общее количество получателей'
    )
    sent_count = models.IntegerField(
        default=0, 
        verbose_name='Количество отправленных'
    )
    failed_count = models.IntegerField(
        default=0, 
        verbose_name='Количество неудачных отправок'
    )
    
    class Meta:
        verbose_name = 'Новостная рассылка'
        verbose_name_plural = 'Новостные рассылки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def get_recipients(self):
        """Получить список получателей рассылки"""
        if self.send_to_all:
            return User.objects.filter(is_active=True)
        elif self.send_to_active:
            return User.objects.filter(is_active=True, date_joined__lt=timezone.now() - timezone.timedelta(days=7))
        elif self.send_to_new:
            return User.objects.filter(
                is_active=True, 
                date_joined__gte=timezone.now() - timezone.timedelta(days=7)
            )
        return User.objects.none()


class NewsletterRecipient(models.Model):
    """Модель для отслеживания получателей рассылок"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает отправки'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка отправки'),
        ('bounced', 'Отклонено'),
    ]
    
    newsletter = models.ForeignKey(
        Newsletter, 
        on_delete=models.CASCADE, 
        related_name='recipients',
        verbose_name='Рассылка'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='newsletter_recipients',
        verbose_name='Пользователь'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Статус'
    )
    sent_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Дата отправки'
    )
    error_message = models.TextField(
        blank=True, 
        verbose_name='Сообщение об ошибке'
    )
    
    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылок'
        unique_together = ['newsletter', 'user']
    
    def __str__(self):
        return f"{self.user.email} - {self.newsletter.title}"


class NewsletterTemplate(models.Model):
    """Модель для шаблонов рассылок"""
    
    name = models.CharField(max_length=100, verbose_name='Название шаблона')
    subject = models.CharField(max_length=200, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Шаблон рассылки'
        verbose_name_plural = 'Шаблоны рассылок'
        ordering = ['name']
    
    def __str__(self):
        return self.name
