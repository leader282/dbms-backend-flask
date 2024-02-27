from flask import Flask
import psycopg2
from config import load_config

app = Flask(__name__)

# Function to connect to the PostgreSQL database server
def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

config  = load_config()

#     try:
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 # Executing the selected query
#                 cur.execute(query_list[query_number-1])
#                 rows = cur.fetchall()
#                 # Printing the results using query_output function
#                 query_output(rows, query_number)

#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/')
def abc():
    pass