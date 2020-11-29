from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Article


@receiver(pre_save, sender=Article)
def reset_counter(sender, instance, *args, **kwargs):
    instance.views_count = 0
