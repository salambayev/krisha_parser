from bs4 import BeautifulSoup
import requests
import re

link = "https://krisha.kz/a/show/25994402"
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')

pattern = re.compile(r'"lat":')
text = soup.find('script', text=pattern)
latitude = 0.0
longitude = 0.0
if (text != None):
    all_script_text = text.string
    lat = re.search('"lat":(.+?),"lon":', all_script_text)
    if lat:
        latitude = lat.group(1)

    lon = re.search('"lon":(.+?),"zoom"', all_script_text)
    if lon:
        longitude = lon.group(1)


print(latitude)
print(longitude)
