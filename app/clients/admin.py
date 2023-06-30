from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Client, Match


class CustomUserAdmin(UserAdmin):
    model = Client
    list_display = ['email', 'username', 'first_name',
                    'last_name', 'avatar',]


class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ['client1', 'client2', 'created_at']


admin.site.register(Client, CustomUserAdmin)
admin.site.register(Match, MatchAdmin)
