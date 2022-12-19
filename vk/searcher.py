import time

import vk_api, requests, json
from pprint import pprint

API_URL = 'https://api.vk.com/method/'
user_token = 'vk1.a.RfkfwZV20ihXF3QhAW7qI8rqWQ8OBw0pz7164OBS2GKM8q6u9qy3xA4YSDllX3ZHmvS7j7GMMI7BUEdZr84gbHTY0txHcy-4XqDRzSakIcwa8qVELHM1qQLCjiKHDSXKzhjBbsOtGYN_Gaz1wd3Qt-O7CE2J-ErwuVu5ywNgnO-ZDn94XIArhxvtvMtorm2Q'
comm_token = 'vk1.a.uEAZDL6VdipYG2DG8V4Adi1Rkul0lGcw5uS-Fau_BX7tdernJnHWP1sAdbi9Gi05Xv6x8ERic8g0wO_9wTyDAEDWBCmF8UhjOJbTf56OuTA4CXesAWg7w1q7-DASQS8C6Tod-Ai5n9G3kLnarynV2llKki-DrVimbEkDZtfRt_Wy8KBvjVKk0URrkK_apPHW9tRNskxGbB-5itcKwY4Jhw'

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
            'v': '5.131',
            'is_closed': 'False'
        }
        res = requests.get(url, params=params)
        response = res.json().get("response")
        return response

    def get_vk_photo(self, id):
        metod = 'photos.get'

        list_photos = []
        params = {
            'access_token': user_token,
            'v': '5.131',
            'owner_id': id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'
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
                list_photos.append(max_url)
        return list_photos

    def search_users(self, sex, age_at, age_to, city):
        all_persons = []
        link_profile = 'https://vk.com/id'
        vk_ = vk_api.VkApi(token=user_token)
        response = vk_.method('users.search',
                              {'v': '5.89',
                              'sort': 1,
                               'sex': sex,
                               'status': 1,
                               'age_from': age_at,
                               'age_to': age_to,
                               'has_photo': 1,
                               'is_closed': False,
                               'album_id': 'profile',
                               'count': 25,
                               'online': 1,
                               'hometown': city,
                               'photo_sizes': 1,
                               'extended': 1
        })
        for element in response['items']:
            id = element['id']

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
    main()
