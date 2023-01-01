import random
import requests
from functools import wraps

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Bot:
    def __init__(self, token):
        self.messages_handlers = {}
        self.token = token
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)
        self.session = requests.Session()

    def message_handler(self, message):
        def __handler(func):
            @wraps(func)
            def handler_function(*args, **kwargs):
                func(*args, **kwargs)

            self.messages_handlers.setdefault(message, [])
            self.messages_handlers[message].append(handler_function)
            return handler_function

        return __handler

    def create_photo_attachment(self, image_url):
        upload = VkUpload(self.vk_session)
        image = self.session.get(image_url, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        return f"photo{photo['owner_id']}_{photo['id']}"

    def send_message(self, user, message=None, keyboard=None, attachments=None):
        values = {
            "user_id": user,
            "message": message,
            "random_id": random.randint(-2147483648, +2147483648),
            "keyboard": keyboard,
            "attachment": attachments
        }
        return self.vk_session.method("messages.send", values)


    def infinity_polling(self):
        while True:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if self.messages_handlers.get(event.message):
                        for handler in self.messages_handlers.get(event.message):
                            handler(event)
