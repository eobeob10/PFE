import os
import subprocess

def banner_grab(IP):
    subprocess.Popen(f"nc -vn {IP} 22")

def ssh_key(IP, PORT="22"):
    subprocess.Popen(f"ssh-keyscan -t rsa {IP} -p {PORT}")

def nmap_default(IP, PORT="22"):
    subprocess.Popen(f"nmap -sC -sV -p {PORT} {IP}")

def nmap_supported_algorithms(IP):
    subprocess.Popen(f"nmap -p 22 {IP} --script ssh2-enum-algos")

def nmap_weak_keys(IP):
    subprocess.Popen(f"nmap -p 22 {IP} --script ssh-hostkey --script-args ssh_hostkey=full")

def nmap_weak_keys(IP):
    subprocess.Popen(f"nmap -p 22 {IP} --script ssh-auth-methods --script-args='ssh.user=root'")



    