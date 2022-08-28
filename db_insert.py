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
  database="my_bot", 
  user="my_bot_user", 
  password="QWEasd123", 
  host="127.0.0.1", 
  port="5432"
)


shops = [
    ('главная', 'Привет, я чат-бот кондитерского магазина "Ральф"  &#128526;', '/home/vladimir/bot_vk/photo/main.jpg'),
    ('маффин', 'шоколадный - сделан из лучших какао бобов, собранных в индонезии, прекрасно подойдет к утреннему кофе. Стоимость 150 руб. (1 шт)', '/home/vladimir/bot_vk/photo/maffin_choko.jpg'),
    ('маффин', 'ванильный - ваниль мы привозим из Пуэрто-Рико. Стоимость 150 руб. (1 шт)', '/home/vladimir/bot_vk/photo/maffin.jpg'),
    ('торт', 'Торт «Три шоколада» — это торт, состоящий из трех шоколадных муссов. Стоимость 1500 руб. (вес 2 кг)', '/home/vladimir/bot_vk/photo/three_choko.jpg'),
    ('торт', 'Торт «Красный бархат» — это классический десерт родом из США. Стоимость 1700 руб. (вес 2 кг)', '/home/vladimir/bot_vk/photo/red_barhat.jpg'),
    ('пончик', 'Классический пончики - мягкие, сладкие кольца из теста, жареные во фритюре и посыпанные сахарной пудрой. Стоимость 70 руб. (1 шт.)', '/home/vladimir/bot_vk/photo/classik.jpg'),
    ('пончик', 'Шоколадные пончики - вкус корицы и шоколада гармонируют друг с другом, а сахарная глазурь придает сочность. Стоимость 80 руб. (1 шт)', '/home/vladimir/bot_vk/photo/choko.jpg'),
    ('команда', 'Шеф', '/home/vladimir/bot_vk/photo/chef.jpg'),
    ('команда', 'Джеки', '/home/vladimir/bot_vk/photo/djeki.jpg'),
    ('команда', 'Люк', '/home/vladimir/bot_vk/photo/god_man.jpeg'),
]


shop_records = ", ".join(["%s"] * len(shops))

insert_query = (
    f"INSERT INTO shop (category, products, photo) VALUES {shop_records}"
)

con.autocommit = True
cursor = con.cursor()
cursor.execute(insert_query, shops)
