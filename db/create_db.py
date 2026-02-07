import sqlite3
import random
import string
from datetime import datetime, timedelta

#Function for SQLite DB creation
def create_db(): 
    
    #Connect to or create DB
    conn = sqlite3.connect('loans.db')
    cursor = conn.cursor()

    #drop tables if exist
    cursor.execute('DROP TABLE IF EXISTS dim_application')
    cursor.execute('DROP TABLE IF EXISTS dim_product')
    cursor.execute('DROP TABLE IF EXISTS dim_channel')
    cursor.execute('DROP TABLE IF EXISTS dim_countries')



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
        CREATE TABLE dim_products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   product_full_name TEXT, 
                   product_short_name TEXT,
                   country_id INTEGER,
                   FOREIGN KEY (country_id) REFERENCES dim_countries(id)
                    )
    ''')

    # Create dim_application table
    cursor.execute('''
        CREATE TABLE dim_applications(
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
    cursor.executemany("INSERT INTO dim_countries (country_code, country_name, region_name, short_name) VALUES (?, ?, ?, ?)", countries)

    print('countries added')

#populate channel table with sample data
def populate_channels(cursor):

    #Get country ids
    cursor.execute('SELECT id FROM dim_countries')
    country_ids = [row[0] for row in cursor.fetchall()]

    #channel groups based on typical GA4 default grouping
    channel_groups = ['Organic Search', 'Direct', 'Paid Search', 'Email', 'Organic Social', 'Paid Social', 'Affiliates', 'Paid Other']

    social_ch = ['Reddit', 'LinkedIn', 'Lemmy', 'Instagram', 'Facebook', 'Threads', 'Bluesky', 'Discord']

    #in the list of search engines are only the ones that tend to show ads:
    #Bing - Microsoft Advertisement network
    #Google - Google Ads network
    #Yahoo, Ecosia - integrates with Microsoft Advertisement network
    #Startpage - integrates with Google ads network
    #DuckDuckGo - integrates with Bing Ads (Microsoft Advertising), yet show ads based on keywords not user activity (can target more tech savvy or privacy concius people)
    search_ch = ['Bing', 'Google', 'Startpage', 'Ecosia', 'DuckDuckGo', 'Yahoo']

    other_ch = ['newsportal', 'youtube', 'TV', 'QR-pamphlet', 'widgetInCarPortal', 'widgetInBlog']


    channels = []
    channel_id = 1

    for country_id in country_ids[:10]: #use first 10 countries
        for i in range(random.randint(6, 19)): # 6 - 19 channels per country
            channel_group = random.choice(channel_groups)

            #print(channel_groups)

            if channel_groups == 'Email':
                channel_name = 'email'
                campaign_code = f"CMP-{country_id:02d}-{channel_id:03d}-email"
            elif channel_groups == 'Organic Search' or channel_groups == 'Paid Search':
                channel_name = random.choice(search_ch)
                campaign_code = f"CMP-{country_id:02d}-{channel_id:03d}-search"
            elif channel_groups == 'Organic Social' or channel_groups == 'Paid Social':
                channel_name = random.choice(social_ch)
                campaign_code = f"CMP-{country_id:02d}-{channel_id:03d}-social"
            elif channel_groups == 'Paid Other':
                channel_name = random.choice(other_ch)
                campaign_code = f"CMP-{country_id:02d}-{channel_id:03d}-other"
            elif channel_groups == "Affiliate":
                channel_name = 'influencers'

                #generate unique id for each affiliate

                leters = ''.join(random.choices(string.ascii_letters, k=3))
                uni = f"{random.randint(0,999999):06d}"  

                affiliate_num = leters + uni
                campaign_code = f"CMP-{country_id:02d}-{channel_id:03d}-{affiliate_num}"
            else:
                channel_name = 'Direct'
                campaign_code = ''
                country_id = country_id
                channel_id = channel_id

            channels.append((
                campaign_code, 
                channel_group, 
                channel_name, 
                country_id
            ))

            channel_id +=1

    cursor.executemany('''
        INSERT INTO dim_channel (campaign_code, channel_group, channel_name, country_id)
        VALUES (?, ?, ?, ?)
    ''', channels)
    
    print('channels added')


def populate_products(cursor):
    #Get country Ids
    cursor.execute('SELECT id FROM dim_countries')
    countries = cursor.fetchall()

    product_types = [
        ('Personal Loan - Standard', 'Personal Loan'),
        ('Personal Loan - Premium', 'Premium Personal'),
        ('Auto Loan - New Vehicle', 'Auto New'),
        ('Auto Loan - Used Vehicle', 'Auto Used'),
        ('Home Improvement Loan', 'Home Improve'),
        ('Debt Consolidation Loan', 'Debt Consol'),
        ('Business Loan - Startup', 'Business Start'),
        ('Business Loan - Expansion', 'Business Expand'),
        ('Student Loan', 'Student'),
        ('Medical Loan', 'Medical'),
        ('Green Energy Loan', 'Green Energy'),
        ('Quick Cash Loan', 'Quick Cash')
    ]
             
    products = []

    for (country_id,) in countries:

        #Each country has slighly different subset of products
        num_products = random.randint(5, 10)
        selected_products = random.sample(product_types, num_products)

        for full_name, short_name in selected_products:
            products.append((
                country_id,
                full_name,
                short_name
            ))

    cursor.executemany('''
        INSERT INTO dim_products (country_id, product_full_name, product_short_name)
        VALUES (?, ?, ?)
    ''', products)

    print('products added')

def populate_applications(cursor, num_applications):

    #Get all foreign keys
    cursor.execute('SELECT id FROM dim_channel')
    channel_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT id FROM dim_countries')
    country_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT id, country_id FROM dim_products')
    products = cursor.fetchall()

    #Generate applications over last X years/days/months
    start_date = datetime.now() - timedelta(days=730) #730 == 2 years

    applications = []

    for i in range(num_applications):

        random_day = random.randint(0, 730)
        application_date = start_date + timedelta(days=random_day)

        #Random product and country
        product_id, product_country_id = random.choice(products)
        country_id = product_country_id

        #Random channel
        cursor.execute('SELECT id FROM dim_channel WHERE country_id = ?', (country_id,))
        country_channels = cursor.fetchall()

        if country_channels:
            channel_id = random.choice(country_channels)[0]
        else:
            channel_id = random.choice(channel_ids)

        #Generate customer ID
        cust_id = f"{random.randint(0,999999):06d}"  

        #age of customers, leagal age where applications can be made and paid out
        age = random.randint(18, 75)

        #Loan amount
        if age < 25:
            loan_amount = round(random.uniform(500, 15000), 2)
        elif age <35:
            loan_amount = round(random.uniform(5000, 70000), 2)
        elif age <45:
            loan_amount = round(random.uniform(4000, 210000), 2)
        elif age < 50: 
            loan_amount = round(random.uniform(1000, 100000), 2)
        else:
            loan_amount = round(random.uniform(500, 20000), 2)

        applications.append((
            channel_id, 
            country_id, 
            product_id, 
            cust_id, 
            application_date.strftime('%Y-%m-%d'),
            age,
            loan_amount
        ))

    cursor.executemany('''
        INSERT INTO dim_applications (channel_id, country_id, product_id, customer_id, date, age_at_application, loan_amount)
        VALUES(?, ?, ?, ?, ?, ?, ?)                       
        ''', applications)
    

#main function
def main():
    conn, cursor = create_db()

    #populate tables
    populate_countries(cursor)
    populate_channels(cursor)
    populate_products(cursor)
    populate_applications(cursor, 5000)
    



    #comit changes
    conn.commit()

    #close connection
    conn.close()

    print('db created, connection closed')



print('test statement')

if __name__ == "__main__":
    main()