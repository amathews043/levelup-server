from django.db import models

class GameType(models.Model):
    type = models.CharField(max_length=50)