from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    firstName = models.CharField(max_length=20, default="", null=True, blank=True)
    lastName = models.CharField(max_length=20, default="", null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"    


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organistaion = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username