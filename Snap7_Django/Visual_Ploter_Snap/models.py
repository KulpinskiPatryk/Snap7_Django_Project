from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Odczyty(models.Model):
    czas = models.DateTimeField(auto_now=True)
    temperatura = models.IntegerField()
    prad = models.IntegerField()
    napiecie = models.IntegerField()

    def __str__(self):
        return str(self.id) + " " + str(self.czas)

    class Meta:
        ordering = ('czas',)
        verbose_name_plural = "Odczyty"
# Create your models here.
