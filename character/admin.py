from django.contrib import admin
from .models.discipline import Discipline
from .models.clan import Clan
from .models.character import Character
from .models.vampire_generation import Generation
from .models.minor_character import MinorCharacter

#Todo: set up custom admins for Character and MinorCharacter to pull in the other classes as fields

# Register your models here.
admin.register(Discipline)
admin.register(Clan)
admin.register(Generation)
admin.register(Character)
admin.register(MinorCharacter)
