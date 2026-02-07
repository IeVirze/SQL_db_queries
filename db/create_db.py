import sqlite3
import random
from datetime import datetime, timedelta

#Function for SQLite DB creation
def create_db(): 
    
    #Connect to or create DB
    conn = sqlite3.connect('loans.db')
    cursor = conn.cursor()

    #drop tables if exist
    cursor.execute('DROP TABLE IF EXISTS dim_application')
    cursor.execute('DROP TABLE IF EXISTS dim_countries')
    cursor.execute('DROP TABLE IF EXISTS dim_channel')
    cursor.execute('DROP TABLE IF EXISTS dim_product')

    #create tables - SQL with datatypes more universally used; SQLite will convert to one of 5 affinities
    #Create dim_application table
    cursor.execute('''
        CREATE TABLE dim_countries (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   country_code TEXT NOT NULL UNIQUE,
                   country_name TEXT NOT NULL,
                   region_name TEXT,
                   short_name TEXT
                   )    
    ''')

    #Create dim_channel table
    cursor.execute('''
        CREATE TABLE dim_channel (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   campaign_code TEXT,
                   channel_group TEXT,
                   channel_name TEXT NOT NULL,
                   country_id INTEGER,
                   FOREIGN KEY (country_id) REFERENCES dim_countries(id)
                   )
    ''')

    #Create dim_product table
    cursor.execute(''' 
        CREATE TABLE dim_product (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   product_full_name TEXT, 
                   product_short_name TEXT
                   country_id INTEGER,
                   FOREIGN KEY (country_id) REFERENCES dim_countries(id)
                   )
    ''')

    #Create dim_application table
    cursor.execute('''
        CREATE TABLE dim_application(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   age_at_application INTEGER,
                   channel_id INTEGER, 
                   country_id INTEGER,
                   customer_id INTEGER, 
                   date DATE NOT NULL,
                   loan_amount REAL, 
                   product_id INTEGER,
                   FOREIGN KEY (country_id) REFERENCES dim_country(id),
                   FOREIGN KEY (channel_id) REFERENCES dim_channel(id),
                   FOREIGN KEY (product_id) REFERENCES dim_product(id)
                   )
    ''') # Customer id should be FOREIGN KEY (customer_id) REFERNECES dim_customer(id) as it would allow application data matching to real people
    print("DB createde")
    return conn, cursor

#Populate country table with sample data
def populate_countries(cursor):
    
    #insertable countries
    countries = [
        ('SE', 'Sweden', 'Europe', 'SWD'),
        ('UK', 'United Kingdom', 'Europe', 'UK'),
        ('DE', 'Germany', 'Europe', 'GER'),
        ('FR', 'France', 'Europe', 'FRA'),
        ('ES', 'Spain', 'Europe', 'ESP'),
        ('IT', 'Italy', 'Europe', 'ITA'),
        ('CA', 'Canada', 'North America', 'CAN'),
        ('NL', 'Netherlands', 'Europe', 'NLD'),
        ('NO', 'Norway', 'Europe', 'NOR'),
        ('LV', 'Latvia', 'Europe', 'LAT'),
        ('EE', 'Estonia', 'Eurpoe', 'EST'),
        ('LT', 'Lithuania', 'Europe', 'LIT'), 
        ('PL', 'Poland', 'Europe', 'POL'), 
        ('DK', 'Denmark', 'Europe', 'DNK')
    ]

    #query to populate countries table
    cursor.executemany(''' 
        INSERT INTO dim_countries (country_code, country_name, region_name, short_name)
        VALUES (?, ?, ?, ?)
    ''', countries)



print('test statement')


