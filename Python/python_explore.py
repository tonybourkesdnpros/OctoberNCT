#!/usr/bin/python3
import yaml


# Simple Variables

i = 1 # Integers
z = "This is a string" # Strings

# Complex variables

list = ['Kirk', 'Spock', 'McCoy', 'Sulu', 'Smith']


def add_numbers(x, y):
    z = x + y
    return z

result = add_numbers(10, 20)

print(result)


output_json = open("output.json", 'r')

output = yaml.safe_load(output_json)

#print(output['result'][0])


def show_ips():
    for interface in output['result'][0]['interfaces']:
        ip = output['result'][0]['interfaces'][interface]['interfaceAddress']['ipAddr']['address']
        print("The interface", interface, "has an IP address of", ip)

#show_ips()


# ship_yaml = open("ships.yml", 'r')


# dictionary = yaml.safe_load(ship_yaml)


# # #print(dictionary['NCC-74656'])
# # # Loops!

# for ship, crew in dictionary.items():
#     for position in crew:
#         print("The", position, "of the", ship, "is", dictionary[ship][position])
    



