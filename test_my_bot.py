import unittest
import os
import time
import logging
from logging.handlers import RotatingFileHandler
#from logging.handler import RotatingFileHandler 
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import pdb
import psycopg2
from db_func import execute_read_query
from  message_func import preparing_images_for_sending, write_msg


load_dotenv('.env')
token = os.environ.get("VK_TOKEN")
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
upload = VkUpload(vk)


connection_bd = psycopg2.connect(
   database= os.environ.get("DB_NAME"),
   user=os.environ.get("DB_USER"),
   password=os.environ.get("DB_PASSWORD"),
   host=os.environ.get("DB_HOST"),
   port=os.environ.get("DB_PORT"),
)



class TestMybot(unittest.TestCase):
    def test_write_msg(self):
        """Проверка отправки сообщений без вложений"""
        user_id=739496938
        message = 'Hi!'
        send_message = write_msg(user_id, message, vk)
        self.assertEqual(isinstance(send_message, int), True, 'сообщение без вложения не отправляется')

    def test_execute_read_query(self):
        """Проверка доступности данных главной страницы в БД"""
        shop_category = "'главная'"
        select_shop = "SELECT COUNT(*) FROM shop WHERE category = {}".format(shop_category)
        acess_bd = execute_read_query(connection_bd, select_shop)
        self.assertEqual(acess_bd[0][0], 1, 'база данных недоступна или изменены данные главной страницы')


if __name__ == "__main__":
    unittest.main() 
