from django.conf import settings
from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patients",
    )

    def __str__(self):
        return self.name
