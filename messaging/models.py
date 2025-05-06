from django.db import models
from django.utils import timezone

from api.models import Department

# Create your models here.


class Message(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    olympiad = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.department} - {self.olympiad} - {self.time} - {self.text[:max(len(self.text), 20)]}..."
