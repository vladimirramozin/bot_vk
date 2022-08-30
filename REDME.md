# VK-бот кондитериской Ральф.

## Описание проекта:
Чат-бот кондитерского магазина с возможностью выбора ассортимента и последующей покупкой (функции оплаты не подключены).

## Основные возможности:
```
Бот начинает работу 
```
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/vladimirramozin/api_final_yatube.git
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source .venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
### Пример запроса:
{
"text": "sterwsfdrifddxvcng"
}

## Системные требования:
Python 3.7,
Django==2.2.16,
pytest==6.2.4,
pytest-pythonpath==0.7.3,
pytest-django==4.4.0,
djangorestframework==3.12.4,
djangorestframework-simplejwt==4.7.2,
Pillow==8.3.1,
PyJWT==2.1.0,
requests==2.26.0
