import os

import psycopg2
from dotenv import load_dotenv

load_dotenv('.env')

con = psycopg2.connect(
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT'),
)


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('Query executed successfully')
    except psycopg2.OperationalError:
        print('The error occurred')


delete_shop_table = """
DELETE FROM shop
"""
execute_query(con, delete_shop_table)
con.close()
