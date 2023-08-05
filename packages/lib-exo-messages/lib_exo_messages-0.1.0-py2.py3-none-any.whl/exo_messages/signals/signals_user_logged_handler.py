from django.apps import apps


def user_logged_handler(sender, **kwargs):
    Message = apps.get_model(
        app_label='exo_messages',
        model_name='Message')

    user = kwargs.get('user')
    Message.all_objects.filter_by_user(
        user).filter_read_when_login().already_read().delete()
    Message.all_objects.filter_by_user(
        user).filter_read_when_login().not_read().mark_read()
