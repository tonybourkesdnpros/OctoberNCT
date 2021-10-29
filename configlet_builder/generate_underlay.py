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

prefix_list = """
ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 20 permit 192.168.102.0/24 eq 32
    seq 30 permit 192.168.201.0/24 eq 32
    seq 40 permit 192.168.202.0/24 eq 32
    seq 50 permit 192.168.253.0/24 eq 32
"""
route_map = """
route-map LOOPBACK permit 10
   match ip address prefix-list LOOPBACK
"""

peer_filter = """
peer-filter LEAF-AS-RANGE
 10 match as-range 65000-65535 result accept
"""

# Global Variables

mtu = underlay['global']['MTU']

def generate_interfaces():
  for interface in underlay[hostname]['interfaces']:
    ip = underlay[hostname]['interfaces'][interface]['ipv4']
    mask = underlay[hostname]['interfaces'][interface]['mask']
    print("interface %s") % interface
    print("   ip address %s/%s") % (ip, mask)
    if 'Ethernet' in interface:
      print("   no switchport")
      print("   mtu %s") % mtu
      
def generate_leaf_BGP():
  loopback0 = underlay[hostname]['interfaces']['loopback0']['ipv4']
  ASN = underlay[hostname]['BGP']['ASN']
  spine_ASN = underlay['global']['DC1']['spine_ASN']

  print(prefix_list)
  print(route_map)
  print("router bgp %s") % ASN
  print("   router-id %s") % loopback0
  
  print("   neighbor Underlay peer group")
  print("   neighbor Underlay remote-as %s") % spine_ASN
  print("   neighbor Underlay send-community")
  print("   neighbor Underlay maximum-routes 12000")
  
  spine_peers = underlay[hostname]['BGP']['spine-peers']
  for spine in spine_peers:
    print("    neighbor %s peer group Underlay") % spine
  
  print("    address-family ipv4")
  print("       neighbor Underlay activate")
  print("       redistribute connected route-map LOOPBACK")
  
def generate_spine_BGP():
  loopback0 = underlay[hostname]['interfaces']['loopback0']['ipv4']
  ASN = underlay[hostname]['BGP']['ASN']
  print(peer_filter)
  print(prefix_list)
  print(route_map)
  print("router bgp %s") % ASN
  print("   router-id %s") % loopback0
  print("   no bgp default ipv4-unicast")
  print("   maximum-paths 3")
  print("   distance bgp 20 200 200")
  print("   bgp listen range 192.168.103.0/24 peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE")
  print("   neighbor LEAF_Underlay peer group")
  print("   neighbor LEAF_Underlay send-community")
  print("   neighbor LEAF_Underlay maximum-routes 12000")
  print("   address-family ipv4")
  print("   neighbor LEAF_Underlay activate")
  print("   redistribute connected route-map LOOPBACK")
  

  
      
generate_interfaces()

if 'leaf' in hostname:
  generate_leaf_BGP()
if 'spine' in hostname:
  generate_spine_BGP()
