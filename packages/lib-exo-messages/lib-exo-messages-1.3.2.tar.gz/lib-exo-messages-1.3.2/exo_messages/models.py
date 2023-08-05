from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from model_utils.models import TimeStampedModel

from .conf import settings
from .manager import MessageManager, MessageAllManager


class Message(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='messages',
        on_delete=models.deletion.CASCADE,
    )

    can_be_closed = models.BooleanField(default=False)
    read_when_login = models.BooleanField(default=False)

    description = models.TextField(blank=True)

    code = models.CharField(
        max_length=1,
        choices=settings.EXO_MESSAGES_CH_CODE,
    )
    level = models.IntegerField(
        choices=settings.EXO_MESSAGES_CH_LEVEL,
    )

    variables = JSONField()

    read_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    objects = MessageManager()
    all_objects = MessageAllManager()

    def __str__(self):
        return '{}-{}'.format(self.user, self.get_code_display())

    def mark_as_read(self):
        self.read_at = timezone.now()
        self.save(update_fields=['read_at'])

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save(update_fields=['deleted'])

    def force_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
