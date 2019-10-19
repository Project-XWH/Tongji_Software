from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Advice(models.Model):
    text = models.EmailField()
    advice_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
