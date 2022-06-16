
import os
from os.path import exists
import subprocess
from pathlib import Path
from threading import Thread
import sys
import string
import ipaddress
import time
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")
global ports
global path
global path_to_wordlist

path_to_wordlist = '/mnt/c/Users/Nour Abdessalem/Desktop/baha/curated.txt'

# define path where output files would be dumped or generated
path = os.path.join(os.getcwd(), 'project') + '/'
# creating folders corresponding each user.
print(sys.argv[2])
print(sys.argv[3])

process = os.system('mkdir -p ' + path + "/" + sys.argv[2] + "/" + sys.argv[3])


def available_ports():
    # identify ports on which services might be running
    nox = subprocess.Popen(
        ['naabu', '-iL', sys.argv[1], '-o', 'naabu.txt'])
    nox.wait()
    print("++++++++++ running naabu")

    subprocess.Popen['grep ', ' -o ',
                     " '[0-9]\{1, 3\}\.[0-9]\{1, 3\}\.[0-9]\{1, 3\}\.[0-9]\{1, 3\}'", sys.argv[1],  '> IPs.txt ']

    # subprocess.Popen['nrich', 'IPs.txt ', '-o ', '>' ' nrich.txt']

    file1 = open('naabu.txt')
    # file2 = open('nrich.txt')

    target = {}
    tab = {}
    for i in (file1.readlines()):  # () & file2.readlines()):
        try:
            target[i.split(":")[0]] = target[i.split(":")[0]] + \
                "," + i.split(":")[1].strip()
        except:
            target[i.split(":")[0]] = i.split(":")[1].strip()

    # manage running services
    for i in (target.keys()):
        # the keys function takes the IP addresses from the target dict as an arg
        print(target[i])
        # print('nmap ' + '-sV' + ' -Pn ' + i + ' -p ' +
        # target[i] + ' -oG ' + 'nmap')
        subprocess.Popen(['nmap', '-sV', '-Pn ', i, '-p',
                          target[i], '-oG', 'nmap_'+target[i]+'.txt']).wait()

        #subprocess.Popen(['nmapAutomator/nmapAutomator.sh ', i, '-t port'])
        # grep all strings that are placed between "//" "//" in the nmap input file (which refer to services)

        os.system(
            "cat nmap |tr ','  '\n' | grep -Eo ' .*/' | tr ':'  '\n' | grep -v Ports | cut -d '/' -f '1,5' > output.txt")
        with open("output.txt") as f:
            for j in f.readlines():
                try:
                    tab[i] = tab[i] + ',' + j.split("/")[1].strip()
                except:
                    tab[i] = j.split("/")[1].strip()

    enum(tab, target)


def httpx():
    print("++++++++++ running httpx")
    # generating urls from user's input
    subprocess.Popen(['httpx', '-l', sys.argv[1],
                      '-o', 'httpx.txt'])
    # for i in open('httpx.txt').readlines():
    # subprocess.Popen(['echo', i, '|', 'python3', 'Astra.py',
    # '-ns', '|' ' tee ',  ' astra_urls.txt'], shell=True)


def special_module_for_scanning_all_subdomains_using_ffuf(asset):
    os.system('')


def http_scripts(asset, port):
    print("++++++++++ running http")
    subprocess.Popen([
        'nmap -Pn -p ', port, ' -T4 --script http-methods --script-args http-methods.test=all ', asset, ' -oX http-methods-', asset, '-', port, '.xml'], shell=True)
    # , '|', 'nmap-formatter', 'html', 'http-methods-', asset, '-', port, '.xml']
    subprocess.Popen(["nmap -Pn -p ", port,
                      " --script http-enum ", asset, " -oX  http-enum-", asset, '-'+port+'.xml'], shell=True)
    # firewalls
    os.system(
        "nmap -Pn -p " + port + " --script http-waf-detect, http-waf-fingerprint " + asset + " -oX http-waf-"+asset+'-'+port+'.xml')
    # vulnerable heartbleed
    subprocess.Popen(['nmap ', '-sS ', '-sV ', '-p ', port, ' --script=ssl-heartbleed',
                      asset, ' -oX heartbleed-', asset, '-', port, '.xml'], shell=True)
    # nikto
    os.system(" nikto -h " + asset + "> nikto-"+asset+'-'+port+'.txt')
    os.system("  nikto -h http://" +
              asset+":"+port + " | tee nikto"+asset+'-'+port+'.txt')
    # gobuster
    os.system("gobuster -u http://"+asset +
              " -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt -t 150 -l | tee " + asset+"-gobuster"+'-'+port+'.txt')
    # wpscan
    os.system("wpscan --url http://"+asset +
              ":"+port + " --enumerate u,t,p | tee "+asset+"-wpscan-enum"+'-'+port+'.txt')
    # CVE-2021-44228 - Apache Log4j RCE Scanner
    subprocess.Popen(['python3 ', ' log4j.py ',
                     '-l ', ' httpx.txt', '>log4j.txt'])


