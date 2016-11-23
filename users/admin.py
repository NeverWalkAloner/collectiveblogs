from django.contrib import admin
from .models import Profile, KarmaVotes


# Register your models here.
class KarmaAdmin(admin.ModelAdmin):
    list_display = ['vote_for', 'vote_from', 'vote_result']
    list_filter = ['vote_for', 'vote_from']

admin.site.register(Profile)
admin.site.register(KarmaVotes, KarmaAdmin)