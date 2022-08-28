import logging
from logging.handlers import RotatingFileHandler

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


def execute_read_query(connection_bd, query):
    cursor = connection_bd.cursor()
    try:
        cursor.execute(query)
        logger.info('SQL запрос к БД')
        return cursor.fetchall()
    except OperationalError:
        logger.error('неверный SQL запрос к БД')


def preparing_images_for_sending(category, vk, con, upload, user_id, key=None):
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
            logger.info('файл картинки успешно прочитан')
        return attachmets
    except FileNotFoundError:
        logger.error('файл не найден')


def write_msg(user_id, message, vk, attachment=None, keyboard=None):
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
