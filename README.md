# Sample Data Database and SQL queries

This is sample data database created with Python SQLite3 from a database relational table schema. The main SQL queries file "quaries.sql" is created to query the db via Python to find answers for specific marketing analytics questions.

## Database build

Database has been built based on the following schema:

[DB relational table schema](misc/Improved%20DB%20relations.png)

Database currently consist of 4 tables:
* dtm_applications - contain product application data and foreign keys to other tables
* dtm_products - contain modelled product data
* dtm_countries - contains sample set of countries
* dtm_channel - contains sample set of typical Marketing channels

## SQL query writting and running
Current set-up allows for SQL queries to be written in a folder "SQL" in same or separte .sql files with a typical SQL syntax. The file "run_SQL.py" allows the SQL files to be processed and executed like typical SQL queries returning data in Python DataFrame for validation and (if # removed from commented out section) downloading data as .csv for further data usage or processing outside of the database.

## How to use?
Currently the project is not packaged as typical Python project ready for production. 

1. Download repository using typical means to download
2. Make sure you have all Python libraries installed which are listed in "requirements.txt" file
3. Run "build_db.py" (it should build sqlite database in "db" folder)
4. If needed - modify file/s in "SQL" folder
5. Run "run_SQL.py" by default it returns Python DataFrame with data 
