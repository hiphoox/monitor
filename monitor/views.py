from django.http import HttpResponse 
from django.template import Context 
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from monitor.models import *

def main_page(request): 
  alarms = Alarm.objects.all()
  titulo = ""
  direccion = ""
  url = ""
  
  for alarm in alarms:
    titulo = alarm.computer.location.institute
    direccion = alarm.computer.location.address
    building = alarm.computer.location.building
    floor = alarm.computer.location.floor
    computer = str(event.computer.id)
    url = "/monitor/activities/?institute=" + titulo + ";building=" + building + ";floor=" + floor + ";computer=" + computer 
  
  variables = RequestContext(request, { 
    'user': request.user,
    'titulo': titulo,
    'direccion': direccion,
    'url': url
  })
  
  return render_to_response( 
    'monitor/main.html', variables
  )
    
@login_required 
def activities_page(request):
  institute = "institute";
  building = "building";
  floor = "floor";
  coordinates = "";
  
  if "institute" in request.GET:
    institute = request.GET["institute"];
  if "building" in request.GET:
    building = request.GET["building"];
  if "floor" in request.GET:
    floor = request.GET["floor"];
  if "computer" in request.GET:
    computer_id = request.GET["computer"];
    computer = Computer.objects.get(id=computer_id)
    coordinates = computer.coordinates

  variables = RequestContext(request, { 
    'activities_class': 'active',
    'institute_style': "background: url(/site_media/img/" + institute +".png)",
    'building_style': "background: url(/site_media/img/" + building +".png)",
    'floor_style': "background: url(/site_media/img/" + floor +".png)",
    'alarm_mark_style': "margin: " + coordinates
  })
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
  variables = RequestContext(request, { 
    'about_class': 'active'
  })
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
