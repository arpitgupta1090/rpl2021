from django.contrib import admin
from .models import RplUsers, PlayerList, Selected, parmtable

# Register your models here.

admin.site.register(RplUsers)
admin.site.register(PlayerList)
admin.site.register(Selected)
admin.site.register(parmtable)
