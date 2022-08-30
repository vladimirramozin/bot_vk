import logging
import os
import time
from logging.handlers import RotatingFileHandler

import psycopg2
import vk_api
from dotenv import load_dotenv
from psycopg2 import OperationalError
from vk_api import VkUpload
from vk_api.longpoll import VkEventType, VkLongPoll

from message_func import connection_bd, preparing_images_for_sending, write_msg

logger = logging.getLogger(__name__)
handler = RotatingFileHandler('my_bot_logger.log',
                              maxBytes=500000, backupCount=5)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s, %(filename)s,'
                              '%(levelname)s, %(message)s')
handler.setFormatter(formatter)
load_dotenv('.env')

token = os.environ.get('VK_TOKEN')
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
upload = VkUpload(vk)


if __name__ == '__main__':
    print('Бот запущен')
    for event in longpoll.listen():
        if (event.type == VkEventType.MESSAGE_NEW
                and event.to_me and event.text):
            request = event.text.lower()
            attachmets = []
            if request == 'привет' or request == 'начать':
                select = '\"главная\"'
                connection_bd = connection_bd()
                preparing_images_for_sending(select, vk, connection_bd, upload,
                                             event.user_id, 'start')
            elif request == 'пока':
                write_msg(event.user_id, 'Пока((')
            elif request == 'магазин':
                write_msg(event.user_id, 'Чтобы вы хотели попробовать?',
                          vk, keyboard='keyboard_for_shop')
            elif request == 'маффины':
                write_msg(
                    event.user_id,
                    'У нас их много, какой будешь? Cейчас все покажу!',
                    vk
                )
                time.sleep(1.1)
                select = '\"маффин\"'
                connection = connection_bd()
                preparing_images_for_sending(
                    select,
                    vk,
                    connection,
                    upload, event.user_id,
                    'pay'
                )
            elif request == 'торты':
                write_msg(
                    event.user_id,
                    'У нас их много, какой будешь? Cейчас все покажу!',
                    vk
                )
                time.sleep(1.1)
                select = '\"торт\"'
                connection = connection_bd()
                preparing_images_for_sending(
                    select,
                    vk,
                    connection,
                    upload,
                    event.user_id,
                    'pay'
                )
            elif request == 'пончики':
                write_msg(
                    event.user_id,
                    'У нас их много, какой будешь? Cейчас все покажу!?',
                    vk
                 )
                time.sleep(1.1)
                select = '\"пончик\"'
                connection = connection_bd()
                preparing_images_for_sending(
                    select,
                    vk,
                    connection,
                    upload,
                    event.user_id,
                    'pay'
                )
            elif request == 'о нашей команде':
                time.sleep(1.1)
                select = '\"команда\"'
                connection = connection_bd()
                preparing_images_for_sending(
                    select,
                    vk,
                    connection,
                    upload,
                    event.user_id,
                    'team'
                )
            elif request == 'назад':
                write_msg(
                    event.user_id,
                    'Чтобы вы хотели попробовать?',
                    vk,
                    keyboard='keyboard_for_shop'
                )
            elif request == 'оплатить':
                write_msg(
                    event.user_id,
                    'к сожалению у нас пока нет аккаунта для платежей',
                    vk
                )
            else:
                write_msg(
                    event.user_id,
                    'Не поняла вашего ответа...',
                    vk
                )
