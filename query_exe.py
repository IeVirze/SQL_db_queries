import sqlite3
import os
import pandas as pd

db_path = 'db/loans.db'
sql_path = 'quaries.sql'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

#Read SQL
with open(sql_path, "r") as f:
    sql_script = f.read()

#Execute SQL
queries = sql_script.split(";")

res = {}

for query in queries: 
    query = query.strip()

    res = pd.read_sql_query(query, conn)
    print(res)

conn.commit()

conn.close()