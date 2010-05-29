# encoding: utf-8
from monitor.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django import forms


############################################################################################################
#######################################   Catalogs Admin  ##################################################  
############################################################################################################
class CatalogAdmin(admin.ModelAdmin):
  list_filter = ('enabled',)
  save_on_top = True

admin.site.register(Area, CatalogAdmin)
admin.site.register(Location, CatalogAdmin)
admin.site.register(Room, CatalogAdmin)
admin.site.register(MapKey, CatalogAdmin)
admin.site.register(Message, CatalogAdmin)

############################################################################################################
#######################################   Models Admin  ##################################################  
############################################################################################################
admin.site.register(Switch)
admin.site.register(Computer)
admin.site.register(Employee)
