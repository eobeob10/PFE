from asyncio import subprocess
import os
from re import sub
import subprocess

def nikto(IP, PORT = "80"): 
    subprocess.Popen('echo n | nikto -nointeractive -maxtime 45m -timeout 60 -host {IP}:{PORT} -Plugins "paths;outdated;report_sqlg;auth;content_search;report_text;fileops;parked;shellshock;report_html;cgi;headers;report_nbe;favicon;cookies;robots;report_xml;report_csv;ms10_070;msgs;drupal;apache_expect_xss;siebel;put_del_test;apacheusers;dictionary;embedded;ssl;clientaccesspolicy;httpoptions;subdomain;negotiate;sitefiles;mutiple_index;strutshock;dishwasher;paths;docker_registry;origin_reflection;dir_traversal;multiple_index"', shell = True)

def whatweb(IP, PORT="80"):
    subprocess.Popen("whatweb -a 3 {IP}:{PORT}", shell=True)

def robots(IP, PORT="80"):
    print("Grabbing Robots.txt")
    subprocess.Popen("curl {IP}:{PORt}/robots.txt -L -k --user-agent 'Googlebot/2.1 (+http://www.google.com/bot.html)' --connect-timeout 30 --max-time 180", shell=True)


def nmap(IP, PORT = "80"):
    subprocess.Popen(f'nmap -n -sV --script "(http* and not (dos or brute) and not http-xssed))" -p {PORT} {IP}',shell=True)

def wafw00f(IP, PORT = "80"):
    subprocess.Popen(f"wafw00f {IP}:{PORT}", shell=True)

def dirsearch(IP, PORT = "80", path = "/", extensions="php,html,sh,txt"):
    subprocess.Popen(f"dirsearch -F -r -u {IP}:{PORT}{path} -e {extensions}",shell=True)

def dirhunt(IP, PORT = "80", path="/"):
    subprocess.Popen(f"dirhunt {IP}:{PORT}{path}", shell=True)

def gobuster(IP, PORT = "80", path="/", extensions="php,html,sh,txt", wordlist="/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"):
    subprocess.Popen(f"gobuster -k -fw -w {wordlist} -u {IP}:{PORT}{path} -e {extensions}", shell=True)

# could do dirb too

def csmap(IP, PORT = "80", path="/"):
    subprocess.Popen(f'echo "y" | cmsmap -s {IP}:{PORT}{path}',shell=True)

def curl_put(IP, PORT="80", path="/"):
    subprocess.Popen(f'curl -v -X PUT -d "PUT PUT PUT" {IP}:{PORT}{path}/legion.txt',shell=True)

def gobuster_vhosts(IP,wordlist, PORT="80"):
    subprocess.Popen(f'gobuster vhost -u "{IP}:{PORT}" -t 50 -w {wordlist}', shell=True)


# HTTPS :

def https_sslscan(IP, PORT="443"):
    subprocess.Popen(f'sslscan {IP}:{PORT}', shell=True)





