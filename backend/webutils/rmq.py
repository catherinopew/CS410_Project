import pika
import yaml
import json


class RMQHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RMQHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.load_config()
    
    def load_config(self, config_path='config.yaml'):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        self.host = config['rabbitmq']['host']
        self.port = port=config['rabbitmq']['port']
        self.queue_name = config['rabbitmq']['queue_name']
        self.username = config['rabbitmq']['username']
        self.password = config['rabbitmq']['password']
        self.connection_attempts = config['rabbitmq']['connection_attempts']
        self.retry_delay = config['rabbitmq']['retry_delay']
        self.socket_timeout = config['rabbitmq']['socket_timeout']
        self.heartbeat = config['rabbitmq']['heartbeat']

    def connect(self):
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        conn_params = pika.ConnectionParameters(host=self.host, port=self.port, connection_attempts=self.connection_attempts, retry_delay=self.retry_delay, socket_timeout=self.socket_timeout, heartbeat=self.heartbeat) #, virtual_host=self.virtual_host, credentials=credentials)

        try:            
            self.connection = pika.BlockingConnection(conn_params)
            self.channel = self.connection.channel()
            print(f"Connected to RabbitMQ on {self.host}:{self.port}")
        except Exception as e:
            print(f"{e}")

    def close_connection(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("Connection to RabbitMQ closed.")
    
    def publish_message(self, message, queue_name="ws_messages"):
        try:
            if not self.connection.is_open:
                self.connect()

            message = json.dumps(message)
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)

            return {"status": "ok"}
        except Exception as e:
            print(f"{e}")    
            return {"status": f"{e}"}
