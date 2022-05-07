import os
from os.path import exists
import subprocess
from pathlib import Path
from threading import Thread
import sys
import string
import re
from authentication.models import Scan

global ports

global services


def file_loc(filename, user):
    # define path where output files would be dumped or generated
    path = os.path.join(os.getcwd(), 'project') + '/'
    # creating folders corresponding each user.
    process = os.system('mkdir -p ' + path + "/" + user)


def httpx():
    # generating urls from user's input
    subprocess.Popen(['httpx -l '+sys.argv[1] + ' -o ' +
                     str(path) + ' httpx.txt'], shell=True)


def available_ports():
    # exploit ports on which services might be running
    os.system("naabu --iL " + sys.argv[1] + " -o " + "naabu.txt")
    fle = open("naabu.txt")
    target = {}
    for i in fle.readlines():
        try:
            target[i.split(":")[0]] = target[i.split(":")[0]] + \
                "," + i.split(":")[1]
        except:
            target[i.split(":")[0]] = i.split(":")[1]


def available_services():
    # manage running services
    for i in (target.keys()):
        # the keys function takes the IP addresses from the target dict as an arg
        subprocess.Popen(['nmap -sV -Pn ' + i + ' -p ' +
                          target[i] + ' -oG ' + str(path) + '/' + 'nmap'], shell=True)

    tab = {}

    # grep all strings that are placed between "//" "//" in the nmap input file (which refer to services)
    os.system("cat nmap | tr ",
              " "'\n'" | grep -Eo "'.*/'" | tr "':' " "'\n'" | grep -v Ports | cut -d '/' -f 1,5 > output.txt")
    with open("output.txt") as f:
        for i in f.readlines():
            try:
                tab[i.split("/")[0]] = tab[i.split("/")[0]] + \
                    "," + i.split("/")[1]
            except:
                tab[i.split("/")[0]] = i.split(":")[1]

    enum(**tab)


def http_scripts(**tab):
    for i in (tab.keys()):
        subprocess.Popen([
            'nmap -Pn -p '+i + ' -T4 --script http-methods, https-methods --script.args http-methods.test=all ' + domain + ' -oG http-methods'], shell=True)
        # find hidden files and directories using HTTP-enum script
        subprocess.Popen(["nmap -sV -p " + i +
                          " --script http-enum " + tab[i] + " -oG  http-enum"], shell=True)
        # firewalls
        os.system(
            "nmap -Pn -p " + i + " --script http-waf-detect, http-waf-fingerprint " + domain + " -oG http-waf")


def ftp_scripts(**tab):
    for i in (tab.keys()):
        os.system("sudo nmap -p " + i +
                  " -sS --script ftp-anon ,ftp-syst, tftp-enum , ftp-vsftp-backdoor " + tab[i] + " -oG ftp")


def dns_scripts():
    for i in (tab.keys()):
        os.system("nmap --script dns-zone-transfer --script-args dns-zone-transfer.server= " +
                  server+" ,dns-zone-transfer.port=53,dns-zonz-transfer.domain="+domain + " -oG dns")
        # bruteforcing using a domain list ( a wordlist that helps)
        os.system(
            "nmap --script dns-brute --script.args dns.brute.threads=5, dns.brute.hostlist=#path of the wordlist " + domain + " -oG dns-brute")


def smtp_scripts(**tab):
    for i in (tab.keys()):
        os.system(
            "sudo nmap -p " + i + " --script smtp-commands " + tab[i] + " -oG commands.txt")
        os.system(
            "sudo nmap -p "+i+" --script smtp-enum-users --script-args smtp-enum.users.methods={"+methods+"}" + tab[i] + " -oG enum-smtp-users")
        # try to bypass SMTP authentication
        os.system("nmap -p " + i +
                  " --script smtp-open-relay " + tab[i] + " -oG smtp-openrelay")

    # there are plenty of CVEs in nmap scripts that help us enumerate


def nbtscan(**tab):
    for i in (tab.keys()):
        if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', i):
            os.system("sudo nbtscan -v -r " + tab[i] + " > netbios.txt")


def smb_scripts(**tab):
    for i in (tab.keys()):
        os.system("sudo nmap -p " + i +
                  " --script smb-os-discovery " + tab[i] + " -oG smb-os-discovery")
        os.system("sudo nmap -p " + i +
                  " --script smb-enum-shares "+tab[i] + " -oG smb-enum-shares")
        # listing versions of smb
        os.system("sudo nmap -p " + i +
                  " --script smb-enum-shares "+tab[i] + " -oG smb-shares")
    # little vulnerability scan now that we know OS and version
        os.system(
            "sudo nmap -p " + i + " --script smb-double-pulsar-backdoor "+tab[i] + " -oG smb-double-pulsar")
    # exemple of the eternal blue exploit
        os.system("sudo nmap -p " + i +
                  " --script smb-vuln-ms17-010 "+tab[i] + " -oG smb-vuln-ms17")
    # searching for null sessions:
        os.system("smbclient -L " + i + " -oG smbclient")


def mysql_scripts(**tab):
    for i in (tab.keys()):
        os.system("nmap -p " + i + " --script mysql-info " +
                  tab[i] + " -oG mysql-info")
        os.system("nmap -p " + i + " --script mysql-enum " +
                  tab[i] + " -oG mysqlenum")
        os.system("nmap -p " + i +
                  "--script mysql-empty-password " + tab[i] + " -oG empty_pass")
        os.system(
            "nmap -p  " + i + " --script mysql-brute --script-args mysql-brute.threads=100 " + tab[i] + " -oG mysql_brute")


def content_discovery():
    if os.path.exists('httpx.txt'):
        os.system("python3 dirsearch.py -l httpx.txt -o dirsearch.txt")
    else:
        httpx()
    return 0


def screenshot():
    os.system("cat httpx.txt" + "|" +
              "aquatone -ports xlarge -out aquatone")

    path4 = os.path.join('scans', 'temps', 'aquatone') + '/'


def enum(**tab):

    for i in (tab.values()):
        if (i == 'http' | i == 'https'):
            content_discovery()
            screenshot()
            http_scripts(i, tab[i])

        elif i == 'ftp':
            ftp_scripts(i, tab[i])

        elif (i == 'dns' | i == 'domain'):
            dns_scripts(i, tab[i])

        elif i == 'smtp':
            smtp_scripts(i, tab[i])

        elif i == 'smb':
            smb_scripts(i, tab[i])

        elif i == 'mysql':
            mysql_scripts(i, tab[i])

    os.system("echo " + i.strip() + "|" +
              "httpx -ports xlarge "+"|" + "nuclei -list httpx.txt > " + str(path) + "/" + "nuclei.txt")


available_ports()
available_services()
