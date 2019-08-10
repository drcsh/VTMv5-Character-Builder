from django.db import models
from django.contrib.auth.models import User

from chronicle.models import Chronicle


class Profile(models.Model):
    """
    User profile - extends the basic user model with additional fields and relationships.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    chronicles = models.ManyToManyField(
        Chronicle,
        related_name='player_profiles',
    )
