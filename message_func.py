import logging
from logging.handlers import RotatingFileHandler
import psycopg2
import os
from psycopg2 import OperationalError
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

keyboard_for_main = VkKeyboard(inline=True)
keyboard_for_main.add_button('магазин', color=VkKeyboardColor.PRIMARY)
keyboard_for_main.add_line()
keyboard_for_main.add_button(
    'о нашей команде',
    color=VkKeyboardColor.SECONDARY
)

keyboard_for_shop = VkKeyboard(inline=True)
keyboard_for_shop.add_button('маффины', color=VkKeyboardColor.PRIMARY)
keyboard_for_shop.add_line()

keyboard_for_shop.add_button('пончики', color=VkKeyboardColor.PRIMARY)

keyboard_for_shop.add_line()
keyboard_for_shop.add_button('торты', color=VkKeyboardColor.PRIMARY)

keyboard_for_team = VkKeyboard(one_time=True)
keyboard_for_team.add_button('назад', color=VkKeyboardColor.PRIMARY)


keyboard_for_shop_pay = VkKeyboard(inline=True)
keyboard_for_shop_pay.add_button('оплатить', color=VkKeyboardColor.PRIMARY)
keyboard_for_shop_pay.add_button('назад', color=VkKeyboardColor.PRIMARY)

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    'my_bot_logger.log',
    maxBytes=500000,
    backupCount=5
)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(filename)s, %(levelname)s, %(message)s'
)
handler.setFormatter(formatter)

def connection_bd():
    try:
        connection_bd = psycopg2.connect(
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
        )
        logger.info('успешное подключение к бд')
        return  connection_bd
    
    except OperationalError:
        print('нет подключения к бд')

def execute_read_query(connection_bd, query):
    '''
    Функция посылает запрос в БД 
    postgres принимает два аргумента:
    connection_bd, соединение к бд через psycopg2.connect,
    query, SQL запрос SELECT..
    '''
    cursor = connection_bd.cursor()
    try:
        cursor.execute(query)
        logger.info('SQL запрос к БД')
        return cursor.fetchall()
    except OperationalError:
        logger.error('неверный SQL запрос к БД')


def preparing_images_for_sending(category, vk, con, upload, user_id, key=None):
    '''
    Подготавливает представление изображения к виду
    необходимому для отправку в VK, принимает аргументы:
    category, категория по которой делается выборка в бд,
    vk, подсоединение к чату в VK, 
    con, соединение с БД,
    upload, результат VkUpload(vk),
    user_id, идентификатор пользователя в VK,
    key, варианты клавиатур для ответов,
    после завершения работы передает данные в write_msg()
    '''
    select_shop = (
        'SELECT products, photo FROM shop WHERE category = {}'.format(category)
    )
    shop = execute_read_query(con, select_shop)
    try:
        for photo in shop:
            attachmets = []
            uploade_image = upload.photo_messages(photos=photo[1])[0]
            attachmets.append(
                'photo{}_{}'.format(
                    uploade_image['owner_id'],
                    uploade_image['id']
                )
            )
            write_msg(user_id, f'{photo[0]}', vk, attachmets, key)
            con.close()
            logger.info('файл картинки успешно прочитан')
    except FileNotFoundError:
        logger.error('файл не найден')


def write_msg(user_id, message, vk, attachment=None, keyboard=None):
    '''
    Передает сообщение в VK, принимает аргументы:
    user_id, идентификатор пользователя в VK,
    message, строка сообщения,
    vk, подсоединение к чату в VK,
    attachment, подготовленное в preparing_images_for_sending() 
    для отправки в ВК изобржение,
    key, варианты клавиатур для ответов
    '''
    if keyboard == 'keyboard_for_shop':
        return vk.method(
            'messages.send', {
                'user_id': user_id,
                'message': message,
                'random_id': get_random_id(),
                'keyboard': keyboard_for_shop.get_keyboard()
                }
            )
    elif keyboard == 'team':
        return vk.method(
            'messages.send', {
                'user_id': user_id,
                'message': message,
                'random_id': get_random_id(),
                'attachment': ','.join(attachment),
                'keyboard': keyboard_for_team.get_keyboard()
                }
            )
    elif keyboard == 'pay':
        return vk.method(
            'messages.send', {
                'user_id': user_id,
                'message': message,
                'random_id': get_random_id(),
                'attachment': ','.join(attachment),
                'keyboard': keyboard_for_shop_pay.get_keyboard()
                }
            )
    elif keyboard == 'start':
        return vk.method(
            'messages.send', {
                'user_id': user_id,
                'message': message,
                'random_id': get_random_id(),
                'attachment': ','.join(attachment),
                'keyboard': keyboard_for_main.get_keyboard()
                }
            )
    else:
        return vk.method(
            'messages.send', {
                'user_id': user_id,
                'message': message,
                'random_id': get_random_id()
                }
            )
