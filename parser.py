import requests
from bs4 import BeautifulSoup
import json
import codecs
import os
import re

def parse_data(krisha_link):
	page = requests.get(krisha_link)
	#200 - page loaded succesfully
	#print(page.content)
	room_count = -1
	address = -1
	map_complex = -1
	building = -1
	built_time = -1
	floor = -1
	space = -1
	renovation = -1
	toilet = -1
	balcony = -1
	door = -1
	phone = -1
	ceiling = -1
	security = -1
	priv_dorm = -1
	internet = -1
	furniture = -1
	flooring = -1
	balcony_glass = -1
	parking = -1
	price = -1
	region = -1
	longitude = 0.0
	latitude = 0.0

	if (page.status_code == 200):
		soup = BeautifulSoup(page.content, 'html.parser')
		#print(soup.prettify())

		rmc = soup.find('div', class_='a-header company')
		if (rmc is None):
			rmc = soup.find('div', class_='a-header specialist')
			if (rmc is None):
				rmc = soup.find('div', class_='a-header owner')

		pattern = re.compile(r'"lat":')
		script_text = soup.find('script', text=pattern)
		if (script_text != None):
			all_script_text = script_text.string
			lat = re.search('"lat":(.+?),"lon":', all_script_text)
			if lat:
			    latitude = lat.group(1)

			lon = re.search('"lon":(.+?),"zoom"', all_script_text)
			if lon:
			    longitude = lon.group(1)

		district = soup.find('div', class_='a-where-region')
		district = district.text
		print(district)

		room_count = rmc.h1.text[0]
		address = rmc.h1.text[21:]
		print(room_count)
		print(address)

		dt = soup.find_all('dt')
		dd = soup.find_all('dd')
		for i in range(len(dt)):
			if (dt[i].text == "Жилой комплекс"):
				map_complex = dd[i].text
			elif (dt[i].text == "Дом"):
				home = dd[i].text
				divider = home.split(',')
				if "г.п." in divider[0]:
					built_time = divider[0]
					building = -1
				else:
					building = divider[0]
					built_time = divider[1]
			elif (dt[i].text == "Этаж"):
				floor = dd[i].text
			elif (dt[i].text == "Площадь"):
				living_space = dd[i].text
				d_space = living_space.split(',')
				space = d_space[0]
			elif (dt[i].text == "Состояние"):
				renovation = dd[i].text
			elif (dt[i].text == "Санузел"):
				toilet = dd[i].text
			elif (dt[i].text == "Балкон"):
				balcony = dd[i].text
			elif (dt[i].text == "Дверь"):
				door = dd[i].text
			elif (dt[i].text == "Телефон"):
				phone = dd[i].text
			elif (dt[i].text == "Потолки"):
				ceiling = dd[i].text
			elif (dt[i].text == "Безопасноть"):
				security = dd[i].text
			elif (dt[i].text == "В прив. общежитии"):
				priv_dorm = dd[i].text
			elif (dt[i].text == "Интернет"):
				internet = dd[i].text
			elif (dt[i].text == "Мебель"):
				furniture = dd[i].text
			elif (dt[i].text == "Пол"):
				flooring = dd[i].text
			elif (dt[i].text == "Балкон остеклен"):
				balcony_glass = dd[i].text
			elif (dt[i].text == "Парковка"):
				parking = dd[i].text

		price = soup.find('span', class_='price').text
		region = soup.find('div', class_='a-where-region').string
	else:
		print("Failed to load page: --> ", krisha_link)
		return 0
	ans = "district:" + str(district) + "|" + "address: " + str(address) + "|" + " room_count: " + str(room_count) + "|" + " price: " + str(price) + "|" + " Жилой комплекс: " + str(map_complex) + "|" + " Дом: " + str(building) + "|" + "Время постройки: " + str(built_time) + "|" + " Этаж: " + str(floor) + "|" + " Площадь: " + str(space) + "|" + " Состояние: " + str(renovation) + "|" + " Санузел: " + str(toilet) + "|" + " Балкон: " + str(balcony) + "|" + " Балкон остеклен: " + str(balcony_glass) + "|" + " Дверь: " + str(door) + "|" + " Телефон: " + str(phone) + "|" + " Потолки: " + str(ceiling) + "|" + " Безопасноть: " + str(security) + "|" + " В прив. общежитии: " + str(priv_dorm) + "|" + " Интернет: " + str(internet) + "|" + " Мебель: " + str(furniture) + "|" + " Пол: " + str(flooring) + "|" + " Парковка: " + str(parking) + "|" + " Latitude: " + str(latitude) + "|" + " Longitude: " + str(longitude) + "\n"
	return ans


