# GETNEXT Command Generator with MIB resolution
import string, sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
from optparse import OptionParser

# GETNEXT Command Generator with MIB resolution
def port_status_for_community_in_switch(protocol_version,community, switch, user, password, key):
  SWITCH_PORT = 161
  MAX_PORT_NUMBER = 49
  cmdGen = cmdgen.CommandGenerator()

  if protocol_version == 'v3':
    # SNMP v3
    protocol = cmdgen.UsmUserData(user, password, key)
  else:
    # SNMP v2
    protocol = cmdgen.CommunityData('test-agent', community)
  
  errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
    protocol,
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

def define_options(parser):
  parser.add_option("-u", "--user", dest="username",
                    help="User registered in the switch")
  parser.add_option("-p", "--password", dest="password",
                    help="User's password")
  parser.add_option("-k", "--key", dest="key",
                    help="Secret key")
  parser.add_option("-c", "--community", dest="community",
                    help="Swithc's community")
  
  
if __name__ == "__main__":
  usage = "usage: $python snmp.py ipaddress protocol [options] "
  parser = OptionParser(usage)
  define_options(parser)
  (options, args) = parser.parse_args()
  print options
  print args
  if len(args) < 2:
      parser.error("incorrect number of arguments")
  
  puertos = port_status_for_community_in_switch(args[1], 
                                                options.community, 
                                                args[0], 
                                                options.username, 
                                                options.password, 
                                                options.key)
  #puertos = port_status_for_community_in_switch('v3', 'alarmas', '132.248.51.18', 'centinela', 'InsT003H1n1', 'InsT003H1n1')
  print puertos