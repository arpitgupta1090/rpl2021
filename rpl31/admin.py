from django.contrib import admin
from .models import RplUsers, PlayerList, Selected, parmtable, Otptabl, SelectedPlayers


admin.site.register(RplUsers)
admin.site.register(PlayerList)
admin.site.register(Selected)
admin.site.register(parmtable)
admin.site.register(Otptabl)


@admin.register(SelectedPlayers)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "userName", "seriesId", "matchId", "bat1", "bat2", "bowl1", "bowl2", "allrounder")