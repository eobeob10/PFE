from multiprocessing import connection
import os
import subprocess
import ldap3


def setserver(server1, port1 = 636):
    server = ldap3.Server(server1, get_info = ldap3.ALL, port = port1, use_ssl = True)
    connection = ldap3.Connection(server)
    connection.bind()
    server.info()
    connection.search(search_base='DC=DOMAIN,DC=DOMAIN', search_filter='(&(objectClass=*))', search_scope='SUBTREE', attributes='*')
    connection.entries
    connection.search(search_base='DC=DOMAIN,DC=DOMAIN', search_filter='(&(objectClass=person))', search_scope='SUBTREE', attributes='userPassword')
    connection.entries

def nmap_and_not_brute(IP):
    subprocess.Popen(f"nmap -n -sV --script 'ldap* and not brute' {IP}", shell=True)