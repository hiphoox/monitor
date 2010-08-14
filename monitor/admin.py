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
  date_hierarchy = 'created'
  list_display  = ('name', 'description','created', 'modified','enabled')
  list_filter = ('enabled', 'created',)
  save_on_top = True
  readonly_fields = ('created', 'modified') 

admin.site.register(Area,     CatalogAdmin)
admin.site.register(Location, CatalogAdmin)
admin.site.register(Room,     CatalogAdmin)
admin.site.register(MapKey,   CatalogAdmin)
admin.site.register(Message,  CatalogAdmin)

############################################################################################################
#######################################   Models Admin  ##################################################  
############################################################################################################
class SwitchAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_display  = ('name', 'description','ip_address', 'protocol_version','ports_number','created', 'modified','enabled')
  list_filter   = ('protocol_version',)
  save_on_top   =  True
  search_fields = ['name', 'description']
  actions       = 'delete_selected' 
  readonly_fields = ('created', 'modified') 
admin.site.register(Switch, SwitchAdmin)

class EventAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_display  = ('name','port_number','switch', 'computer', 'count', 'created', 'modified')
  list_filter   = ('created',)
  save_on_top   =  True
  search_fields = ['name', 'computer']
  actions       = 'delete_selected' 
  readonly_fields = ('created', 'modified') 
admin.site.register(Event, EventAdmin)

class AlarmAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_display  = ('name','port_number','switch', 'computer','processed','created', 'modified')
  list_filter   = ('created',)
  save_on_top   =  True
  search_fields = ['name', 'computer']
  actions       = 'delete_selected' 
  readonly_fields = ('created', 'modified') 
admin.site.register(Alarm, AlarmAdmin)

class ComputerAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_display  = ('name','description','switch', 'ip_address','location','created', 'modified', 'enabled')
  list_filter   = ('created',)
  save_on_top   =  True
  search_fields = ['name', 'description']
  actions       = 'delete_selected' 
  readonly_fields = ('created', 'modified') 
admin.site.register(Computer, ComputerAdmin)

class MonitorAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_display  = ('name','purge_time','alarm_threshold','conf_has_changed','created', 'modified', 'enabled')
  list_filter   = ('created',)
  save_on_top   =  True
  search_fields = ['name']
  actions       = 'delete_selected' 
  readonly_fields = ('created', 'modified') 
admin.site.register(Monitor, MonitorAdmin)

class SwitchStatusAdmin(admin.ModelAdmin):
  date_hierarchy = 'created'
  list_display  = ('name', 'created', 'modified', 'checked')
  list_filter   = ('created',)
  save_on_top   =  True  
  search_fields = ['created']
  actions       = 'delete_selected' 
  readonly_fields = ('created', 'modified') 
admin.site.register(SwitchStatus, SwitchStatusAdmin)


#admin.site.register(UserProfile)
admin.site.unregister(User) 
class UserProfileInline(admin.StackedInline): 
    model = UserProfile 
class UserProfileAdmin(UserAdmin): 
    inlines = [UserProfileInline] 
admin.site.register(User, UserProfileAdmin) 