def pulling_links(page):
	page = requests.get(page)
	links = []
	if (page.status_code == 200):
		soup = BeautifulSoup(page.content, 'html.parser')
		data = soup.find_all('div', class_='a-title')
		for div in data:
			links.append(div.a['href'])
	return links


def get_count(link):
	page = requests.get(link)
	if (page.status_code == 200):
		count_soup = BeautifulSoup(page.content, 'html.parser')
		cnt = count_soup.find('div', class_ = 'a-search-subtitle search-results-nb')
		count = cnt.span.text
		count = count.replace(u'\xa0', '')
		count = int(count)
	else:
		count = 0
	return count


def get_links(city, links_count):
	page_0 = "https://krisha.kz/prodazha/kvartiry/" + city + "/"
	temp_list = pulling_links(page_0)
	temp_list = normalizing_links(city, temp_list)
	save_links(city, temp_list)
	cnt = len(temp_list)
	count = 2
	while (cnt <= links_count):
		page = "https://krisha.kz/prodazha/kvartiry/" + city + "/?page=" + str(count)
		temp_list = pulling_links(page)
		temp_list = normalizing_links(city, temp_list)
		save_links(city, temp_list)
		cnt = cnt + len(temp_list)
		count = count + 1

	return "Links of : " + city + " pulled succesfully! "


def normalizing_links(city, temp_list):
	for i in range(len(temp_list)):
		temp_list[i] = "https://krisha.kz" + temp_list[i] + " | " + city
	return temp_list


def save_links(city, links_data):
	cwd = os.getcwd()
	cwd = cwd + "/links_" + city + ".txt"
	truepath = "links_" + city + ".txt"
	if (os.path.isfile(cwd)):
		with codecs.open(truepath, "a", "utf-8") as myfile:
			for i in range(len(links_data)):
				myfile.write(str(links_data[i]) + "\n")
	else:
		with codecs.open(truepath, "w", "utf-8") as myfile:
			for i in range(len(links_data)):
				myfile.write(str(links_data[i]) + "\n")


def save_data(city, data):
	cwd = os.getcwd()
	cwd = cwd + "/data_" + city + ".txt"
	truepath = "data_" + city + ".txt"
	if (os.path.isfile(cwd)):
		with codecs.open(truepath, "a", "utf-8") as myfile:
			myfile.write(str(data))
	else:
		with codecs.open(truepath, "w", "utf-8") as myfile:
			myfile.write(str(data))


def log(text):
	cwd = os.getcwd()
	cwd = cwd + "/logs.txt"
	if (os.path.isfile(cwd)):
		with codecs.open("logs.txt", "a", "utf-8") as myfile:
			myfile.write(str(text))
	else:
		with codecs.open("logs.txt", "w", "utf-8") as myfile:
			myfile.write(str(text))


def parse_and_save(city, first, second, whole_links):
	for i in range(first, second):
		temp_appart = parse_data(whole_links[i])
		if (temp_appart != 0):
			save_data(city, temp_appart)
		else:
			log("Found empty page: --> " + "City: " + city + " " + whole_links[i])

	with open("last_index.txt", "w") as myfile:
		myfile.write(str(second))
	return log("City: " + city + "Parsing from " + first + " to " + second + " - succesfully!" )


def cities():
	cts = ["almaty", "astana", "akmolinskaja-oblast", "aktjubinskaja-oblast", "almatinskaja-oblast",
			"atyrauskaja-oblast", "vostochno-kazahstanskaja-oblast", "zhambylskaja-oblast", "zapadno-kazahstanskaja-oblast",
			"karagandinskaja-oblast", "kostanajskaja-oblast", "kyzylordinskaja-oblast", "mangistauskaja-oblast", "pavlodarskaja-oblast", "severo-kazahstanskaja-oblast",
			"juzhno-kazahstanskaja-oblast"]
	for i in range(len(cts)):
		links_count = get_count("https://krisha.kz/prodazha/kvartiry/" + cts[i] + "/")
		log(get_links(cts[i], links_count))
		thefile = open("links_" + cts[i] + ".txt", 'r')
		whole_links = thefile.readlines()

		cwd = os.getcwd()
		cwd = cwd + "/last_index_" + cts[i] + ".txt"
		truefile = "last_index_" + cts[i] + ".txt"
		if (os.path.isfile(cwd)):
			with open(truefile, 'r') as myfile:
				last_index = myfile.read()
				if (last_index == ''):
					last_index = 0
		else:
			last_index = 0
		counting = int(len(whole_links)/10)
		log(str(counting) + " in " + cts[i])
		last_index = int(last_index)
		while(last_index < len(whole_links)):
			parse_and_save(cts[i], last_index, last_index + counting, whole_links)
			last_index = last_index + counting

		with open(truefile, 'w') as myfile:
			myfile.write(str(0))



def main():
	cities()


main()
