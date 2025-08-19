from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
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
            print(f'✅ Отклик создан: ID {response.id}, объявление: {response.advertisement.title}')
            
            # Отправляем email уведомление автору объявления
            self.send_response_notification(response)
            
        except Exception as e:
            print(f'❌ Ошибка при создании отклика: {e}')
            raise
    
    def perform_update(self, serializer):
        """Обновление статуса отклика с отправкой email уведомления"""
        old_status = serializer.instance.status
        response = serializer.save()
        
        # Если статус изменился, отправляем уведомление
        if old_status != response.status:
            self.send_status_change_notification(response, old_status)
    
    def send_response_notification(self, response):
        """Отправка email уведомления о новом отклике"""
        try:
            print(f'📧 Начинаем отправку email уведомления...')
            
            advertisement = response.advertisement
            author_email = advertisement.author.email
            author_username = advertisement.author.username
            
            print(f'📧 Данные для email:')
            print(f'   - Объявление: {advertisement.title}')
            print(f'   - Автор объявления: {author_username}')
            print(f'   - Email автора: {author_email}')
            print(f'   - Автор отклика: {response.author.username}')
            print(f'   - Текст отклика: {response.text[:50]}...')
            
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
            
            print(f'📧 Отправляем email...')
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[author_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f'✅ Email уведомление успешно отправлено на {author_email}')
            
        except Exception as e:
            print(f'❌ Ошибка отправки email: {e}')
            print(f'❌ Тип ошибки: {type(e).__name__}')
            import traceback
            print(f'❌ Traceback: {traceback.format_exc()}')
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
                'site_url': settings.SITE_URL
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
            
            print(f'✅ Email уведомление об изменении статуса отправлено на {respondent_email}')
            
        except Exception as e:
            print(f'❌ Ошибка отправки email: {e}')
    
    @action(detail=False, methods=['get'])
    def my_responses(self, request):
        """Получить все отклики текущего пользователя"""
        responses = self.get_queryset()
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def advertisement_responses(self, request, advertisement_id=None):
        """Получить все отклики на конкретное объявление (только для автора объявления)"""
        responses = self.get_queryset()
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        """Изменить статус отклика (только для автора объявления)"""
        response = self.get_object()
        
        # Проверяем, что пользователь является автором объявления
        if response.advertisement.author != request.user:
            return Response(
                {'error': 'Вы можете изменять статус только откликов на свои объявления'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ResponseStatusSerializer(response, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
