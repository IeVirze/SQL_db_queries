from db.create_db import create_db 
from db.create_db import populate_countries 
from db.create_db import populate_channels 
from db.create_db import populate_products 
from db.create_db import populate_applications 
import sqlite3

#main function
def main():
    conn, cursor = create_db()

    #populate tables
    populate_countries(cursor)
    populate_channels(cursor)
    populate_products(cursor)
    populate_applications(cursor, 10000)

    #comit changes
    conn.commit()

    #close connection
    conn.close()

    #print('db created, connection closed')



if __name__ == "__main__":
    main()