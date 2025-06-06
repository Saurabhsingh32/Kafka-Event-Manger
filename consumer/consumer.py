import threading
from pydoc_data.topics import topics
from kafka import KafkaConsumer
import mysql.connector
import json
import time
from datetime import datetime

topics = ['North','South','East','West','others']
threads = []
BATCH_SIZE = 5
WAIT_DURATION = 20

# Kafka Consumer Configuration
def comsumer_details(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='kafka:29092',
        auto_offset_reset='earliest',
        group_id='my-group4'
    )
# MySQL Connection Configuration
    DB_HOST = "mysql"
    DB_PORT = 3306
    DB_NAME = "my_db"
    DB_USER = "user"
    DB_PASSWORD = "password"

    def connect_db(retries=5, delay=3):
        for i in range(retries):
            try:
                print("Connecting to MySQL DB")
                conn = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME,
                    port=DB_PORT
                )
                return conn
            except mysql.connector.Error as e:
                print(f"DB connection failed ({e}), retrying in {delay} seconds...")
                time.sleep(delay)
        raise Exception("Could not connect to DB")


    def db_info(data):
        connection = connect_db()
        cursor = connection.cursor()
        insert_query = "INSERT INTO North_user_details (user_id, login_location, login_time, topic) VALUES (%s, %s, %s, %s)"
        values = []
        for i in data:
            last_login = i['last_login_time']
            login_time_obj = datetime.strptime(last_login, '%d-%m-%Y %H:%M:%S')
            login_time = login_time_obj.strftime('%Y-%m-%d %H:%M:%S')
            values.append((i['user_id'], i['login_location'], login_time, topic_name))
        cursor.executemany(insert_query, values)
        connection.commit()
        connection.close()

    batch = []
    last_received_time = time.time()
    lock = threading.Lock()

    def timeout():
        nonlocal last_received_time, batch
        while True:
            time.sleep(WAIT_DURATION)
            with lock:
                if batch and (time.time() - last_received_time) > WAIT_DURATION:
                    db_info(batch)
                    batch = []
    threading.Thread(target=timeout, daemon= True).start()

    for message in consumer:
        data = json.loads(message.value)
        # Assuming data is a dictionary with keys matching your table columns
        with lock:
            batch.append(data)
            if len(batch) % BATCH_SIZE == 0:
                db_info(batch)
                batch =[]


for topic in topics:
    thread = threading.Thread(target=comsumer_details, args=(topic,))
    thread.start()
    threads.append(thread)

# Optional: Wait for all threads to complete
for thread in threads:
    thread.join()
















