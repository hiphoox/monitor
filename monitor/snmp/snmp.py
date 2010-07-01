# GETNEXT Command Generator with MIB resolution
import string
from pysnmp.entity.rfc3413.oneliner import cmdgen

# GETNEXT Command Generator with MIB resolution
def port_status_for_community_in_switch(community, switch):
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

  
if __name__ == "__main__":
  puertos = port_status_for_community_in_switch('alarmas', '132.248.51.194')
  print puertos