from datetime import datetime
import pytz

file_info = []


# функция для заполнения массива информацией из файла
def fill_array():
    global file_info
    with open('RU.txt', encoding='utf-8') as file:
        file_info = [line.split("\t") for line in file]


# метод переводящий массив в нужный для ответа словарь
def format_geo_info(info):
    fields = ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature class",
              "feature code", "country code", "cc2", "admin1 code", "admin2 code", "admin3 code", "admin4 code",
              "population", "elevation", "dem", "timezone", "modification date"]
    return dict(zip(fields, info))


# метод принимает geonameid и возвращает информацию о городе
def find_by_geonameid(geonameid):
    for city in file_info:
        if city[0] == geonameid:
            return format_geo_info(city)


# метод принимает страницу и количество отображаемых на странице городов и возвращает информацию о городах
def geonames_on_pages(page, count):  # page - номер страницы, count - количество городов
    return [format_geo_info(file_info[i]) for i in range((count*(page-1)), count*(page-1)+count)]


# метод принимает названия двух городов на русском языке и получает информацию о разных городах + какой расположен
# севернее + одинаковая ли у них временная зона
def find_by_ru_names(name1, name2):
    answer = {"first_city": [],
              "second_city": []}
    # поиск нужных городов
    for city in file_info:
        if name1 in city[3].split(','):
            if not answer["first_city"] or city[14] > answer["first_city"][14]:
                answer["first_city"] = city
        if name2 in city[3].split(','):
            if not answer["second_city"] or city[14] > answer["second_city"][14]:
                answer["second_city"] = city

    # форматирование городов
    answer["first_city"] = format_geo_info(answer["first_city"])
    answer["second_city"] = format_geo_info(answer["second_city"])

    # поиск более северного города
    if float(answer["first_city"]["latitude"]) > float(answer["second_city"]["latitude"]):
        answer["to_the_north"] = "first"
    elif float(answer["first_city"]["latitude"]) < float(answer["second_city"]["latitude"]):
        answer["to_the_north"] = "second"
    else:
        answer["to_the_north"] = "same"

    # проверка на идентичность часовых поясов
    if answer["first_city"]["timezone"] == answer["second_city"]["timezone"]:
        answer["same_timezone"] = True
    else:
        answer["same_timezone"] = False

        # вычисление разницы во времени между часовыми поясами
        first_city_tz_offset = pytz.timezone(answer["first_city"]["timezone"]).utcoffset(datetime.now())
        second_city_tz_offset = pytz.timezone(answer["second_city"]["timezone"]).utcoffset(datetime.now())

        difference = first_city_tz_offset - second_city_tz_offset

        # перевод разницы в часы
        if difference.days == -1:  # если разница отрицательная
            answer['tz_difference'] = -int(abs(difference).seconds/3600)
        else:  # если разница положительная
            answer['tz_difference'] = int(difference.seconds/3600)

    return answer


# метод, в котором пользователь вводит часть названия города и возвращает ему подсказку с вариантами продолжений
def find_by_part(name):
    similar_names = []
    for city in file_info:
        for alternative_name in city[3].split(','):
            if name in alternative_name:
                similar_names.append(alternative_name)
    similar_names = list(set(similar_names))
    return {"similar_names": similar_names}
