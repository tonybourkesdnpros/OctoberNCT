from cvplibrary import CVPGlobalVariables, GlobalVariableNames
from cvplibrary import RestClient
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

stuff = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)

for item in stuff: 
  key, value = item.split(':')
  if key == 'hostname':
    hostname = value

import yaml

cvp_url = 'https://192.168.0.5/cvpservice/'
configlet = 'underlay_YAML'

rest_client = RestClient(cvp_url+'configlet/getConfigletByName.do?name='+configlet,'GET')

if rest_client.connect():
  raw = yaml.safe_load(rest_client.getResponse())

underlay = yaml.safe_load(raw['config'])



# Global Variables

mtu = underlay['global']['MTU']

for interface in underlay[hostname]['interfaces']:
  ip = underlay[hostname]['interfaces'][interface]['ipv4']
  mask = underlay[hostname]['interfaces'][interface]['mask']
  print("interface %s") % interface
  print("   ip address %s/%s") % (ip, mask)
  if 'Ethernet' in interface:
    print("   no switchport")
    print("   mtu %s") % mtu

