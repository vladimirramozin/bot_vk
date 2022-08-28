import os
import unittest

import psycopg2
import vk_api
from dotenv import load_dotenv
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll

from message_func import execute_read_query, write_msg

load_dotenv('.env')
token = os.environ.get('VK_TOKEN')
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
upload = VkUpload(vk)


connection_bd = psycopg2.connect(
   database=os.environ.get('DB_NAME'),
   user=os.environ.get('DB_USER'),
   password=os.environ.get('DB_PASSWORD'),
   host=os.environ.get('DB_HOST'),
   port=os.environ.get('DB_PORT'),
)


class TestMybot(unittest.TestCase):
    def test_write_msg(self):
        """Проверка отправки сообщений без вложений"""
        user_id = 739496938
        message = 'Hi!'
        send_message = write_msg(user_id, message, vk)
        self.assertEqual(isinstance(send_message, int), True, ('сообщение'
                         'без вложения не отправляется'))

    def test_execute_read_query(self):
        """Проверка доступности данных главной страницы в БД"""
        category = '"главная"'
        sel = 'SELECT COUNT(*) FROM shop WHERE category = {}'.format(category)
        acess_bd = execute_read_query(connection_bd, sel)
        self.assertEqual(acess_bd[0][0], 1, (
            'база данных недоступна или изменены '
            'данные главной страницы'
            )
        )


if __name__ == '__main__':
    unittest.main()
