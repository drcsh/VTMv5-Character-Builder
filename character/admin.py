from django.contrib import admin

from .models import CharacterAttribute, CharacterSkill
from .models.discipline import Discipline
from .models.clan import Clan
from .models.character import Character
from .models.vampire_generation import Generation
from .models.minor_character import MinorCharacter


class AttributeInline(admin.TabularInline):
    model = CharacterAttribute
    fields = (('name', 'value'),)


class SkillInline(admin.TabularInline):
    model = CharacterSkill
    fields = (('name', 'value'),)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'chronicle', 'player']
    list_filter = ['chronicle', 'player']
    inlines = [
        AttributeInline,
        SkillInline
    ]

@admin.register(MinorCharacter)
class MinorCharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'chronicle', 'tag']
    list_filter = ['chronicle']


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name', 'clans']
    list_filter = ['clans']


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ['value']