def ftp_scripts(asset, port):
    print("++++++++++ running ftp")
    os.system("nmap -p " + port +
              " -sS --script ftp-anon,ftp-syst, tftp-enum,ftp-vsftpd-backdoor" + asset + " -oX ftp"+asset+'-'+port+'.xml')
    os.system("searchsploit vsftpd > vsftpd.txt")
    with open("ftp"+asset+'-'+port+'.xml') as f:
        version = os.system(" cat vsftpd.txt | grep version | cut -d ' ' -f 3")
        if version in open("vsftpd.txt"):
            os.system('msfconsole')

        elif 'root' in f.readlines():
            t = tube()
            r = remote(asset, port)
            t.recvuntil(b'Name('+asset+':root)')
            r.sendline("anonymous")
            r.interactive()
            t.recvuntil(b'Using binary node to transfer files')
            r.sendline("dir")
            r.recvline()
            r.close()


def dns_scripts(asset, port):
    print("++++++++++ running dns")
    # with the host command we can specify the type of information we are looking for, '-t ns' is for name server particularity,  that helps us tell what dns provider is
    # used (eg: cloudflare), what type of instructure , '-t ms' for enumerating mail server or even reverse-lookup
    os.system("host " + sys.argv[1] + ' >host.txt')
    os.system("nmap --script dns-zone-transfer --script-args dns-zone-transfer.server= " +
              server+" ,dns-zone-transfer.port="+port+",dns-zone-transfer.domain="+asset + " -oX dns.xml")
    # bruteforcing using a domain list ( a wordlist that helps)
    os.system(
        "nmap --script dns-brute --script.args dns.brute.threads=5, dns.brute.hostlist=#path of the wordlist " + asset + " -oX dns-brute.xml")


def smtp_scripts(asset, port):
    print("++++++++++ running smtp")
    os.system(
        "nmap -p " + port + " --script smtp-commands " + asset + " -oG SMTP-commands.txt")
    os.system(
        "nmap -p "+port+" --script smtp-enum-users --script-args smtp-enum.users.methods={VRFY} " + asset + " -oG enum-smtp-users.txt")
    # try to bypass SMTP authentication
    os.system("nmap -p " + port +
              " --script smtp-open-relay " + asset + " -oG smtp-openrelay.txt")
    # there are plenty of CVEs in nmap scripts that help us enumerate
    os.system(
        "sudo nmap -p " + port + " --script smtp-vuln-cve2010-4344 " + asset + " -oG cve2010-4344.txt")
    os.system(
        "sudo nmap -p " + port + " --script smtp-vuln-cve2011-1720 " + asset + " -oG cve2011-1720.txt")


def rpc(asset, port):
    os.system("rpcinfo -p " + asset + " >rpcinfo.txt")
    # null sessions:
    os.system("rpcclient -U """ + asset + " >rpcclient.txt")


def kerberos_scripts(asset, port):
    os.system("nmap "+asset + "-p " + port +
              "--script krb5-enum-users --script-args krb5-enum-users.realm='test'  -oG enum-krb5-users.txt")


def nbtscan(asset):
    print("++++++++++ running nbtscan")
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', asset):
        os.system("sudo nbtscan -v -r " + asset + " > netbios-"+asset+".txt")


