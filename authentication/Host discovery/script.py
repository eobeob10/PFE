import subprocess
import os
import pandas as pd
# if connected to wifi, i want to print SSID
# ffe600


def SSID():
    os.system('ls /sys/class/net | grep wlan > wlan.txt')
    with open('wlan.txt') as f:
        for i in f.readlines():
            x = subprocess.check_output(['/sbin/iwconfig ', i[:-1], " |",
                                        'grep SSID ', ' | ', 'cut -d " '"'",  '- f 2'])
            AP = 'Access Point'
            output = subprocess.check_output(['cat ', x,
                                             ' | grep ', AP, '| cut -d ', ':', '-f 4,5,6,7,8,9'], shell=True)
            print(output)


# if not then grep ip address
lst = []


def not_SSID():
    os.system('ls /sys/class/net >interface.txt')
    with open('interface.txt') as fl:
        for i in fl.readlines():
            net = subprocess.check_output(['ip -4  addr show ',
                                          i[:-1], ' | ', "grep -oP '(?<=inet\s)\d+(\.\d+){3}'"], shell=True)
        lst.append(net)


def default():
    details = []
    lst = [2, 3, 4, 5]
    os.system(
        'route | ' + " grep '^default' | grep -o '[^ ]*$' > default.txt")
    with open("default.txt") as f:
        for i in f.readlines():
            for j in lst:
                x = subprocess.check_output("ifconfig " + i[:-1] + ' | ' +
                                            'awk ' + "'$1==", 'inet', '"{print $"' + str(j)+"}'", shell=True)
                x = x.strip()
                details.append(x)


# we need to add the details of ifconfig
# details = os.system('ip addr show ' + i)


def asset_discovery():
    # SSID()
    # not_SSID()
    default()


asset_discovery()
