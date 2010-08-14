import os, time, logging
from monitor.models import *
from monitor.snmp.snmp import *
import logging.handlers
import subprocess

LOG_FILENAME = 'log.out'
# Set up a specific logger with our desired output level
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

#File Handler
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5)
#Console handler
handler = logging.StreamHandler()
logger.addHandler(handler)


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
      monitor.save()
  
  
  def validate_monitor_state(self):
    '''We initialize the switchs_to_monitor dictionary to include all the switches and ports to be monitorated.
      We also get the initial state of all switches when the monitor starts.
    '''
    if self.needs_initialization():
      self.switchs = Switch.objects.all()
      for switch in self.switchs:
        if (switch.enabled):
          ports = port_status_for_community_in_switch(switch.protocol_version, switch.community, switch.ip_address, switch.user_name, switch.password, switch.encryption_key)
          self.switch_states[switch.identifier] = ports
        
      computers = Computer.objects.filter(enabled=True)
      for computer in computers:
        if not computer.switch.identifier in self.switchs_to_monitor:
          self.switchs_to_monitor[computer.switch.identifier] = []      
        ports = self.switchs_to_monitor[computer.switch.identifier]
        ports.append(computer.switch_port)
      
      self.reset_monitors() 
      #Debug section
      logger.debug("Initial Switch states: ")
      logger.debug(self.switch_states)
      logger.debug("Switchs & Ports to monitor: ")
      logger.debug(self.switchs_to_monitor)
      logger.debug("Switchs: ")
      logger.debug(self.switchs)
    
    
  def register_event(self, switch, port):
    key = "%i%i" % (switch.identifier, port)
    local_count = 1
    if key in self.events:
      (identifier, port, count, new_time) = self.events[key]
      local_count = count + 1

    self.events[key] = [switch.identifier, port, local_count, time.time()]
    #Debug section
    logger.debug("Events: ")
    logger.debug(self.events)
    
    
  def compare_switch_state(self, switch, current, previous, ports_to_monitor):
    """docstring for compare"""    
    for port in ports_to_monitor:
      if current[port] != previous[port]:
        logger.info("Registering event...")
        self.register_event(switch,port)


  def check_switch_states(self):
    for switch in self.switchs:
      if switch.identifier in self.switchs_to_monitor:
        if (switch.enabled):
          current_statuses = port_status_for_community_in_switch(switch.protocol_version, switch.community, switch.ip_address, switch.user_name, switch.password, switch.encryption_key)
          if len(current_statuses) != 0:
            previous_statuses = self.switch_states[switch.identifier]
            ports_to_monitor = self.switchs_to_monitor[switch.identifier]
            self.compare_switch_state(switch, current_statuses, previous_statuses, ports_to_monitor)
          else:
            print "HOLA MUNDO"
 
 
  def stop_alarm(self, computer_id, user):
    computer = Computer.objects.get(id=int(computer_id))
    alarms = Alarm.objects.filter(computer=computer)
    for alarm in alarms:
      if str(alarm.pid) != 'None':
        cmd = ['kill', str(alarm.pid)]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        print str(alarm.pid)
        alarm.processed = True
        alarm.pid = None
        alarm.employee = user
        alarm.save()
    
 
  def archive_event(self, key, identifier, port, count):
    self.events.pop(key)  
    switch = Switch.objects.get(identifier=identifier)
    computer = Computer.objects.get(switch=switch,switch_port=port)      
    new_event = Event(name=key, port_number=port, switch=switch, computer=computer, count=count)
    new_event.save()
    logger.info("Archiving event...")
    
    
  def alarm_is_ringing(self):
    alarm_count = Alarm.objects.filter(pid__isnull=False).count()
    if alarm_count > 0:
      print alarm_count
      return True
    else:
      print "TODO BIEN"
      return False
  
  
  def fire_alarm(self, key, identifier, port):
    self.events.pop(key)        
    switch = Switch.objects.get(identifier=identifier)
    computer = Computer.objects.get(switch=switch,switch_port=port)  
    same_alarm = Alarm.objects.filter(computer=computer, processed=False).count()
    
    if same_alarm > 0:
      return 
    
    if self.alarm_is_ringing():
      logger.info("Creating an alarm and just saving it...")
      new_alarm = Alarm(name=key, port_number=port, switch=switch, computer=computer, processed=False)
    else :
      logger.info("Creating and starting the alarm...")
      cmd = ['./monitor/sound.sh']
      p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
      logger.info("Alarm with process id: " + str(p.pid))
      new_alarm = Alarm(name=key, port_number=port, switch=switch, computer=computer, processed=False, pid=p.pid)

    new_alarm.save()
    
  
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
        self.archive_event(key, identifier, port, count)          
      elif count > alarm_threshold:
        self.fire_alarm(key, identifier, port)


  def sleep(self):
    monitors = Monitor.objects.filter(enabled=True)
    for monitor in monitors:
      sleep_time = monitor.sleep_time
    time.sleep(sleep_time)

    
  def start(self):    
    while True:
      self.validate_monitor_state()
      self.sleep()
      self.check_switch_states()
      self.process_events()
      