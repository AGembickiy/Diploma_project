from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResponseViewSet

router = DefaultRouter()
router.register(r'responses', ResponseViewSet, basename='response')

urlpatterns = [
    path('', include(router.urls)),
    # Добавляем специальный endpoint для откликов на конкретное объявление
    path('advertisements/<int:advertisement_id>/responses/', 
         ResponseViewSet.as_view({'get': 'advertisement_responses'}), 
         name='advertisement-responses'),
    # Добавляем endpoint для изменения статуса отклика
    path('responses/<int:pk>/change_status/', 
         ResponseViewSet.as_view({'patch': 'change_status'}), 
         name='response-change-status'),
]
