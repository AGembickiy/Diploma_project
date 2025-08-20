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
        """Возвращает объявления в зависимости от действия"""
        if self.action == 'retrieve':
            # Для просмотра конкретного объявления разрешаем всем
            return Advertisement.objects.all()
        elif self.action == 'my_advertisements':
            # Только объявления текущего пользователя
            return Advertisement.objects.filter(author=self.request.user)
        else:
            # По умолчанию только объявления текущего пользователя
            return Advertisement.objects.filter(author=self.request.user)
    
    def get_permissions(self):
        """Разрешаем просмотр объявлений всем пользователям"""
        if self.action in ['retrieve', 'public_advertisements']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от действия"""
        if self.action == 'create':
            return AdvertisementCreateSerializer
        return AdvertisementSerializer
    
    def perform_create(self, serializer):
        """Автоматически устанавливает автора при создании"""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Проверяем, что пользователь редактирует свое объявление"""
        advertisement = serializer.instance
        if advertisement.author != self.request.user:
            raise permissions.PermissionDenied("Вы можете редактировать только свои объявления")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Проверяем, что пользователь удаляет свое объявление"""
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Вы можете удалять только свои объявления")
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def my_advertisements(self, request):
        """Получить все объявления текущего пользователя"""
        advertisements = self.get_queryset()
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public_advertisements(self, request):
        """Получить все публичные объявления (исключая авторизованного пользователя)"""
        if request.user.is_authenticated:
            # Для авторизованных пользователей исключаем их собственные объявления
            advertisements = Advertisement.objects.exclude(author=request.user).order_by('-created_at')
        else:
            # Для гостей показываем все объявления
            advertisements = Advertisement.objects.all().order_by('-created_at')
        
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data)
