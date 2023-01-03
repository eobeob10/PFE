import os
import subprocess

def banner_grab(IP, PORT):
    os.system(f"nc -vn {IP} {PORT}")

def ssh_key(IP, PORT="22"):
    os.system(f"ssh-keyscan -t rsa {IP} -p {PORT}")

def nmap_default(IP, PORT="22"):
    subprocess.Popen(f"nmap -sC -sV -p {PORT} {IP}", shell=True)

def nmap_supported_algorithms(IP):
    subprocess.Popen(f"nmap -p 22 {IP} --script ssh2-enum-algos", shell=True)

def nmap_weak_keys(IP):
    subprocess.Popen(f"nmap -p 22 {IP} --script ssh-hostkey --script-args ssh_hostkey=full",shell=True)

def nmap_auth_methods(IP):
    subprocess.Popen(f"nmap -p 22 {IP} --script ssh-auth-methods --script-args='ssh.user=root'",shell=True)

def metasploit_juniper_backdoor(IP):
    subprocess.Popen(f"msfconsole -q -x 'use auxiliary/scanner/ssh/juniper_backdoor; set RHOSTS {IP}; set RPORT 22; run; exit'",shell=True)

def metasploit_ssh_enumusers(IP):
    subprocess.Popen(f"msfconsole -q -x 'use scanner/ssh/ssh_enumusers; set RHOSTS {IP}; set RPORT 22; run; exit' ",shell=True)

def metasploit_ssh_version(IP):
    subprocess.Popen(f"msfconsole -q -x 'use auxiliary/scanner/ssh/ssh_version; set RHOSTS {IP}; set RPORT 22; run; exit' ",shell=True)

    