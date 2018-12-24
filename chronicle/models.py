from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Chronicle(models.Model):
    """
        Characters exist in a Chronicle. If this is to be used by the wider VTM community, users will need to
        sign up to Chronicles, and characteres will exist *within* that Chronicle.
    """

    name = models.CharField()

    # The chronicle must be owned by a particular user, who is its' Storyteller. 
    storyteller = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

