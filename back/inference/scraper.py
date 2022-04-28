import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

districts = set()

# uses pandas to get the unique postcodes from the dataset
districts = list()

dataset = pd.read_csv("Uk_property_price_2021.csv")  

df = pd.DataFrame(dataset)

postcode_list = df['Postcode District'].tolist() # finds the list of all postcodes in the data set

for i in postcode_list: # makes sure that the postcodes are unique, don't want to find properties that you have already found
    if i not in districts:
        districts.append(i)

districts = list(districts)
np.random.shuffle(districts)
def process(item):
    return "".join(c for c in item.lower() if c in "0123456789abcdefghijklmnopqrstuvwxyz")
with open("data.csv", "w+") as writer:
    for district in districts[:100]:
        url = "https://www.nestoria.co.uk/{}/property/buy".format(district.lower())
        fp = urllib.request.urlopen(url)

        mybytes = fp.read()
        html_doc =  mybytes.decode("utf8")

        fp.close()

        print(html_doc)

        soup = BeautifulSoup(html_doc, 'html.parser')

        listings = [l for l in soup.find_all("li", {"class": "rating__new"})] + [l for l in soup.find_all("div", {"class": " rating__new"})]

        for listing in listings:
            try:
                rooms = process(listing.find("span", {"itemprop":"numberOfRooms"}).text)
                price = process(listing.find("div", {"class":"result__details__price"}).text)

                items = [i.text for i in listing.find_all("span", {"class":"summary-item"})][2:]
                line = price + "," + rooms + "," + ",".join([process(item) for item in items]) + "\n"
                
                writer.write(line)
            except Exception as e:
                print(e)
                pass
