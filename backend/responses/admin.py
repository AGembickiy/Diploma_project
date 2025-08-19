from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """Админка для откликов"""
    list_display = ['id', 'advertisement', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['advertisement__title', 'author__username', 'text']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('advertisement', 'author', 'text', 'status')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
