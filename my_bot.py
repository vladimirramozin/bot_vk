import logging
import os
from logging.handlers import RotatingFileHandler

import psycopg2
import vk_api
from dotenv import load_dotenv
from psycopg2 import OperationalError
from vk_api import VkUpload
from vk_api.longpoll import VkEventType, VkLongPoll

from message_func import preparing_images_for_sending, write_msg

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

try:
    connection_bd = psycopg2.connect(
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
    )

    logger.info('успешное подключение к бд')
except OperationalError:
    print('нет подключения к бд')

change_func = {
    'пока':
        {'func': write_msg,
         'message': 'пока',
         'attachment': None,
         'keyboard': None},
    'оплатить':
        {'func': write_msg,
         'message': 'к сожалению у нас пока нет платежного аккаунта(',
         'attachment': None,
         'keyboard': None},
    'магазин':
        {'func': write_msg, 'message': 'Чтобы вы хотели попробовать?',
         'attachment': None,
         'keyboard': 'keyboard_for_shop'},
    'назад':
        {'func': write_msg,
         'message': 'Чтобы вы хотели попробовать?',
         'attachment': None,
         'keyboard': 'keyboard_for_shop'},
    'привет':
        {'func': preparing_images_for_sending,
         'category': '\'главная\'',
         'key': 'start'},
    'начать':
        {'func': preparing_images_for_sending,
         'category': '\'главная\'',
         'key': 'start'},
    'пончики':
        {'func': preparing_images_for_sending,
         'category': '\'пончик\'',
         'key':'pay'},
    'маффины':
        {'func': preparing_images_for_sending,
         'category': '\'маффин\'',
         'key': 'pay'},
    'торты':
        {'func': preparing_images_for_sending,
         'category': '\'торт\'',
         'key': 'pay'},
    'о нашей команде':
        {'func': preparing_images_for_sending,
         'category': '\'команда\'',
         'key': 'team'}
    }

if __name__ == '__main__':
    print('Бот запущен')
    for event in longpoll.listen():
        if (event.type == VkEventType.MESSAGE_NEW
                and event.to_me and event.text):
            request = event.text.lower()
            attachmets = []
            try:
                func = change_func.get(request).get('func')
                if func == write_msg:
                    message = change_func.get(request).get('message')
                    attachment = change_func.get(request).get('attachment')
                    keyboard = change_func.get(request).get('keyboard')
                    func(
                        user_id=event.user_id,
                        message=message,
                        attachment=attachment,
                        keyboard=keyboard, vk=vk
                    )
                elif func == preparing_images_for_sending:
                    category = change_func.get(request).get('category')
                    key = change_func.get(request).get('key')
                    if key == 'pay':
                        write_msg(
                            event.user_id,
                            'У нас их много, какой будешь?'
                            'Cейчас все покажу!?',
                            vk
                        )
                    func(
                        category=category,
                        key=key,
                        vk=vk,
                        con=connection_bd,
                        user_id=event.user_id,
                        upload=upload
                    )
            except AttributeError:
                write_msg(
                    event.user_id,
                    'Не поняла вашего ответа...',
                    vk
                )
