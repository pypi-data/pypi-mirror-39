from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist

from .conf import settings
from .exceptions import ExoMessagesException
from .queryset import MessageQuerySet


class MessageManager(Manager):
    use_for_related_fields = True
    use_in_migrations = True
    queryset_class = MessageQuerySet

    variable_counter_name = 'counter'

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db).filter(
                deleted=False).filter_by_user_active()

    def filter_by_user(self, user):
        return self.queryset_class(self.model, using=self._db).filter(
            deleted=False,
            user=user,
        )

    def create_message(self, user, code, level, *args, **kwargs):
        if code not in [_[0] for _ in settings.EXO_MESSAGES_CH_CODE]:
            raise ExoMessagesException('Invalid code')
        if level not in [_[0] for _ in settings.EXO_MESSAGES_CH_LEVEL]:
            raise ExoMessagesException('Invalid level')

        variables = kwargs.get('variables', {})
        variables.update({'user_pk': user.pk})

        return self.create(
            user=user,
            code=code,
            level=level,
            can_be_closed=kwargs.get('can_be_closed', False),
            read_when_login=kwargs.get('read_when_login', False),
            variables=variables)

    def clear_messages(self, user, code):
        messages = self.filter_by_user(user).filter_by_code(code)
        messages.delete()

    def update_or_create_message(
            self, user, code, level,
            can_be_closed=False, read_when_login=False,
            **kwargs):
        """
            Creates or update a message for a given User/Code:
        """
        should_create_new_message = created = False
        message = None
        variables = kwargs.get('variables', {})

        if code not in [_[0] for _ in settings.EXO_MESSAGES_CH_CODE]:
            raise ExoMessagesException('Invalid code')
        if level not in [_[0] for _ in settings.EXO_MESSAGES_CH_LEVEL]:
            raise ExoMessagesException('Invalid level')

        try:
            message = self.filter_by_user(user).get(
                user=user,
                code=code,
                level=level,
                read_at__isnull=True)

            if variables.get(self.variable_counter_name, None):
                # Update counter
                variables_updated = message.variables
                new_counter_value = message.variables.get(
                    self.variable_counter_name,
                    0)
                new_counter_value = new_counter_value + variables.get(
                    self.variable_counter_name)
                variables_updated[self.variable_counter_name] = new_counter_value
                self.filter_by_user(user).filter(
                    code=code,
                    level=level,
                    read_at__isnull=True
                ).update(variables=variables_updated)

        except ObjectDoesNotExist:
            should_create_new_message = created = True

        if should_create_new_message:
            variables['user_pk'] = user.pk
            message = self.create_message(
                user=user,
                code=code,
                level=level,
                can_be_closed=can_be_closed,
                read_when_login=read_when_login,
                variables=variables)

        return message, created


class MessageAllManager(Manager):
    queryset_class = MessageQuerySet

    def get_queryset(self):
        return self.queryset_class(
            self.model,
            using=self._db,
        ).filter(deleted=False)

    def filter_by_user(self, user):
        return self.get_queryset().filter(user=user)
