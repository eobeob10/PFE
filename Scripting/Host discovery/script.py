import os
# if connected to wifi, i want to print SSID
os.system('ls /sys/class/net | grep wlan > wlan.txt')
with open('wlan.txt') as f:
    for i in f.readlines():
        os.system(' ip addr show ' + i[:-1] + "|" +
                  'grep -Po ' + "'"+"inet \K[\d.]+'")
        print(i)


# if not then grep ip address
os.system('ls /sys/class/net >interface.txt')
with open('interface.txt') as fl:
    for i in fl.readlines():

        os.system(' ip addr show ' + i[:-1] + "|" +
                  'grep -Po ' + "'"+"inet \K[\d.]+'")
        print(i)

# we need to add the details of ifconfig
details = os.system('ip addr show ' + i)
