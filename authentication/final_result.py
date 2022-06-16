import glob
import os
from pathlib import Path


def nmap_formatter():
    read_files = glob.glob("*.xml")
    print(read_files)
    for file in read_files:
        try:
            cmd = 'cat ' + file + ' | ' + 'nmap-formatter ' + \
                'html ' + file + ' > ' + file.replace('xml', 'html')
            os.system(cmd)

        except EOFError as e:
            print("Ignored:", e)
            answer = None


def txt_formatter():
    read_files = glob.glob("*.txt")
    with open('final_result.txt', "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


def service_files():
    list_http = ['nikto', 'gobuster', 'wpscan', 'log4j', 'dirsearch']
    files = glob.glob('*.txt')
    for file in files:
        base = os.path.basename(file)

        name = str(os.path.splitext(base)[0])
        print(name)
        if name in list_http:
            with open('http_results.txt', "a") as outfile:
                with open(file, "rb") as infile:
                    outfile.write(str(infile.read()))
                    print("write https_results succ")
        elif name in 'rpc ':
            with open('rpc_results.txt', "a") as outfile:
                with open(file, "rb") as infile:
                    outfile.write(str(infile.read()))
                    print("write rpc succ")
        elif name in 'netbios':
            with open('netbios_results.txt', "a") as outfile:
                with open(file, "rb") as infile:
                    outfile.write(str(infile.read()))
                    print("write nb succ")
        elif name in 'smb':
            with open('smb_results.txt', "a") as outfile:
                with open(file, "rb") as infile:
                    outfile.write(str(infile.read()))
                    print("write smb succ")


service_files()


# filtrer selon Anonymmous login successful (smb)
