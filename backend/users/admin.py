from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailVerification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели пользователя"""
    
    list_display = ['email', 'username', 'email_verified', 'is_active', 'date_joined']
    list_filter = ['email_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('username', 'first_name', 'last_name')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Подтверждение email', {'fields': ('email_verified', 'verification_token', 'verification_token_created')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Админка для подтверждения email"""
    
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used', 'is_expired']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['token', 'created_at']
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Истек'
