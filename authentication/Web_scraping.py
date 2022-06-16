# import libraries
import numpy as np
from bs4 import BeautifulSoup
import os
import glob
from collections import OrderedDict


tab: dict = {}
html_files = glob.glob('*.html',
                       recursive=True)
x = 0
for file in html_files:
    # specify the url
    with open(file, 'r') as html_file:
        content = html_file.read()
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(content, 'lxml')
    # Take out the <div> of name and get its value
    div1 = soup.find('table', class_="address-info-table")
    div2 = soup.find('table', class_="port-table data-table")
    with open("/mnt/c/Users/Nour Abdessalem/Desktop/abcd/templates/authentication/web_formatter.html", "a") as output_file:
        output_file.write(str(div1))
        output_file.write(str(div2))

        output_file.close

    # count <tr>

    for tr in soup.findAll('table')[2].findAll('tbody'):
        numbertr = tr.findAll('tr')
        print(tr)
        if (len(numbertr) > 1):
            try:
                tab[file.split("-")[0]] = tab[file.split("-")[0]
                                              ] + "," + file.split("-")[1].strip()
            except:
                tab[file.split("-")[0]] = file.split("-")[1].strip()

        for i in list(OrderedDict.fromkeys(tab.keys())):
            print(i)
            vulns = ['Anonymous', 'VULNERABLE', 'Exploitable',
                     'root', 'Valid credentials', 'salt']
            service_files = glob.glob(i+"*.html")
            new_result = list(OrderedDict.fromkeys(service_files))

        # print(new_result)

            for file in new_result:

                with open(file, 'r') as service_file:
                    for i in numbertr[len(numbertr) > 1]:
                        i = str(i)
                        print(i)
                        for j in vulns:
                            # print(j)
                            result = i.find(j)
                            if result > 0:
                                x = x + 1
                                with open('js.txt', "a") as outfile:
                                    outfile.write(str(x)+" ")
                                    outfile.close()
