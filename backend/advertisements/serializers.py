from rest_framework import serializers
from .models import Advertisement
from users.serializers import UserSerializer

class AdvertisementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'category', 'author', 'image', 'video', 'audio', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

class AdvertisementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'category', 'image', 'video', 'audio']
    
    def create(self, validated_data):
        # Устанавливаем автора из request.user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
