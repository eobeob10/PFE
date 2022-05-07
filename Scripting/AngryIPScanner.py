import os
import sys

global path
path = os.system('whereis '+'ipscan-3.8.2_amd64.exe')
file = open("Target.txt")
input = file.read()
os.system(str(path) + '-f: ' + input + '-s -q -o AngryIPScanner.txt')
