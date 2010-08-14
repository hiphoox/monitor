from django.http import HttpResponse 
from django.template import Context 
from django.template.loader import get_template 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout
from django import forms
import subprocess
from monitor.domain import *

from django.contrib.auth.decorators import login_required
from monitor.models import *

def get_alarms():
  alarmse = Alarm.objects.filter(processed=False)[:10]
  alarms = []
  alarm_names = {}
  alarms.append(('','-----'))
  for alarm in alarmse:
    if alarm.computer_id not in alarm_names:
      alarm_names[alarm.computer_id] = "true"
      alarms.append((alarm.computer_id, alarm.computer.name))
  return alarms

class AlarmForm(forms.Form): 
  alarma = forms.ChoiceField(choices=get_alarms(), required=False)
  institute = forms.CharField(initial="IIMAS", widget=forms.widgets.HiddenInput, required=False)
  building = forms.CharField(initial="EPSUR", widget=forms.widgets.HiddenInput, required=False)
  floor    = forms.CharField(initial="PP", widget=forms.widgets.HiddenInput, required=False)
  alarma.widget.attrs["onchange"]="submitform()" 
  building.widget.attrs["hidden"]=True
  
def main_page(request): 
  alarms = Alarm.objects.filter(processed=False)  
  form_main = AlarmForm()  
  form_main.fields['alarma'].choices = get_alarms()
  print form_main
  variables = RequestContext(request, { 
    'alarms': alarms,
    'form': form_main
  })
#  variables['alarm_list'] = alarms
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
    coordinates = coordinates.replace("px", "")
    temporal = coordinates.split()
    offset = str(int(temporal[0]) - 45)
    coordinates = offset + "px " + temporal[1] + "px " + temporal[2]+ "px " + temporal[3]  + "px"
    
    location = computer.location
    alarm_title = location.get_institute_display() + ', '  + location.get_building_display() + ', ' + location.get_floor_display() + ', '  + computer.name;

  variables = {
    'alarm_title': alarm_title,
    'institute_style': "background: url(/site_media/img/" + institute + "/" + floor +".png)",
    'building_style': "background: url(/site_media/img/"+ institute + "/" + building +".png)",
    'floor_style': "background: url(/site_media/img/"+ institute + "/" + building + "-" + floor +".png)",
#    'computer_mark_style': "background: url(/site_media/img/" + computer_mark +".png)",
    'computer_mark_style': "margin: " + coordinates
  }
  return variables;

def get_computers_from(institute_value, building_value, floor_value):
  locatione = Location.objects.filter(institute=institute_value, building=building_value, floor=floor_value);
  computers = [];
  computers.append(('','-----'))
  for computer in Computer.objects.filter(location=locatione):
    computers.append((computer.id, computer.name));
  return computers

def get_computers():
  return get_computers_from("", "","")
  
def add_default(list):
  new_list = []
  new_list.append(('','-----'))
  for value in list:
    new_list.append(value)
  return new_list
  
class InstituteForm(forms.Form): 
  institute = forms.ChoiceField(choices=Location.INSTITUTES)
  building = forms.ChoiceField(choices=add_default(Location.BUILDINGS), required=False)
  floor = forms.ChoiceField(choices=add_default(Location.FLOORS), required=False)
  computer = forms.ChoiceField(choices=get_computers(), required=False)
  institute.widget.attrs["onchange"]="this.form.submit()" 
  building.widget.attrs["onchange"]="this.form.submit()" 
  floor.widget.attrs["onchange"]="this.form.submit()" 
  computer.widget.attrs["onchange"]="this.form.submit()" 
      
    
@login_required 
def activities_page(request):
  institute = "institute";
  building = "";
  floor = "PP";
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

  if institute == "institute":
    form = InstituteForm()
  else:
    form = InstituteForm(request.GET) # A form bound to the GET data
  
  form.fields['computer'].choices = get_computers_from(institute,building,floor)
  images_paths = get_images_paths_for(institute,building,floor,computer_id);
  images_paths['misc_class'] = 'active';
  images_paths['form'] = form;
  if computer_id != "" and floor != "":
    images_paths['computer_title'] = "alarm_title";
  #print images_paths;
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

def stop_alarm(computer_id, user):
  print "DETENIENDO ALARMA"
  monitor = SwitchMonitor()
  monitor.stop_alarm(computer_id, user)
  
def can_stop(computer_id):
  computer = Computer.objects.get(id=int(computer_id))  
  alarm_count = Alarm.objects.filter(computer=computer, pid__isnull=False).count()
  if alarm_count > 0:
    return True
  return False
  
def about_page(request): 
  institute = "institute";
  building = "";
  floor = "";
  coordinates = "";
  computer_id = "";

  if "detener" in request.GET and "alarma" in request.GET and "NO" != request.GET["detener"] and "" != request.GET["alarma"]:
    stop_alarm(request.GET["alarma"], request.user)
  
  if "institute" in request.GET:
    institute = request.GET["institute"];
  if "building" in request.GET:
    building = request.GET["building"];
  if "floor" in request.GET:
    floor = request.GET["floor"];
  if "alarma" in request.GET:
    computer_id = request.GET["alarma"];
  
  images_paths = get_images_paths_for(institute,building,floor,computer_id);
  variables = RequestContext(request, images_paths);

  if institute == "institute":
    form_about = AlarmForm()
  elif "detener" in request.GET and "alarma" in request.GET and "NO" != request.GET["detener"] and "" != request.GET["alarma"]:
    form_about = AlarmForm()    
  else:
    form_about = AlarmForm(request.GET) # A form bound to the GET data
  form_about.fields['alarma'].choices = get_alarms()
  print get_alarms()
  
  if computer_id != '':
    if can_stop(computer_id) and variables['alarm_title'] != "":
      variables['show_stop_button'] = 'Show';
  variables['about_class'] = 'active';
  variables['form'] = form_about;
  
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
