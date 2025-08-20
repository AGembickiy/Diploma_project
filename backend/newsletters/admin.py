from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Newsletter, NewsletterRecipient, NewsletterTemplate
from .services import NewsletterService


@admin.register(NewsletterTemplate)
class NewsletterTemplateAdmin(admin.ModelAdmin):
    """Админка для шаблонов рассылок"""
    
    list_display = ['name', 'subject', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'subject', 'content']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'subject', 'content')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
        ('Метаданные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewsletterRecipient)
class NewsletterRecipientAdmin(admin.ModelAdmin):
    """Админка для получателей рассылок"""
    
    list_display = ['user', 'newsletter', 'status', 'sent_at']
    list_filter = ['status', 'sent_at', 'newsletter']
    search_fields = ['user__username', 'user__email', 'newsletter__title']
    readonly_fields = ['newsletter', 'user', 'sent_at', 'error_message']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Админка для новостных рассылок"""
    
    list_display = [
        'title', 'status', 'created_by', 'total_recipients', 
        'sent_count', 'created_at', 'sent_at'
    ]
    list_filter = ['status', 'created_at', 'sent_at', 'created_by']
    search_fields = ['title', 'subject', 'content']
    readonly_fields = [
        'created_by', 'created_at', 'sent_at', 
        'total_recipients', 'sent_count', 'failed_count'
    ]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subject', 'content')
        }),
        ('Настройки отправки', {
            'fields': ('send_to_all', 'send_to_active', 'send_to_new', 'scheduled_at')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Статистика', {
            'fields': ('total_recipients', 'sent_count', 'failed_count'),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_by', 'created_at', 'sent_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['send_newsletter', 'cancel_newsletter', 'duplicate_newsletter']
    
    def save_model(self, request, obj, form, change):
        """Сохранить модель"""
        if not change:  # Создание новой рассылки
            obj.created_by = request.user
        
        super().save_model(request, obj, form, change)
        
        # Создаем получателей при создании
        if not change:
            NewsletterService.create_recipients(obj)
    
    @admin.action(description='Отправить выбранные рассылки')
    def send_newsletter(self, request, queryset):
        """Отправить рассылки"""
        success_count = 0
        error_count = 0
        
        for newsletter in queryset:
            try:
                if newsletter.status == 'draft':
                    NewsletterService.send_newsletter(newsletter)
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request, 
                    f'Ошибка отправки рассылки "{newsletter.title}": {str(e)}', 
                    level='ERROR'
                )
        
        if success_count > 0:
            self.message_user(
                request, 
                f'Успешно отправлено {success_count} рассылок'
            )
        
        if error_count > 0:
            self.message_user(
                request, 
                f'Не удалось отправить {error_count} рассылок', 
                level='WARNING'
            )
    
    @admin.action(description='Отменить выбранные рассылки')
    def cancel_newsletter(self, request, queryset):
        """Отменить рассылки"""
        success_count = 0
        error_count = 0
        
        for newsletter in queryset:
            try:
                if newsletter.status in ['draft', 'sending']:
                    NewsletterService.cancel_newsletter(newsletter)
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request, 
                    f'Ошибка отмены рассылки "{newsletter.title}": {str(e)}', 
                    level='ERROR'
                )
        
        if success_count > 0:
            self.message_user(
                request, 
                f'Успешно отменено {success_count} рассылок'
            )
        
        if error_count > 0:
            self.message_user(
                request, 
                f'Не удалось отменить {error_count} рассылок', 
                level='WARNING'
            )
    
    @admin.action(description='Дублировать выбранные рассылки')
    def duplicate_newsletter(self, request, queryset):
        """Дублировать рассылки"""
        success_count = 0
        
        for newsletter in queryset:
            try:
                NewsletterService.duplicate_newsletter(newsletter)
                success_count += 1
            except Exception as e:
                self.message_user(
                    request, 
                    f'Ошибка дублирования рассылки "{newsletter.title}": {str(e)}', 
                    level='ERROR'
                )
        
        if success_count > 0:
            self.message_user(
                request, 
                f'Успешно создано {success_count} копий рассылок'
            )
    
    def get_queryset(self, request):
        """Получить queryset с дополнительными полями"""
        return super().get_queryset(request).select_related('created_by')
