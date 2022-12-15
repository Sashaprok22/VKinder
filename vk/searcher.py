import vk_api, requests, json
import pprint

API_URL = 'https://api.vk.com/method/'
user_token = ''
comm_token = 'vk1.a.uEAZDL6VdipYG2DG8V4Adi1Rkul0lGcw5uS-Fau_BX7tdernJnHWP1sAdbi9Gi05Xv6x8ERic8g0wO_9wTyDAEDWBCmF8UhjOJbTf56OuTA4CXesAWg7w1q7-DASQS8C6Tod-Ai5n9G3kLnarynV2llKki-DrVimbEkDZtfRt_Wy8KBvjVKk0URrkK_apPHW9tRNskxGbB-5itcKwY4Jhw'


def get_info(self, user_ids):
    method = 'users.get'
    url = self.API_URL + method
    params = {
        'user_ids': user_ids,
        'access_token': self.user_token,
        'fields': 'screen_name, city, bdate, sex, screen_name',
        'v': '5.131'
    }
    res = requests.get(url, params=params)
    response = res.json().get("response")
    return response.json()

def search_users(sex, age_at, age_to, city):
    all_persons = []
    idnum = []
    link_profile = 'https://vk.com/id'
    vk_ = vk_api.VkApi(token=user_token)
    response = vk_.method('users.search',
                          {'sort': 1,
                           'sex': sex,
                           'status': 1,
                           'age_from': age_at,
                           'age_to': age_to,
                           'has_photo': 1,
                           'album_id': 'profile',
                           'count': 25,
                           'online': 1,
                           'hometown': city
                           })
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link_profile + str(element['id']),
            element['id']
        ]
        all_persons.append(person)
        idnum.append(person[element['id']])
    return all_persons, idnum

sex = int(input('введите пол \n 1 - женский, \n 2 - мужской: '))
age_at = int(input("возраст от "))
age_to = int(input("возраст до "))
city = input("город: ")
find_people = search_users(sex, age_at, age_to, city)
print(f'запрос поиска людей в возрасте от {age_at} до {age_to} лет из города {city}\nрезультат: {find_people}')
search_users(sex, age_at, age_to, city)

