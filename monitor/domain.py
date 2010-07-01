import os, time
from monitor.models import *
from monitor.snmp.snmp import *

class SwitchMonitor:
  '''This variable holds all the initial switch states. 
     If we add a computer port to the switch_to_monitor this variable will need to be flushed and reloaded.  
  '''
  switch_states = {} 
  switchs_to_monitor = {}
  switchs = {}
  events = {}
  
  def needs_initialization(self):
    '''If any monitor has a change we will refresh the state.'''
    monitors = Monitor.objects.filter(enabled=True)
    for monitor in monitors:
      if monitor.conf_has_changed:
        return True
    return False

  def reset_monitors(self):
    monitors = Monitor.objects.filter(enabled=True)
    for monitor in monitors:
      monitor.conf_has_changed = False
      monitor.save
  
  def validate_monitor_state(self):
    '''We initialize the switchs_to_monitor dictionary to include all the switches and ports to be monitorated.
      We also get the initial state of all switches when the monitor starts.
    '''
    if self.needs_initialization():
      self.switchs = Switch.objects.all()
      for switch in self.switchs:
        if (switch.enabled):
          ports = port_status_for_community_in_switch(switch.community, switch.ip_address)
          self.switch_states[switch.identifier] = ports
        
      computers = Computer.objects.filter(enabled=True)
      for computer in computers:
        if not computer.switch.identifier in self.switchs_to_monitor:
          self.switchs_to_monitor[computer.switch.identifier] = []      
        ports = self.switchs_to_monitor[computer.switch.identifier]
        ports.append(computer.switch_port)
      
      self.reset_monitors() 
    
    
  def register_event(self, switch, port):
    key = "%i%i" % (switch.identifier, port)
    local_count = 1
    if key in self.events:
      (identifier, port, count, time) = self.events[key]
      local_count = count + 1

    self.events[key] = [switch.identifier, port, local_count, time.time()]
    print self.events
    
    
  def compare_switch_state(self, switch, current, previous, ports_to_monitor):
    """docstring for compare"""    
    for port in ports_to_monitor:
      if current[port] != previous[port]:
        self.register_event(switch,port)
        print "Bravo"

  def check_switch_states(self):
    for switch in self.switchs:
      if switch.identifier in self.switchs_to_monitor:
        current_statuses = port_status_for_community_in_switch(switch.community, switch.ip_address)
        if len(current_statuses) != 0:
          previous_statuses = self.switch_states[switch.identifier]
          ports_to_monitor = self.switchs_to_monitor[switch.identifier]
          self.compare_switch_state(switch, current_statuses, previous_statuses, ports_to_monitor)
  
  
  def process_events(self):
    local_count_index = 2
    alarm_threshold = 5
    purge_time = 3600
    
    monitors = Monitor.objects.filter(enabled=True)
    for monitor in monitors:
      purge_time = monitor.purge_time
      alarm_threshold = monitor.alarm_threshold
    
    for key, value in self.events.items():
      (identifier, port, count, current_time) = self.events[key]
      #Log and purge events older than one hour
      if time.time() - current_time > purge_time:
        self.events.pop(key)  
        switch = Switch.objects.get(identifier=identifier)
        computer = Computer.objects.get(switch=switch,switch_port=port)      
        new_event = Event(name=key, port_number=port, switch=switch, computer=computer, count=count)
        new_event.save()
        print "Archiving event..."
              
      elif count > alarm_threshold:
        self.events.pop(key)        
        switch = Switch.objects.get(identifier=identifier)
        computer = Computer.objects.get(switch=switch,switch_port=port)      
        new_alarm = Alarm(name=key, port_number=port, switch=switch, computer=computer, processed=False)
        new_alarm.save()
        # send mail. fire alarm
        print "Creating alarm..."
    
    
  def start(self):
    while True:
      self.validate_monitor_state()
      self.check_switch_states()
      self.process_events()
      time.sleep(3)

