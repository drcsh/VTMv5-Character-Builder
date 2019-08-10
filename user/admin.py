from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class NewUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)