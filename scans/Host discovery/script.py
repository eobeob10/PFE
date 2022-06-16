import os
# if connected to wifi, i want to print SSID
os.system('ls /sys/class/net | grep wlan > wlan.txt')
with open('wlan.txt') as f:
    for i in f.readlines():
        name = os.system(
            ' ip addr show ' + i + '|grep -Po ' + "'"+"inet \K[\d.]+'")
# if not then grep ip address
os.system('ls /sys/class/net >interface.txt')
with open('interface.txt') as fl:
    for i in fl.readlines():

        os.system(' ip addr show ' + i[:-1] + "|" +
                  'grep -Po ' + "'"+"inet \K[\d.]+'")

# we need to add the details of ifconfig
details = os.system('ip addr show ' + i)
