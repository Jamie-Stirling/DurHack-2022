import urllib.request
import urllib.parse


url = 'https://api.nestoria.co.uk/api?encoding=json&pretty=1&action=search_listings&country=uk&listing_type=buy&place_name=brighton'
f = urllib.request.urlopen(url)
print(f.read().decode('utf-8'))