from flask import Flask, request, jsonify
import mysql.connector
import datetime
from kafka import KafkaProducer
import json

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data.get('user_id')
    login_location = data.get('login_location')

    formatted_date = datetime.datetime.now()
    last_login_time = formatted_date.strftime("%d-%m-%Y %H:%M:%S")

    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO users (email, name, location) VALUES (%s, %s, %s)", (email, name, location))
    # connection.commit()
    # cursor.close()
    # if login_location == "North":
    #     kafka_producer(topic = 'north', data = f"{user_id} {last_login_time} {login_location}")
    # elif login_location == "South":
    #     kafka_producer(topic = 'south', data = f"{user_id} {last_login_time} {login_location}")
    # elif login_location == "East":
    #     kafka_producer(topic = 'east', data = f"{user_id} {last_login_time} {login_location}")
    # elif login_location == "West":
    #     kafka_producer(topic = 'west', data = f"{user_id} {last_login_time} {login_location}")
    # else:
    #     kafka_producer(topic = 'other', data = f"{user_id} {last_login_time} {login_location}")
    location_topic_map_1 = {

        # North India
        "delhi": "North",
        "lucknow": "North",
        "jaipur": "North",
        "chandigarh": "North",
        "shimla": "North",
        "dehradun": "North",
        "agra": "North",
        "gurgaon": "North",
        "noida": "North",
        "faridabad": "North",

        # South India
        "bangalore": "South",
        "chennai": "South",
        "hyderabad": "South",
        "kochi": "South",
        "coimbatore": "South",
        "mysore": "South",
        "madurai": "South",
        "vizag": "South",
        "trivandrum": "South",

        # East India
        "kolkata": "East",
        "bhubaneswar": "East",
        "guwahati": "East",
        "patna": "East",
        "ranchi": "East",
        "durgapur": "East",
        "jamshedpur": "East",
        "siliguri": "East",

        # West India
        "mumbai": "West",
        "pune": "West",
        "ahmedabad": "West",
        "surat": "West",
        "vadodara": "West",
        "rajkot": "West",
        "indore": "West",
        "bhopal": "West",
        "nagpur": "West",

        # Others
        "Other": "Other"
    }

    # location_topic_map = {
    #     "North": "north",
    #     "South": "south",
    #     "East": "east",
    #     "West": "west"
    # }
    topic = location_topic_map_1.get(login_location.lower(), "others")
    print(f"topic{topic}")
    print(f"login_location.lower(){login_location.lower()}")
    user_data_map = {
        "user_id": user_id,
        "last_login_time": last_login_time,
        "login_location": login_location
    }
    kafka_producer(topic, json.dumps(user_data_map))

    return "added"


#
# producer = KafkaProducer(bootstrap_servers='kafka:9092')
# topic = 'test-topic'
#
# while True:
#     message = f"Hello from producer at {time.time()}"
#     producer.send(topic, message.encode('utf-8'))
#     print(f"Produced: {message}")
#     time.sleep(2)

def kafka_producer(topic, data):
    producer = KafkaProducer(bootstrap_servers='kafka:29092')
    try:
        producer.send(topic, value=data.encode('utf-8'))
        producer.flush()

    except KeyboardInterrupt:
        print("Producer stopped.")


@app.route('/get', methods=['GET'])
def get_user():
    return "get"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)