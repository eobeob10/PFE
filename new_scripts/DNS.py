import os
import subprocess

def banner_grab(DNS):
    subprocess.Popen(f"dig version.bind CHAOS TXT @{DNS}")


def nmap_banner_grab(IP):
    subprocess.Popen(f"nmap --script dns-nsid {IP}")

def zone_transfer(IP):
    subprocess.Popen(f"dig axfr @{IP}")

def zone_transfer(IP, DOMAIN):
    subprocess.Popen(f"dig axfr @{IP}{ DOMAIN}")

def zone_transfer_fierce(IP, DOMAIN):
    subprocess.Popen("fierce --domain {DOMAIN} --dns-servers {IP}")

def dig_any_info(IP, DOMAIN):
    subprocess.Popen(f"dig ANY @{IP} {DOMAIN}")

def dig_regular_dns(IP, DOMAIN):
    subprocess.Popen(f"dig A @{IP} {DOMAIN}")

def dig_IPV6_dns(IP, DOMAIN):
    subprocess.Popen(f"dig AAAA @{IP} {DOMAIN}")

def dig_information(IP, DOMAIN):
    subprocess.Popen(f"dig TXT @{IP} {DOMAIN}")

def dig_emails(IP, DOMAIN):
    subprocess.Popen(f"dig MX @{IP} {DOMAIN}")

def dig_nameresolve_dns(IP, DOMAIN):
    subprocess.Popen(f"dig NS @{IP} {DOMAIN}")

def reverse_lookup(IP):
    subprocess.Popen(f"dig -x 192.168.0.2 @{IP}")

def reverse_lookup_IPV6(IP):
    subprocess.Popen(f"dig -x 2a00:1450:400c:c06::93 @{IP}")

def nslookup(IP):
    os.system(f"nslookup")
    os.system(f"127.0.0.1")
    os.system(f"{IP}")

def nmap_scripts(IP):
    subprocess.Popen(f"nmap -n --script '(default and *dns*) or fcrdns or dns-srv-enum or dns-random-txid or dns-random-srcport' {IP}")

def reverse_bf(IP):
    subprocess.Popen(f"dnsrecon -r 127.0.0.0/24 -n {IP}")
    subprocess.Popen(f"dnsrecon -r 127.0.1.0/24 -n {IP}")
    subprocess.Popen(f"dnsrecon -r {IP} -n {IP}")
    subprocess.Popen(f"dnsrecon -d active.htb -a -n {IP}")

def DNS_subdomain(IP, DOMAIN):
    subprocess.Popen(f"dnsrecon -D subdomains-1000.txt -d {DOMAIN} -n {IP}")
    subprocess.Popen(f"dnscan -d {DOMAIN} -r -w subdomains-1000.txt")

def bruteforce_IPV6(DOMAIN):
    subprocess.Popen(f"dnsdict6 -s -t {DOMAIN}")

def DNS_recursion_DDOS(IP):
    subprocess.Popen(f"dig google.com A @{IP}")