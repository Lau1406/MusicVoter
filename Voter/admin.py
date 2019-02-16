from django.contrib import admin
from Voter.models import *

# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'song',)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'image', 'length_ms', 'uri', 'votes',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'uri',)
