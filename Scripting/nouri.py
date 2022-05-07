import os
import json
import subprocess
from pathlib import Path
import argparse
import sys
import string
import re
# import iptools

global path
path = os.path.join('scans', 'filetemps') + '/'
os.system('mkdir -p ' + path + username)


with open(sys.argv[1]) as input_file:
    inp = input_file.readlines()
for i in inp:
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', i):
        os.system("nmap " + i.strip() + " -p- > nmap.txt")
        os.system("echo " + i.strip() + "|"+"httpx -ports xlarge  > httpx.txt")

    else:
        os.system("echo " + i.strip() + "|" +
                  "httpx -ports xlarge "+"|" + "nuclei -list httpx.txt > nuclei.txt")

    os.system("cat httpx.txt" + "|" +
              "aquatone -ports xlarge -out aquatone")


path1 = os.path.join('scans', 'temps', 'nmap.txt') + '/'
path2 = os.path.join('scans', 'temps', 'httpx.txt') + '/'
path3 = os.path.join('scans', 'temps', 'nuclei.txt') + '/'
path4 = os.path.join('scans', 'temps', 'aquatone') + '/'


port = int(input_file.readline())
host = input_file.readLines()


# in case the user entered a file containing subdomains:
content = input_file.read()
subdomains = content.splitlines()


HTTPX_CMD = "cat", input_file, "|", "httpx", "-o httpx.txt"
NUCLEI_CMD = "nuclei", "-list", input_nuclei


process = subprocess.Popen(
    HTTPX_CMD, '|', NUCLEI_CMD, stdout=open('final.txt', 'w+'))
input_nuclei = open("httpx.txt")
process = subprocess.Popen(
    HTTPX_CMD, '|', NUCLEI_CMD, stdout=open('final.txt', 'w+'))

output, err = process.communicate()
# print(json.dumps(output.decode( )))


# Get subdomains and check for HTTP responses
# cat input_file | subfinder | tee subdomains.txt | httpx | tee httpx.txt
# Brute force all subdomains
# cat httpx.txt | while read url
# do
# dirsearch.py - e php, aspx, asp, txt, bak - u $url | tee ./bruteforce /$url-dirsearch.txt
