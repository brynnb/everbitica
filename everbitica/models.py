from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PlayerClass (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_playable = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class ArmorType (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name
    
def __str__(self):
        return self.name
