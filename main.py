from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import bot
import searcher
import database
import configparser
from datetime import date, datetime

if __name__ == "__main__":
    API_URL = 'https://api.vk.com/method/'
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    bot = bot.Bot(config["Tokens"]["bot"])
    comm_token = config["Tokens"]["comm"]
    user_token = config["Tokens"]["VK"]
    VK1 = searcher.VK(user_token, API_URL)
    DB = database.VKinderDB(password='postgres')
    client_sex = 0
    client_age = 0
    client_city = ''


    @bot.message_handler("Начать")  # Декоратор добавляющий обработчик на определённое сообщение
    def hello(msg):
        global client_sex, client_age, client_city
        client = VK1.get_info(msg.user_id)[0]
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Поиск', color=VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()
        photos = VK1.get_vk_photo(client["id"])
        print(client["id"], client["first_name"], client["last_name"],
                         client["bdate"], client["city"]["title"], client["sex"], photos)
        gender = (client["sex"] == 2)
        bdate = client["bdate"]
        client_city = client["city"]["title"]
        DB.insert_client(owner_id=client["id"], name=client["first_name"], surname=client["last_name"],
                         birthday=bdate, city=client_city, gender=gender, photo=photos)
        client_sex = {1:2, 2:1}[client["sex"]]
        today = date.today()
        birth_date = datetime.strptime(bdate, '%d.%m.%Y')
        client_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        bot.send_message(msg.user_id,
                         f'{client["id"]}, {client["city"]["title"]}\nЗдравствуйте, {client["first_name"]} {client["last_name"]}!\nВам {client_age} лет',
                         keyboard)  # Отправляем ответ


    @bot.message_handler("Поиск")
    def find_vk(msg):
        global client_sex, client_age, client_city
        for i in VK1.search_users(sex=client_sex, age_at=client_age, age_to=client_age, city=client_city):
            print(i)
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Запомнить', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('В чёрный список', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Следующий', color=VkKeyboardColor.POSITIVE)
            keyboard1 = keyboard.get_keyboard()
            bot.send_message(msg.user_id, f'{i[1]} {i[2]}\n{i[3]}\n{i[4][0]}', keyboard1)  # Отправляем ответ




    bot.infinity_polling()  # Бесконечный опрос ВК на изменения
