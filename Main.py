import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
import pickle
import requests
import json


class HousePricing():
    def yandex_geocoder(location):
        url = "https://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + " алматы " + location + "&lang=en-US"
        yandex = requests.get(url = url)
        data = json.loads(yandex.text)
        if (data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != "0"):
            print(data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"])
            point = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        else:
            print("Not found")
            point = "0.0 0.0"

        geo = point.split(" ")
        latitude = geo[1]
        longitude = geo[0]
        return latitude, longitude



    def normalization(self, data):
        to_model = data.split("|")
        columns = ['room_number', 'house_type_иное', 'house_type_каркасно-камышитовый',
                   'house_type_кирпичный', 'house_type_монолитный',
                   'house_type_панельный', 'state_евроремонт', 'state_свободная планировка',
                   'state_среднее', 'state_требует ремонта', 'state_хорошее',
                   'state_черновая отделка', 'region_Алматы, Алатауский р-н',
                   'region_Алматы, Алмалинский р-н', 'region_Алматы, Ауэзовский р-н',
                   'region_Алматы, Бостандыкский р-н', 'region_Алматы, Жетысуйский р-н',
                   'region_Алматы, Жетысуский р-н', 'region_Алматы, Медеуский р-н',
                   'region_Алматы, Наурызбайский р-н', 'region_Алматы, Турксибский р-н',
                   'region_Казахстан', 'internet_0', 'internet_ADSL', 'internet_оптика', 'internet_проводной',
                   'internet_через TV кабель', 'bathroom_2 с/у и более', 'bathroom_нет',
                   'bathroom_раздельный', 'bathroom_совмещенный', 'built_time', 'all_space', 'balcony',
                   'phone', 'parking', 'furniture', 'at_the_hostel',
                   'appartments_floor', 'building_floors', 'price_for_sqr_meter',
                   'trngl_first_point', 'trngl_second_point', 'trngl_third_point']
        temp = {'room_number': to_model[0], 'house_type_иное': '0', 'house_type_каркасно-камышитовый': '0',
                'house_type_кирпичный': '0', 'house_type_монолитный': '0', 'house_type_панельный': '0',
                'state_евроремонт': '0', 'state_свободная планировка': '0', 'state_среднее': '0',
                'state_требует ремонта': '0', 'state_хорошее': '0', 'state_черновая отделка': '0',
                'region_Алматы, Алатауский р-н': '0', 'region_Алматы, Алмалинский р-н': '0',
                'region_Алматы, Ауэзовский р-н': '0', 'region_Алматы, Бостандыкский р-н': '0',
                'region_Алматы, Жетысуйский р-н': '0', 'region_Алматы, Жетысуский р-н': '0',
                'region_Алматы, Медеуский р-н': '0', 'region_Алматы, Наурызбайский р-н': '0',
                'region_Алматы, Турксибский р-н': '0', 'region_Казахстан': '0', 'internet_0': '0', 'internet_ADSL': '0',
                'internet_оптика': '0', 'internet_проводной': '0', 'internet_через TV кабель': '0',
                'bathroom_2 с/у и более': '0', 'bathroom_нет': '0', 'bathroom_раздельный': '0',
                'bathroom_совмещенный': '0', 'built_time': '0', 'all_space': '0', 'balcony': '0', 'phone': '0',
                'parking': '0', 'furniture': '0', 'at_the_hostel': '0', 'appartments_floor': '0', 'building_floors': '0',
                'trngl_first_point': '0', 'trngl_second_point': '0', 'trngl_third_point': '0'}
        if (to_model[1] in "house_type_иное"):
            temp['house_type_иное'] = 1
        elif (to_model[1] in "house_type_каркасно-камышитовый"):
            temp['house_type_каркасно-камышитовый'] = 1
        elif (to_model[1] in "house_type_кирпичный"):
            temp['house_type_кирпичный'] = 1
        elif (to_model[1] in "house_type_монолитный"):
            temp['house_type_монолитный'] = 1
        elif (to_model[1] in "house_type_панельный"):
            temp['house_type_панельный'] = 1

        if (to_model[2] in "state_евроремонт"):
            temp['state_евроремонт'] = 1
        elif (to_model[2] in "state_свободная планировка"):
            temp['state_свободная планировка'] = 1
        elif (to_model[2] in "state_среднее"):
            temp['state_среднее'] = 1
        elif (to_model[2] in "state_требует ремонта"):
            temp['state_требует ремонта'] = 1
        elif (to_model[2] in "state_хорошее"):
            temp['state_хорошее'] = 1
        elif (to_model[2] in "state_черновая отделка"):
            temp['state_черновая отделка'] = 1

        if (to_model[3] in "region_Алматы, Алатауский р-н"):
            temp['region_Алматы, Алатауский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Алмалинский р-н"):
            temp['region_Алматы, Алмалинский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Ауэзовский р-н"):
            temp['region_Алматы, Ауэзовский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Бостандыкский р-н"):
            temp['region_Алматы, Бостандыкский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Жетысуйский р-н"):
            temp['region_Алматы, Жетысуйский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Медеуский р-н"):
            temp['region_Алматы, Медеуский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Наурызбайский р-н"):
            temp['region_Алматы, Наурызбайский р-н'] = 1
        elif (to_model[3] in "region_Алматы, Турксибский р-н"):
            temp['region_Алматы, Турксибский р-н'] = 1
        elif (to_model[3] in "region_Казахстан"):
            temp['region_Казахстан'] = 1
        elif (to_model[3] in "region_Алматы, Жетысуский р-н"):
            temp['region_Алматы, Жетысуский р-н'] = 1
        if (to_model[4] in "internet_ADSL"):
                temp['internet_ADSL'] = 1
        elif (to_model[4] in "internet_оптика"):
            temp['internet_оптика'] = 1
        elif (to_model[4] in "internet_проводной"):
            temp['internet_проводной'] = 1
        elif (to_model[4] in "internet_через TV кабель"):
            temp['internet_через TV кабель'] = 1
        else:
            temp['internet_0'] = 1

        if (to_model[5] in "bathroom_2 с/у и более"):
            temp['bathroom_2 с/у и более'] = 1
        elif (to_model[5] in "bathroom_нет"):
            temp['bathroom_нет'] = 1
        elif (to_model[5] in "bathroom_раздельный"):
            temp['bathroom_раздельный'] = 1
        elif (to_model[5] in "bathroom_совмещенный"):
            temp['bathroom_совмещенный'] = 1

        temp['built_time'] = float(to_model[6])
        temp['all_space'] = float(to_model[7])
        temp['balcony'] = float(to_model[8])
        temp['phone'] = float(to_model[9])
        temp['parking'] = float(to_model[10])
        temp['furniture'] = float(to_model[11])
        temp['at_the_hostel'] = float(to_model[12])
        temp['appartments_floor'] = float(to_model[13])
        temp['building_floors'] = float(to_model[14])
        lat, lon = HousePricing.yandex_geocoder(to_model[15])
        temp['trngl_first_point'] = ((43.340777 - float(lat)) + (76.950168 - float(lon)))
        temp['trngl_second_point'] = ((43.232742 - float(lat)) + (76.797475 - float(lon)))
        temp['trngl_third_point'] = ((43.196848 - float(lat)) + (76.979312 - float(lon)))
        answer = pd.DataFrame(temp, index=0, columns=columns)
        return answer



    def train_model(self):
        data = pd.read_csv("dtrain.csv", delimiter=",")
        data = data[data['geocode_lat'] != 0]
        zeros = data[data['geocode_lat'] == 0]
        data = shuffle(data)
        data = data[data['price'] < 1000000000]

        X = data[['room_number', 'house_type_иное', 'house_type_каркасно-камышитовый',
                  'house_type_кирпичный', 'house_type_монолитный',
                  'house_type_панельный', 'state_евроремонт', 'state_свободная планировка',
                  'state_среднее', 'state_требует ремонта', 'state_хорошее',
                  'state_черновая отделка', 'region_Алматы, Алатауский р-н',
                  'region_Алматы, Алмалинский р-н', 'region_Алматы, Ауэзовский р-н',
                  'region_Алматы, Бостандыкский р-н', 'region_Алматы, Жетысуйский р-н',
                  'region_Алматы, Жетысуский р-н', 'region_Алматы, Медеуский р-н',
                  'region_Алматы, Наурызбайский р-н', 'region_Алматы, Турксибский р-н',
                  'region_Казахстан', 'internet_0', 'internet_ADSL', 'internet_оптика', 'internet_проводной',
                  'internet_через TV кабель', 'bathroom_2 с/у и более', 'bathroom_нет',
                  'bathroom_раздельный', 'bathroom_совмещенный', 'built_time', 'all_space', 'balcony',
                  'phone', 'parking', 'furniture', 'at_the_hostel',
                  'appartments_floor', 'building_floors',
                  'trngl_first_point', 'trngl_second_point', 'trngl_third_point']]
        y = data['price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size=0.6)
        self.gbr_model = GradientBoostingRegressor(n_estimators = (len(X.columns) * 2), learning_rate=0.2,
                                                   random_state=7, max_depth=10)
        self.rfr_model = RandomForestRegressor(n_estimators = (len(X.columns) * 2), random_state=7)

        self.gbr_model.fit(X_train, y_train)
        self.rfr_model.fit(X_train, y_train)



    def predict(self, data):
        answer = self.normalization(data)
        return ((self.rfr_model.predict(answer)[0] + self.gbr_model.predict(answer)[0]) / 2)



def main():
    x = HousePricing()
    x.train_model()
    test = "3|кирпичный|хорошее|Медеуский р-н|оптика|раздельный|2010|82.6|0|1|1|0.5|0|9|11|мкр. Коктем-2, 8"
    x.predict(test)

main()
