from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Response
from .serializers import ResponseSerializer, ResponseStatusSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    """ViewSet для управления откликами"""
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Возвращает отклики в зависимости от роли пользователя"""
        user = self.request.user
        
        if self.action == 'my_responses':
            # Пользователь видит свои отклики
            return Response.objects.filter(author=user)
        elif self.action == 'advertisement_responses':
            # Автор объявления видит отклики на свои объявления
            advertisement_id = self.kwargs.get('advertisement_id')
            return Response.objects.filter(advertisement_id=advertisement_id, advertisement__author=user)
        elif self.action in ['change_status', 'destroy', 'update', 'partial_update', 'retrieve']:
            # Для изменения/удаления/просмотра - все отклики на объявления пользователя
            return Response.objects.filter(advertisement__author=user)
        else:
            # По умолчанию пользователь видит свои отклики
            return Response.objects.filter(author=user)
    
    def perform_create(self, serializer):
        """Создание отклика с отправкой email уведомления"""
        try:
            # Проверяем, не оставлял ли пользователь уже отклик на это объявление
            advertisement_id = serializer.validated_data.get('advertisement_id')
            user = self.request.user
            
            # Проверяем, что пользователь не является автором объявления
            from advertisements.models import Advertisement
            try:
                advertisement = Advertisement.objects.get(id=advertisement_id)
                if advertisement.author == user:
                    raise serializers.ValidationError(
                        "Вы не можете оставить отклик на свое собственное объявление."
                    )
            except Advertisement.DoesNotExist:
                raise serializers.ValidationError("Объявление не найдено.")
            
            existing_response = Response.objects.filter(
                advertisement_id=advertisement_id,
                author=user
            ).first()
            
            if existing_response:
                raise serializers.ValidationError(
                    f"Вы уже оставляли отклик на это объявление. "
                    f"Ваш предыдущий отклик: '{existing_response.text[:50]}...'"
                )
            
            response = serializer.save()
            
            # Отправляем email уведомление автору объявления
            self.send_response_notification(response)
            
        except Exception as e:
            raise
    
    def perform_update(self, serializer):
        """Обновление статуса отклика с отправкой email уведомления"""
        old_status = serializer.instance.status
        response = serializer.save()
        
        # Если статус изменился, отправляем уведомление
        if old_status != response.status:
            print(f"🔄 Статус отклика изменился: {old_status} -> {response.status}")
            self.send_status_change_notification(response, old_status)
        else:
            print(f"ℹ️ Статус отклика не изменился: {old_status}")
    
    def send_response_notification(self, response):
        """Отправка email уведомления о новом отклике"""
        try:
            advertisement = response.advertisement
            author_email = advertisement.author.email
            author_username = advertisement.author.username
            
            subject = f'Новый отклик на ваше объявление "{advertisement.title}"'
            
            # HTML версия письма
            html_message = render_to_string('responses/email/new_response.html', {
                'author_username': author_username,
                'advertisement_title': advertisement.title,
                'response_text': response.text,
                'respondent_username': response.author.username,
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3001')
            })
            
            # Текстовая версия письма
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[author_email],
                html_message=html_message,
                fail_silently=False,
            )
            
        except Exception as e:
            # Логируем ошибку для отладки
            print(f"❌ Ошибка отправки email уведомления: {e}")
            # Не прерываем создание отклика из-за ошибки email
    
    def send_status_change_notification(self, response, old_status):
        """Отправка email уведомления об изменении статуса отклика"""
        try:
            advertisement = response.advertisement
            respondent_email = response.author.email
            respondent_username = response.author.username
            
            status_labels = {
                'accepted': 'принят',
                'rejected': 'отклонен'
            }
            
            subject = f'Статус вашего отклика изменен на "{status_labels.get(response.status, response.status)}"'
            
            # HTML версия письма
            html_message = render_to_string('responses/email/status_change.html', {
                'respondent_username': respondent_username,
                'advertisement_title': advertisement.title,
                'old_status': status_labels.get(old_status, old_status),
                'new_status': status_labels.get(response.status, response.status),
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:3001')
            })
            
            # Текстовая версия письма
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[respondent_email],
                html_message=html_message,
                fail_silently=False,
            )
            
        except Exception as e:
            # Логируем ошибку для отладки
            print(f"❌ Ошибка отправки email уведомления: {e}")
            # Не прерываем процесс из-за ошибки email
    
    @action(detail=False, methods=['get'])
    def my_responses(self, request):
        """Получить все отклики текущего пользователя"""
        responses = self.get_queryset()
        serializer = ResponseSerializer(responses, many=True)
        return DRFResponse(serializer.data)
    
    @action(detail=False, methods=['get'])
    def advertisement_responses(self, request, advertisement_id=None):
        """Получить все отклики на объявления текущего пользователя с фильтрацией"""
        user = request.user
        
        # Получаем все отклики на объявления пользователя
        queryset = Response.objects.filter(advertisement__author=user)
        
        # Применяем фильтры
        advertisement_id = request.query_params.get('advertisement_id')
        status_filter = request.query_params.get('status')
        
        if advertisement_id and advertisement_id != 'all':
            queryset = queryset.filter(advertisement_id=advertisement_id)
        
        if status_filter and status_filter != 'all':
            queryset = queryset.filter(status=status_filter)
        
        serializer = ResponseSerializer(queryset, many=True)
        return DRFResponse(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        """Изменить статус отклика (только для автора объявления)"""
        response = self.get_object()
        
        serializer = ResponseStatusSerializer(response, data=request.data, partial=True)
        if serializer.is_valid():
            # Используем perform_update для автоматической отправки email
            self.perform_update(serializer)
            return DRFResponse(serializer.data)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
