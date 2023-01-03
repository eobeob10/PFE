import os
import subprocess

def banner_grab(IP):
    subprocess.Popen("nc -vn <IP> 23",shell=True)