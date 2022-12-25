import configparser
import vk_api
import requests
from pprint import pprint

API_URL = 'https://api.vk.com/method/'
config = configparser.ConfigParser()  # создаём объекта парсера
config.read("..\settings.ini")  # читаем конфиг
comm_token = config["Tokens"]["comm"]
user_token = config["Tokens"]["VK"]


class VK:
    def __init__(self, user_token, API_URL):
        self.user_token = user_token
        self.API_URL = API_URL
        self.idnum = []

    def get_info(self, user_ids):
        method = 'users.get'
        url = API_URL + method
        params = {
            'user_ids': user_ids,
            'access_token': user_token,
            'fields': 'city, bdate, sex',
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        response = res.json().get("response")
        return response

    def get_vk_photo(self, id):
        metod = 'photos.get'
        list_photos = {}
        params = {
            'access_token': user_token,
            'v': '5.131',
            'owner_id': id,
            'album_id': 'profile',
            'extended': '1'
        }
        response = requests.get(url=API_URL + metod, params=params)
        photo = response.json()
        if 'response' in photo.keys():
            for i in photo['response']['items']:
                index_size = 99
                for j in i['sizes']:
                    k = 'wzyrqpoxms'.find(j['type'])
                    if k < index_size:
                        index_size = k
                        max_url = j['url']
                list_photos.update([(i['likes']['count'], max_url)])
            return [sorted(list_photos.items(), key=lambda x: -x[0])[i][1] for i in range(3)]

    def search_users(self, sex, age_at, age_to, city):
        all_persons = []
        link_profile = 'https://vk.com/id'
        vk_ = vk_api.VkApi(token=user_token)
        response = vk_.method('users.search',
                              {'v': '5.89',
                               'sex': sex,
                               'age_from': age_at,
                               'age_to': age_to,
                               'hometown': city
                               })
        for element in response['items']:
            id = element['id']
            photo = self.get_vk_photo(id)
            if photo is not None:
                person = [
                    id,
                    element['first_name'],
                    element['last_name'],
                    link_profile + str(element['id']),
                    self.get_vk_photo(id)
                ]
                all_persons.append(person)
        return all_persons


def main():
    sex = int(input('введите пол \n 1 - женский, \n 2 - мужской: '))
    age_at = int(input("возраст от: "))
    age_to = int(input("возраст до: "))
    city = input("город: ")
    find_people = VK(user_token, API_URL)
    pprint(find_people.search_users(sex, age_at, age_to, city))


if __name__ == '__main__':
    # main()
    find_people = VK(user_token, API_URL)
    pprint(find_people.get_vk_photo(67012330))
