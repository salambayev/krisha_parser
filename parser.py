import requests
from bs4 import BeautifulSoup
import json
import codecs
import os

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

	if (page.status_code == 200):
		soup = BeautifulSoup(page.content, 'html.parser')
		#print(soup.prettify())

		rmc = soup.find('div', class_='a-header company')
		if (rmc is None):
			rmc = soup.find('div', class_='a-header specialist')
			if (rmc is None):
				rmc = soup.find('div', class_='a-header owner')


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
	ans = "address: " + str(address) + "|" + " room_count: " + str(room_count) + "|" + " Жилой комплекс: " + str(map_complex) + "|" + " Дом: " + str(building) + "|" + "Время постройки: " + str(built_time) + "|" + " Этаж: " + str(floor) + "|" + " Площадь: " + str(space) + "|" + " Состояние: " + str(renovation) + "|" + " Санузел: " + str(toilet) + "|" + " Балкон: " + str(balcony) + "|" + " Балкон остеклен: " + str(balcony_glass) + "|" + " Дверь: " + str(door) + "|" + " Телефон: " + str(phone) + "|" + " Потолки: " + str(ceiling) + "|" + " Безопасноть: " + str(security) + "|" + " В прив. общежитии: " + str(priv_dorm) + "|" + " Интернет: " + str(internet) + "|" + " Мебель: " + str(furniture) + "|" + " Пол: " + str(flooring) + "|" + " Парковка: " + str(parking) + "\n"
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


def get_links(city):
	page_0 = "https://krisha.kz/prodazha/kvartiry/" + city + "/"
	temp_list = pulling_links(page_0)
	whole_links = []
	whole_links.extend(temp_list)
	cnt = len(temp_list)
	count = 2
	while (cnt < 34000):
		page = "https://krisha.kz/prodazha/kvartiry/" + city + "/?page=" + str(count)
		temp_list = pulling_links(page)
		#print(len(temp_list))
		whole_links.extend(temp_list)
		cnt = cnt + len(temp_list)
		count = count + 1
	for i in range(len(whole_links)):
		whole_links[i] = "https://krisha.kz" + whole_links[i]
	thefile = open('links.txt', 'w')
	for item in whole_links:
		thefile.write("%s\n" % item)
	thefile.close()


def save_data(data):
	cwd = os.getcwd()
	cwd = cwd + "/data.txt"
	if (os.path.isfile(cwd)):
		with codecs.open("data.txt", "a", "utf-8") as myfile:
			myfile.write(str(data))
	else:
		with codecs.open("data.txt", "w", "utf-8") as myfile:
			myfile.write(str(data))
		# json.dump(appartments, open(path, 'a'),encoding='utf8')
		# with codecs.open('data.txt', 'a', encoding='utf-8') as f:
		# 	json.dump(appartments, f, ensure_ascii=False)



def parse_and_save(first, second, whole_links):
	for i in range(first, second):
		temp_appart = parse_data(whole_links[i])
		if (temp_appart != 0):
			save_data(temp_appart)
		else:
			print("Found empty page: --> ", whole_links[i])

	with open("last_index.txt", "w") as myfile:
		myfile.write(str(second))
	return print("Parsing from {} to {} - succesfully! ", first, second)



def main():
	#get_links()
	thefile = open("links.txt", 'r')
	whole_links = thefile.readlines()

	cwd = os.getcwd()
	cwd = cwd + "/last_index.txt"
	if (os.path.isfile(cwd)):
		with open("last_index.txt", 'r') as myfile:
			last_index = myfile.read()
			if (last_index == ''):
				last_index = 0
	else:
		last_index = 0
	counting = int(len(whole_links)/10)
	print(counting)
	last_index = int(last_index)
	print(last_index)
	while(last_index < len(whole_links)):
		parse_and_save(last_index, last_index+counting, whole_links)
		last_index = last_index + counting


main()
