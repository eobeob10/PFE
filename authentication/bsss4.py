from bs4 import BeautifulSoup

# Fetch the page and create a Beautiful Soup object
page = open(r"nmap2.html").read()
soup = BeautifulSoup(page, "lxml")

# Get the raw text of first quote
quote_elem = soup.find("div", class_="address-info-table")
quote = quote_elem.find("h3")
quote_text = quote.get_text()
print(quote_text)
