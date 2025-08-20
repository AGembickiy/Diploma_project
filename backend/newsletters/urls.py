from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsletterViewSet, NewsletterTemplateViewSet, NewsletterRecipientViewSet

router = DefaultRouter()
router.register(r'newsletters', NewsletterViewSet)
router.register(r'templates', NewsletterTemplateViewSet)
router.register(r'recipients', NewsletterRecipientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
