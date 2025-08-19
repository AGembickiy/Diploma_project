from rest_framework import serializers
from .models import Response
from users.serializers import UserSerializer
from advertisements.models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    """Простой сериализатор для объявления в откликах"""
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'category']

class ResponseSerializer(serializers.ModelSerializer):
    """Сериализатор для отклика"""
    author = UserSerializer(read_only=True)
    advertisement = AdvertisementSerializer(read_only=True)
    advertisement_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Response
        fields = ['id', 'advertisement', 'advertisement_id', 'author', 'text', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Устанавливаем автора из request.user
        validated_data['author'] = self.context['request'].user
        
        # Проверяем, что пользователь не является автором объявления
        advertisement_id = validated_data.get('advertisement_id')
        user = self.context['request'].user
        
        from advertisements.models import Advertisement
        try:
            advertisement = Advertisement.objects.get(id=advertisement_id)
            if advertisement.author == user:
                raise serializers.ValidationError(
                    "Вы не можете оставить отклик на свое собственное объявление."
                )
        except Advertisement.DoesNotExist:
            raise serializers.ValidationError("Объявление не найдено.")
        
        return super().create(validated_data)

class ResponseStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения статуса отклика"""
    
    class Meta:
        model = Response
        fields = ['status']
