import uuid

from django.db import models


class Article(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    body = models.CharField(max_length=160, blank=True)
    views_count = models.PositiveIntegerField(default=0)
