from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import json

# Constants
ENDPOINT = "a2iqq5l1s1a266-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "iotconsole-dbb5c442-e6db-40b6-b343-53c9a6367e4f"
PATH_TO_CERTIFICATE = "C:/Users/DELL/Desktop/@XYUG/project/goldatm/AWSCERTIFICATES/Devicecertificate.crt"
PATH_TO_PRIVATE_KEY = "C:/Users/DELL/Desktop/@XYUG/project/goldatm/AWSCERTIFICATES/Private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "C:/Users/DELL/Desktop/@XYUG/project/goldatm/AWSCERTIFICATES/AmazonRootCA1.pem"
TOPIC = "Gold_Atm_Publish"

# Initialize the MQTT connection
mqtt_connection = None
is_connected = False

def connect():
    global mqtt_connection, is_connected
    if not is_connected:
        # Initialize MQTT connection
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            client_id=CLIENT_ID,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            clean_session=False,
            keep_alive_secs=6
        )

        print(f"Connecting to {ENDPOINT} with client ID '{CLIENT_ID}'...")
        connect_future = mqtt_connection.connect()
        connect_future.result()
        is_connected = True
        print("Connected!")

def publish_message(coil_id):
    global mqtt_connection, is_connected
    if is_connected:
        message = json.dumps({"coil_id": coil_id})
        print(f"Publishing message to topic '{TOPIC}': {message}")
        mqtt_connection.publish(
            topic=TOPIC,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        print("Published!")

def disconnect():
    global mqtt_connection, is_connected
    if is_connected:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        is_connected = False
        print("Disconnected!")
    mqtt_connection = None
