# spy_bot.py
import time
import json
import random
from azure.iot.device import IoTHubDeviceClient
from dotenv import load_dotenv
import os

# Load secret from .env
load_dotenv()
iot_conn_str = os.getenv('IOT_CONN_STR')

# Create the client
client = IoTHubDeviceClient.create_from_connection_string(iot_conn_str)

print("🔌 Spy Bot is waking up...")

while True:
    # Make a pretend message
    message = {
        "machine": "M1",
        "time": time.strftime('%H:%M:%S'),
        "temperature": random.randint(20, 100)
    }
    # Send it
    client.send_message(json.dumps(message))
    print("📨 Sent!", message)
    time.sleep(1)  # wait one second before sending again