import nmap
import sys


class Network_enum():
    def __init__(self):
        dgate = input("Enter IPv4 default gateway :")
        subnet = int(input("Enter the subnet mask :"))
        self.dgate = dgate
        self.subnet = subnet

    def host_discovery(self):
        if len(self.dgate) > 15 or self.subnet >= 32:
            sys.exit(0)
        else:
            network = self.dgate + "/" + str(self.subnet)
            print("+ Scanning network for available hosts +")

            # nmap object
            nm = nmap.PortScanner()

            # scanning network for hosts "sn" argument is the nmap option used to perform a scan
            nm.scan(hosts=network, arguments="sn")

            # using list comprehension to output available hosts on the network
            available_hosts = [(host, nm[host]["status"]["state"])
                               for host in nm.all_hosts()]

            for host, status in available_hosts:
                print(f"Hosts\t{host}")


if __name__ == "__main__":
    scan = Network_enum()
    scan.host_discovery()
