from rest_framework import serializers
from .models import Newsletter, NewsletterRecipient, NewsletterTemplate
from users.serializers import UserSerializer


class NewsletterTemplateSerializer(serializers.ModelSerializer):
    """Сериализатор для шаблонов рассылок"""
    
    class Meta:
        model = NewsletterTemplate
        fields = ['id', 'name', 'subject', 'content', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class NewsletterRecipientSerializer(serializers.ModelSerializer):
    """Сериализатор для получателей рассылок"""
    
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = NewsletterRecipient
        fields = [
            'id', 'user', 'status', 'status_display', 
            'sent_at', 'error_message'
        ]
        read_only_fields = ['id', 'user', 'sent_at', 'error_message']


class NewsletterSerializer(serializers.ModelSerializer):
    """Сериализатор для новостных рассылок"""
    
    created_by = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    recipients = NewsletterRecipientSerializer(many=True, read_only=True)
    recipients_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Newsletter
        fields = [
            'id', 'title', 'content', 'subject', 'status', 'status_display',
            'send_to_all', 'send_to_active', 'send_to_new',
            'created_by', 'created_at', 'scheduled_at', 'sent_at',
            'total_recipients', 'sent_count', 'failed_count',
            'recipients', 'recipients_count'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'sent_at',
            'total_recipients', 'sent_count', 'failed_count',
            'recipients'
        ]
    
    def get_recipients_count(self, obj):
        """Получить количество получателей"""
        return obj.recipients.count()
    
    def validate(self, data):
        """Валидация данных рассылки"""
        # Проверяем, что выбран хотя бы один тип отправки
        send_types = [
            data.get('send_to_all', False),
            data.get('send_to_active', False),
            data.get('send_to_new', False)
        ]
        
        if not any(send_types):
            raise serializers.ValidationError(
                "Необходимо выбрать хотя бы один тип получателей"
            )
        
        # Проверяем, что выбран только один тип отправки
        if sum(send_types) > 1:
            raise serializers.ValidationError(
                "Можно выбрать только один тип получателей"
            )
        
        return data


class NewsletterCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рассылок"""
    
    class Meta:
        model = Newsletter
        fields = [
            'title', 'content', 'subject',
            'send_to_all', 'send_to_active', 'send_to_new',
            'scheduled_at'
        ]
    
    def validate(self, data):
        """Валидация данных рассылки"""
        # Проверяем, что выбран хотя бы один тип отправки
        send_types = [
            data.get('send_to_all', False),
            data.get('send_to_active', False),
            data.get('send_to_new', False)
        ]
        
        if not any(send_types):
            raise serializers.ValidationError(
                "Необходимо выбрать хотя бы один тип получателей"
            )
        
        # Проверяем, что выбран только один тип отправки
        if sum(send_types) > 1:
            raise serializers.ValidationError(
                "Можно выбрать только один тип получателей"
            )
        
        return data


class NewsletterStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики рассылок"""
    
    total_newsletters = serializers.IntegerField()
    draft_count = serializers.IntegerField()
    sending_count = serializers.IntegerField()
    sent_count = serializers.IntegerField()
    cancelled_count = serializers.IntegerField()
    total_recipients = serializers.IntegerField()
    total_sent = serializers.IntegerField()
    total_failed = serializers.IntegerField()
    success_rate = serializers.FloatField()


class NewsletterPreviewSerializer(serializers.Serializer):
    """Сериализатор для предварительного просмотра рассылки"""
    
    subject = serializers.CharField()
    content = serializers.CharField()
    recipients_count = serializers.IntegerField()
    recipients_preview = serializers.ListField(
        child=serializers.CharField(),
        max_length=10
    )
