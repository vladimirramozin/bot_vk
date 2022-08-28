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

logger =logging.getLogger(__name__)
handler = RotatingFileHandler('my_bot_logger.log', maxBytes = 500000, backupCount=5)
logger.setLevel(logging.INFO)
logger.addHandler(handler) 
formatter = logging.Formatter('%(asctime)s, %(filename)s, %(levelname)s, %(message)s')
handler.setFormatter(formatter)
load_dotenv('.env')

token = os.environ.get("VK_TOKEN")
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
upload = VkUpload(vk)

try:
   connection_bd = psycopg2.connect(
       database= os.environ.get("DB_NAME"),
       user=os.environ.get("DB_USER"),
       password=os.environ.get("DB_PASSWORD"),
       host=os.environ.get("DB_HOST"),
       port=os.environ.get("DB_PORT"),
   )
   logger.info('успешное подключение к бд')
except OperationalError:
   print('нет подключения к бд')




if __name__=='__main__':
    print("Бот запущен")

    for event in longpoll.listen():
        #pdb.set_trace()
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            request = event.text.lower()
            attachmets = []
            if request == "привет" or request == 'начать':
                select = "'главная'"
                preparing_images_for_sending(select, vk, connection_bd, upload, event.user_id, 'start')
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == "магазин":
                write_msg(event.user_id, "Чтобы вы хотели попробовать?", vk, keyboard='keyboard_for_shop')
            elif request == "маффины":
                write_msg(event.user_id, "У нас их много какой будешь?", vk)
                time.sleep(1.1)
                select = "'маффин'"
                preparing_images_for_sending(select, vk, connection_bd, upload, event.user_id, 'pay')
            elif request == "торты":
                write_msg(event.user_id, "У нас их много какой будешь? сейчас все покажу!", vk)
                time.sleep(1.1)
                select = "'торт'"
                preparing_images_for_sending(select, vk, connection_bd, upload, event.user_id, 'pay')
            elif request == "пончики":
                write_msg(event.user_id, "У нас их много какой будешь?", vk)
                time.sleep(1.1)
                select = "'пончик'"
                preparing_images_for_sending(select, vk, connection_bd, upload, event.user_id, 'pay')
            elif request == "о нашей команде":
                time.sleep(1.1)
                select = "'команда'"
                preparing_images_for_sending(select, vk, connection_bd, upload, event.user_id, 'team')
            elif request == "назад":
                write_msg(event.user_id, "Чтобы вы хотели попробовать?", vk, keyboard='keyboard_for_shop')
            elif request == "оплатить":
                write_msg(event.user_id, "к сожалению у нас пока нет аккаунта для платежей", vk, keyboard='keyboard_for_shop')
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", vk)
