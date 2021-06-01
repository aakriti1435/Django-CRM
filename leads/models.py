from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class LeadManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


class Lead(models.Model):
    firstName = models.CharField(max_length=20, default="", null=True, blank=True)
    lastName = models.CharField(max_length=20, default="", null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    dateAdded = models.DateTimeField(auto_now_add = True)
    phoneNumber = models.CharField(max_length=20)
    email = models.EmailField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    converted_date = models.DateTimeField(null=True, blank=True)

    objects = LeadManager()

    def __str__(self):
        return f"{self.firstName} {self.lastName}"    


def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"


class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.lead.firstName} {self.lead.lastName}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Signals
def postUserCreatedSignal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(postUserCreatedSignal, sender=User) 

