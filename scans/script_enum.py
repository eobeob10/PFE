import os
import json
import subprocess
from pathlib import Path
import argparse
import sys
import string
import re
# import iptools
global ports
global path
global services


cwd = os.path.join(os.getcwd(), 'filetemps') + '/'
path = os.system('mkdir -p ' + cwd + "nou")


def httpx():
    with open(sys.argv[1]) as input_file:
        os.system("httpx -l "+input_file + "-o " + str(path) + "httpx.txt")
    return 0


def available_ports():
    with open(sys.argv[1]) as input_file:
        os.system("naabu --iL " + sys.argv[1] + " -o " + "naabu.txt")
        # path + "/" + "naabu.txt")
        ports = os.system(
            "cat naabu.txt |  cut -d ':' -f 2  ")


def available_services():

    fle = open("naabu.txt")
    target = {}
    for i in fle.readlines():
        try:
            target[i.split(":")[0]] = target[i.split(":")[0]] + \
                "," + i.split(":")[1]
        except:
            target[i.split(":")[0]] = i.split(":")[1]

    for i in (target.keys()):

        os.system("nmap -sV -Pn " + i + " -p " + target[i] + " -oG " + "nmap")
        # str(path) + "/" +
    services = os.system('cat nmap | tr "," "\n" | grep -Eo "//.*//"')
    enum(services)

# file = open("services.txt")
    # service = file.read()


def http_scripts(i, p):
    os.system(
        "nmap -Pn -p "+target[i] + "-T4 --script http-methods, https-methods --script.args http-methods.test=all " + domain + "-oG http-methods")
    # find hidden files and directories using HTTP-enum script
    os.system("nmap -sV -p " + target[i] +
              " --script http-enum " + i.strip() + "-oG  http-enum")
    # firewalls
    os.system(
        "nmap -Pn -p " + p + "--script http-waf-detect, http-waf-fingerprint " + domain + "-oG http-waf")


def ftp_scripts(i, p):
    os.system("sudo nmap -p "+target[i] +
              "-sS --script ftp-anon ,ftp-syst, tftp-enum , ftp-vsftp-backdoor" + i.strip() + "-oG ftp")


def dns_scripts(i, p):
    os.system("nmap --script dns-zone-transfer --script-args dns-zone-transfer.server= " +
              server+" ,dns-zone-transfer.port=53,dns-zonz-transfer.domain="+domain + "-oG dns")
    # bruteforcing using a domain list ( a wordlist that helps)
    os.system(
        "nmap --script dns-brute --script.args dns.brute.threads=5, dns.brute.hostlist=#path of the wordlist " + domain + "-oG dns-brute")


def smtp_scripts(i, p):
    os.system(
        "sudo nmap -p " + target[i] + "--script smtp-commands" + i.strip() + "-oG commands.txt")
    os.system(
        "sudo nmap -p "+target[i]+" --script smtp-enum-users --script-args smtp-enum.users.methods={"+methods+"}" + i.split() + "-oG enum-smtp-users")
    # try to bypass SMTP authentication
    os.system("nmap -p " + target[i] +
              "--script smtp-open-relay " + i.strip() + "-oG smtp-openrelay")

    # there are plenty of CVEs in nmap scripts that help us enumerate


def nbtscan(i):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', i):
        os.system("sudo nbtscan -v -r " + i.strip() + "> netbios.txt")


def smb_scripts(i, p):
    os.system("sudo nmap -p" + p +
              "--script smb-os-discovery" + i.strip() + "-oG smb-os-discovery")
    os.system("sudo nmap -p" + p +
              "--script smb-enum-shares "+i.strip() + "-oG smb-enum-shares")
    # listing versions of smb
    os.system("sudo nmap -p" + p +
              "--script smb-enum-shares "+i.strip() + "-oG smb-shares")
    # little vulnerability scan now that we know OS and version
    os.system(
        "sudo nmap -p " + target[i] + "--script smb-double-pulsar-backdoor "+i.strip() + "-oG smb-double-pulsar")
    # exemple of the eternal blue exploit
    os.system("sudo nmap -p " + target[i] +
              "--script smb-vuln-ms17-010 "+i.strip() + "-oG smb-vuln-ms17")
    # searching for null sessions:
    os.system("smbclient -L " + i.strip() + "-oG smbclient")


def mysql_scripts(i, p):
    os.system("nmap -p " + target[i] + "--script mysql-info " +
              i.strip() + "-oG mysql-info")
    os.system("nmap -p " + target[i] + "--script mysql-enum " +
              i.strip() + "-oG mysqlenum")
    os.system("nmap -p " + target[i] +
              "--script mysql-empty-password " + i.strip() + "-oG empty_pass")
    os.system(
        "nmap -p  " + target[i] + "--script mysql-brute --script-args mysql-brute.threads=100 " + i.strip() + "-oG mysql_brute")


def content_discovery():
    os.system("python3 dirsearch.py -l httpx.txt -o dirsearch.txt")
    return 0


def screenshot():
    os.system("cat httpx.txt" + "|" +
              "aquatone -ports xlarge -out aquatone")

    path4 = os.path.join('scans', 'temps', 'aquatone') + '/'


def enum(services):

    if (http) in services:
        content_discovery()
        screenshot()
        http_scripts(i, p)

    elif 'ftp' in services:
        ftp_scripts(i, p)

    elif 'dns' in services or 'domain' in services:
        dns_scripts(i, p)

    elif 'smtp' in services:
        smtp_scripts(i, p)

    elif 'smb' in services:
        smb_scripts(i, p)

    elif 'mysql' in services:
        mysql_scripts(i, p)

    os.system("echo " + i.strip() + "|" +
              "httpx -ports xlarge "+"|" + "nuclei -list httpx.txt >" + str(path) + "/" + "nuclei.txt")


available_ports()
available_services()
