from django.contrib import admin
from Voter.models import *

# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    pass


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass
