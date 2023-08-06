from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from epsilon.models import Epsilon


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_post_save(sender, instance, **kwargs):
    if settings.EPSILON_AUTO_PUSH:
        data_to_send = instance.get_epsilon_profile()
        Epsilon.addProfile(data_to_send)
