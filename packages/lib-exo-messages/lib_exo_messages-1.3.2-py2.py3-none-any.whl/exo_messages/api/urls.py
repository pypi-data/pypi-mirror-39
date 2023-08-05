try:
    from django.conf.urls import url, include
except ImportError:
    from django.urls import re_path as url
    from django.urls import include

from rest_framework.routers import DefaultRouter

from .views import MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, base_name='message')

app_name = 'exo_messages'

urlpatterns = [
    url(r'^', include(router.urls)),
]
