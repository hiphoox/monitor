import os
import time
import string
from django.core.management.base import BaseCommand
from django.conf import settings
from pysnmp.entity.rfc3413.oneliner import cmdgen
from monitor.models import *

class SwitchMonitor:
  switch_states = {}
  switchs_to_monitor = {}
  switchs = {}
  events = []
  
  # GETNEXT Command Generator with MIB resolution
  def port_status_for_community_in_switch(self, community, switch):
    SWITCH_PORT = 161
    MAX_PORT_NUMBER = 49
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
      # SNMP v2
      #cmdgen.CommunityData('test-agent', community),
      # SNMP v3
      cmdgen.UsmUserData('centinela', 'InsT003H101', 'InsT003H101'),
      # Transport
      cmdgen.UdpTransportTarget((switch, SWITCH_PORT)), (('IF-MIB', 'ifOperStatus'),),)

    ports = {}
    if errorIndication:
      print "Error:"
      print errorIndication
    else:
      if errorStatus:
        print '%s at %s\n' % (
            errorStatus.prettyPrint(),
            varBindTable[-1][int(errorIndex)-1]
            )
      else:
        for varBindTableRow in varBindTable:
          for oid, val in varBindTableRow:
            (symName, modName), indices = cmdgen.mibvar.oidToMibName(cmdGen.mibViewController, oid )
            val = cmdgen.mibvar.cloneFromMibValue( cmdGen.mibViewController, modName, symName, val )
        
            index = int(string.join(map(lambda v: v.prettyPrint(), indices), '.'))
            if index < MAX_PORT_NUMBER:
              ports[index] = val.prettyPrint()

    return ports
  
  def __init__(self):
    self.switchs = Switch.objects.all()
    for switch in self.switchs:
      if (switch.enabled):
        ports = self.port_status_for_community_in_switch(switch.community, switch.ip_address)
        self.switch_states[switch.identifier] = ports
        
    computers = Computer.objects.filter(enabled=True)
    for computer in computers:
      if not computer.switch.identifier in self.switchs_to_monitor:
        self.switchs_to_monitor[computer.switch.identifier] = []      
      ports = self.switchs_to_monitor[computer.switch.identifier]
      ports.append(computer.switch_port)
    
    
  def register_event(self, switch, port):
    self.events.append([switch.identifier, port])
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
        current_statuses = self.port_status_for_community_in_switch(switch.community, switch.ip_address)
        if len(current_statuses) != 0
          previous_statuses = self.switch_states[switch.identifier]
          ports_to_monitor = self.switchs_to_monitor[switch.identifier]
          self.compare_switch_state(switch, current_statuses, previous_statuses, ports_to_monitor)
  
  
  def process_events(self):
    for (identifier, port) in self.events:
      switch = Switch.objects.get(identifier=identifier)
      computer = Computer.objects.get(switch=switch,switch_port=port)      
      new_event = Event(name="Name", port_number=port, switch=switch, computer=computer)
      new_event.save()
      print "Saving..."
    self.events = []
    
    
  def start(self):
    while True:
      self.check_switch_states()
      self.process_events()
      time.sleep(3)


class Command(BaseCommand):
  help = ("Run the monitor demon")
  
  def handle(self, *args, **options):
    print "Running the demon..."
    switchMonitor = SwitchMonitor()
    switchMonitor.start()
    #stop(switch_statuses)
    
    
    