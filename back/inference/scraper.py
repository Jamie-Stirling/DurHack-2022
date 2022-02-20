import urllib.request
from bs4 import BeautifulSoup
import numpy as np

districts = set()

for years in [2018, 2019, 2020, 2021]:
    with open("inference/data/pp-{}.csv".format(years)) as r:
        lines = [l for l in r.readlines()]
        for line in lines[:50]:
            spl = line.split(",")
            postcode = spl[3][1:-1]

            if postcode != "":
                district = postcode.split(" ")[0]
                districts.add(district)



districts = list(districts)
np.random.shuffle(districts)
for district in districts[:100]:
    url = "https://www.nestoria.co.uk/{}/property/buy".format(district.lower())
    fp = urllib.request.urlopen(url)

    mybytes = fp.read()
    html_doc =  mybytes.decode("utf8")

    fp.close()

    soup = BeautifulSoup(html_doc, 'html.parser')

    listings = [l for l in soup.find_all("li", {"class": "rating__new"})] + [l for l in soup.find_all("div", {"class": " rating__new"})]

    for listing in listings:
        try:
            rooms = listing.find("span", {"itemprop":"numberOfRooms"}).text
            price = listing.find("div", {"class":"result__details__price"}).text

            items = [i.text for i in listing.find_all("span", {"class":"summary-item"})][2:]
            line = rooms + "," + price + str(items)
        except Exception as e:
            pass
