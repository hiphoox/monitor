from django.http import HttpResponse 
from django.template import Context 
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout
from django import forms

from django.contrib.auth.decorators import login_required
from monitor.models import *

def main_page(request): 
  alarms = Alarm.objects.filter(processed=False)    
  variables = RequestContext(request, { 
    'alarms': alarms
  })
  
  variables['alarm_list'] = alarms
  
  return render_to_response( 
    'monitor/main.html', variables
  )

'''institute=IIMAS;building=EP;floor=PP;computer=2'''
def get_images_paths_for(institute, building, floor, computer_id):
  computer_mark = "mark2";
  coordinates = "";
  location = "";
  alarm_title = "";
  
  if(computer_id != ''):
    computer = Computer.objects.get(id=computer_id)
    coordinates = computer.coordinates
    location = computer.location
    alarm_title = location.get_institute_display() + ', '  + location.get_building_display() + ', ' + location.get_floor_display() + ', '  + computer.name;

  variables = {
    'about_class': 'active',
    'alarm_title': alarm_title,
    'institute_style': "background: url(/site_media/img/" + institute + "/" + floor +".png)",
    'building_style': "background: url(/site_media/img/"+ institute + "/" + building +".png)",
    'floor_style': "background: url(/site_media/img/"+ institute + "/" + building + "-" + floor +".png)",
#    'computer_mark_style': "background: url(/site_media/img/" + computer_mark +".png)",
    'computer_mark_style': "margin: " + coordinates
  }
  return variables;

@login_required 
def activities_page(request):
  institute = "institute";
  building = "";
  floor = "";
  coordinates = "";

  if "institute" in request.GET:
    institute = request.GET["institute"];
  if "building" in request.GET:
    building = request.GET["building"];
  if "floor" in request.GET:
    floor = request.GET["floor"];
  if "computer" in request.GET:
    computer_id = request.GET["computer"];
  
  images_paths = get_images_paths_for(institute,building,floor,computer_id);
  variables = RequestContext(request, images_paths);
  return render_to_response( 
    'monitor/activities.html', variables
  )
  
@login_required 
def reports_page(request): 
  variables = RequestContext(request, { 
    'reports_class': 'active'
  })
  return render_to_response( 
    'monitor/reports.html', variables
  )

@login_required 
def misc_page(request): 
  variables = RequestContext(request, { 
    'misc_class': 'active'
  })
  return render_to_response( 
    'monitor/misc.html', variables
  )
  
  
def about_page(request): 
  
  institute = "institute";
  building = "";
  floor = "";
  coordinates = "";
  computer_id = "";

  if "institute" in request.GET:
    institute = request.GET["institute"];
  if "building" in request.GET:
    building = request.GET["building"];
  if "floor" in request.GET:
    floor = request.GET["floor"];
  if "computer" in request.GET:
    computer_id = request.GET["computer"];
  
  images_paths = get_images_paths_for(institute,building,floor,computer_id);
  variables = RequestContext(request, images_paths);

  alarms = Alarm.objects.filter(processed=False)    
  variables['alarm_list'] = alarms
  
  return render_to_response( 
    'monitor/about.html', variables
  )
  
def help_page(request): 
  variables = RequestContext(request, { 
    'help_class': 'active'
  })
  return render_to_response( 
    'monitor/help.html', variables
  )

def logout_page(request): 
  logout(request) 
  variables = RequestContext(request, { 
    'logged_out_class': 'active'
  })
  return render_to_response( 
    'monitor/logged_out.html', variables
  )
#  return HttpResponseRedirect('/') 

@login_required 
def account_page(request): 
  variables = RequestContext(request, { 
    'account_class': 'nothing'
  })
  return render_to_response( 
    'monitor/account.html', variables
  )
