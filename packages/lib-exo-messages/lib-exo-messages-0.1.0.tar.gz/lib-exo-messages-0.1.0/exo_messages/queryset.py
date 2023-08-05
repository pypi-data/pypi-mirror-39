from django.db import models
from django.utils import timezone

from .conf import settings


class MessageQuerySet(models.QuerySet):

    def filter_read_when_login(self):
        return self.filter(read_when_login=True)

    def not_read(self):
        return self.filter(read_at__isnull=True)

    def already_read(self):
        return self.filter(read_at__isnull=False)

    def mark_read(self):
        self.update(read_at=timezone.now())

    def filter_by_code(self, code):
        return self.filter(code=code)

    def delete(self):
        self.update(deleted=True)

    def filter_by_user_active(self):
        default_statement = {
            models.When(
                user__is_active=True,
                then=models.Value(True),
            )
        }
        users_active_statement = getattr(
            settings,
            'CUSTOM_EXO_MESSAGE_USER_ACTIVE_STATEMENT',
            default_statement)

        status_case = models.Case(
            *users_active_statement,
            default=models.Value(False),
            output_field=models.BooleanField())
        return self.annotate(user_status=status_case).filter(user_status=True)
