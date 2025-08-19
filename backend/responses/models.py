from django.db import models
from django.conf import settings
from advertisements.models import Advertisement

class Response(models.Model):
    """Модель отклика на объявление"""
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    ]
    
    advertisement = models.ForeignKey(
        Advertisement, 
        on_delete=models.CASCADE, 
        related_name='responses',
        verbose_name='Объявление'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Автор отклика'
    )
    text = models.TextField(verbose_name='Текст отклика')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']
        unique_together = ['advertisement', 'author']  # Один отклик от одного пользователя на одно объявление
    
    def __str__(self):
        return f'Отклик от {self.author.username} на "{self.advertisement.title}"'
