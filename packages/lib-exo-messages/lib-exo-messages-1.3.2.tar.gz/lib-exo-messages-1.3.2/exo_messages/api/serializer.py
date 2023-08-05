from django.contrib.auth import get_user_model

from rest_framework import serializers

from ..models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class CreateMessageSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        read_only=False,
        slug_field='uuid',
    )

    class Meta:
        model = Message
        fields = [
            'user', 'code', 'level', 'can_be_closed',
            'read_when_login', 'variables']
