from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ..models import Message
from .serializer import MessageSerializer


class MessageViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
):

    model = Message
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter_by_user(
            self.request.user).filter_by_user_active()

    def get_all_queryset(self):
        return Message.all_objects.filter_by_user(self.request.user)

    @detail_route(methods=['post'], url_path='close')
    def close(self, request, pk):
        self.get_all_queryset().filter(pk=pk, can_be_closed=True).delete()
        return Response('ok')