def smb_scripts(asset, port):
    print("++++++++++ running smb")
    os.system("sudo nmap -p " + port +
              " --script smb-os-discovery " + asset + " -oX smb-os-discovery.xml")

    # listing versions of smb
    os.system("sudo nmap -p " + port +
              " --script smb-enum-shares "+asset + " -oG smb-shares.txt")
    # little vulnerability scan now that we know OS and version
    os.system(
        "sudo nmap -p " + port + " --script smb-double-pulsar-backdoor "+asset + " -oG smb-double-pulsar"+asset+port+".txt")
    # exemple of the eternal blue exploit
    os.system("sudo nmap -p " + port +
              " --script smb-vuln-ms17-010 "+asset + " -oX smb-vuln-ms17.xml")
    # searching for null sessions:
    os.system("smbclient -L " + port + " -oG smbclient"+port+".txt")
    # List shares:
    os.system("smbclient -L "+asset+" -U  " " > smbclient"+asset+".txt")
    # enumerating targets using cme
    subprocess.Popen(['cme ', 'smb ', asset, ' >cme.txt'], shell=True)


def mysql_scripts(asset, port):
    print("++++++++++ running mysql")
    os.system("nmap -p " + port + " --script mysql-info " +
              asset + " -oG mysql-info.txt")
    os.system("nmap -p " + port + " --script mysql-enum " +
              asset + " -oG mysqlenum.txt")
    # essentialy checks if the accounts on the system have a null password so we can gain anonymous access.
    os.system("nmap -p " + port +
              "--script mysql-empty-password " + asset + " -oX mysql-"+asset+"-empty_pass.xml")
    os.system(
        "nmap -p  " + port + " --script mysql-brute --script-args mysql-brute.threads=100 " + asset + " -oX mysql-"+asset+"-mysql_brute.xml")


def content_discovery():
    print("++running discovery++")
    httpx()
    os.system("python3 dirsearch.py -l httpx.txt -o dirsearch.txt")
    subprocess.Popen['fuff', '-c', '-w', path_to_wordlist,
                     '-u ', ' httpx.txt ', 'astra_urls.txt '  ' -o ', ' ffuf.txt']
    return 0


def nrich():
    subprocess.Popen['grep -o ',
                     '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}', 'IPs.txt']


def banner_grabbing(asset, port):
    os.system("nc -v " + asset + " " + port + " >nc"+port+asset+".txt")
    os.system("telnet " + asset + " " + port + " >telnet"+port+asset+".txt")
    os.system("curl -vX" + asset + " >curl_results.txt")


def network_file_system_share(asset):
    os.system("showmount -e " + asset + " >nfs.txt")


def sn1per(asset):
    os.system("sudo sniper -t " + asset + " >sn1per.txt")


def screenshot():
    print("++++++++++ running screenshot")
    os.system("cat httpx.txt" + "|" +
              "aquatone -ports xlarge -out aquatone")


def active_directory():
    with open('IPs.txt') as f:
        IP = f.readlines()
    subprocess.Popen(['./linWinPwn.sh ', ' -t ', IP,
                     ' -o ', path, 'linWinPwn', IP])


def nuclei(asset):
    print("++++++++++ running nuclei")
    os.system("sudo nuclei -u " + asset + "> " +
              path + " / nuclei-"+asset + ".txt")


def enum(tab, target):
    for i in (target.keys()):
        for j in (tab.values()):
            if ('http' in tab[i]):
                content_discovery()
                screenshot()
                http_scripts(i, target[i])

            elif ('ftp' in tab[i]):
                ftp_scripts(i, tab[i])

            elif ('dns' in tab[i] or 'domain' in tab[i]):
                dns_scripts(i, tab[i])

            elif('netbios' in tab[i]):
                nbtscan(i)

            elif ('kerberos' in tab[i]):
                kerberos_scripts(i, tab[i])

            elif ('rpc' in tab[i]):
                rpc(i, tab[i])

            elif ('nfs' in tab[i]):
                network_file_system_share(i, tab[i])

            elif ('smtp' in tab[i]):
                smtp_scripts(i, tab[i])

            elif ('smb' in tab[i]):
                smb_scripts(i, tab[i])

            elif ('mysql' in tab[i]):
                mysql_scripts(i, tab[i])

            banner_grabbing(i, tab[i])

        # sn1per(i)
            nuclei(i)

        end = time.time()


available_ports()
