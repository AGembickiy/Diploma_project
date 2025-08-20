from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Newsletter, NewsletterRecipient, NewsletterTemplate
from .serializers import (
    NewsletterSerializer, NewsletterCreateSerializer,
    NewsletterRecipientSerializer, NewsletterTemplateSerializer,
    NewsletterStatsSerializer, NewsletterPreviewSerializer
)
from .services import NewsletterService, NewsletterScheduler


class IsAdminUser(permissions.BasePermission):
    """Разрешение только для администраторов"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class NewsletterViewSet(viewsets.ModelViewSet):
    """ViewSet для новостных рассылок"""
    
    queryset = Newsletter.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NewsletterCreateSerializer
        return NewsletterSerializer
    
    def perform_create(self, serializer):
        """Создать рассылку"""
        newsletter = serializer.save(created_by=self.request.user)
        
        # Создаем получателей
        NewsletterService.create_recipients(newsletter)
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Отправить рассылку"""
        newsletter = self.get_object()
        
        try:
            sent_count = NewsletterService.send_newsletter(newsletter)
            return Response({
                'message': f'Рассылка отправлена {sent_count} получателям',
                'sent_count': sent_count
            })
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Ошибка отправки: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Отменить рассылку"""
        newsletter = self.get_object()
        
        try:
            NewsletterService.cancel_newsletter(newsletter)
            return Response({'message': 'Рассылка отменена'})
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Дублировать рассылку"""
        newsletter = self.get_object()
        new_newsletter = NewsletterService.duplicate_newsletter(newsletter)
        
        serializer = self.get_serializer(new_newsletter)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """Предварительный просмотр рассылки"""
        newsletter = self.get_object()
        preview_data = NewsletterService.preview_newsletter(newsletter)
        
        serializer = NewsletterPreviewSerializer(preview_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def recipients(self, request, pk=None):
        """Получить список получателей рассылки"""
        newsletter = self.get_object()
        recipients = newsletter.recipients.all()
        
        page = self.paginate_queryset(recipients)
        if page is not None:
            serializer = NewsletterRecipientSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = NewsletterRecipientSerializer(recipients, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Получить статистику рассылок"""
        stats = NewsletterService.get_stats()
        serializer = NewsletterStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def process_scheduled(self, request):
        """Обработать запланированные рассылки"""
        try:
            NewsletterScheduler.process_scheduled_newsletters()
            return Response({'message': 'Запланированные рассылки обработаны'})
        except Exception as e:
            return Response(
                {'error': f'Ошибка обработки: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def cleanup(self, request):
        """Очистить старые рассылки"""
        days = request.data.get('days', 30)
        try:
            count = NewsletterScheduler.cleanup_old_newsletters(days)
            return Response({
                'message': f'Удалено {count} старых рассылок',
                'deleted_count': count
            })
        except Exception as e:
            return Response(
                {'error': f'Ошибка очистки: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NewsletterTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet для шаблонов рассылок"""
    
    queryset = NewsletterTemplate.objects.all()
    serializer_class = NewsletterTemplateSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """Использовать шаблон для создания рассылки"""
        template = self.get_object()
        
        # Создаем новую рассылку на основе шаблона
        newsletter = Newsletter.objects.create(
            title=f"Рассылка на основе шаблона '{template.name}'",
            content=template.content,
            subject=template.subject,
            created_by=request.user
        )
        
        serializer = NewsletterSerializer(newsletter)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsletterRecipientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получателей рассылок (только чтение)"""
    
    queryset = NewsletterRecipient.objects.all()
    serializer_class = NewsletterRecipientSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        """Фильтрация по рассылке"""
        queryset = super().get_queryset()
        newsletter_id = self.request.query_params.get('newsletter_id')
        
        if newsletter_id:
            queryset = queryset.filter(newsletter_id=newsletter_id)
        
        return queryset
