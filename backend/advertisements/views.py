from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Advertisement
from .serializers import AdvertisementSerializer, AdvertisementCreateSerializer

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Возвращает объявления текущего пользователя"""
        return Advertisement.objects.filter(author=self.request.user)
    
    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от действия"""
        if self.action == 'create':
            return AdvertisementCreateSerializer
        return AdvertisementSerializer
    
    def perform_create(self, serializer):
        """Автоматически устанавливает автора при создании"""
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_advertisements(self, request):
        """Получить все объявления текущего пользователя"""
        advertisements = self.get_queryset()
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public_advertisements(self, request):
        """Получить все публичные объявления (для гостей)"""
        advertisements = Advertisement.objects.all().order_by('-created_at')
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)
