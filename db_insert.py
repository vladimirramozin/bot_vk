import os

import psycopg2

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

con = psycopg2.connect(
   database=os.environ.get('DB_NAME'),
   user=os.environ.get('POSTGRES_USER'),
   password=os.environ.get('POSTGRES_PASSWORD'),
   host=os.environ.get('DB_HOST'),
  port=os.environ.get('DB_PORT'),
)


shops = [
    ('главная', 'Привет, я чат-бот кондитерского магазина "Ральф"  &#128526;', '/app/photo/main.jpg'),
    ('маффин', 'шоколадный - сделан из лучших какао бобов, собранных в индонезии, прекрасно подойдет к утреннему кофе. Стоимость 150 руб. (1 шт)', '/app/photo/maffin_choko.jpg'),
    ('маффин', 'ванильный - ваниль мы привозим из Пуэрто-Рико. Стоимость 150 руб. (1 шт)', '/app/photo/maffin.jpg'),
    ('торт', 'Торт «Три шоколада» — это торт, состоящий из трех шоколадных муссов. Стоимость 1500 руб. (вес 2 кг)', '/app/photo/three_choko.jpg'),
    ('торт', 'Торт «Красный бархат» — это классический десерт родом из США. Стоимость 1700 руб. (вес 2 кг)', '/app/photo/red_barhat.jpg'),
    ('пончик', 'Классический пончики - мягкие, сладкие кольца из теста, жареные во фритюре и посыпанные сахарной пудрой. Стоимость 70 руб. (1 шт.)', '/app/photo/classik.jpg'),
    ('пончик', 'Шоколадные пончики - вкус корицы и шоколада гармонируют друг с другом, а сахарная глазурь придает сочность. Стоимость 80 руб. (1 шт)', '/app/photo/choko.jpg'),
    ('команда', 'Шеф', '/app/photo/chef.jpg'),
    ('команда', 'Джеки', '/app/photo/djeki.jpg'),
    ('команда', 'Люк', '/app/photo/god_man.jpeg'),
]


shop_records = ", ".join(["%s"] * len(shops))

insert_query = (
    f"INSERT INTO shop (category, products, photo) VALUES {shop_records}"
)

con.autocommit = True
cursor = con.cursor()
cursor.execute(insert_query, shops)
