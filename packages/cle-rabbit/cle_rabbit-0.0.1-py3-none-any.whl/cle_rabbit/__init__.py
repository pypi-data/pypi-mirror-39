import pika
import json

class Rabbit(object):

    def __init__(self, queue, host='localhost', port='5672', user=None, password=None):
        self.queue = queue
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.connection = None
        self.channel = None

        self.connect()

    def __del__(self):
        self.disconnect()


    def connect(self):
        if self.connection:
            return

        params = [
            self.host,
            self.port,
            '/'
        ]
        if self.user:
            params.append(pika.PlainCredentials(self.user, self.password or ""))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(*params))
        self.channel = self.connection.channel()


    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None


    def create_queue(self, durable=False):
        self.channel.queue_declare(queue=self.queue, durable=durable)


    def send(self, message):
        if type(message) != type(""):
            message = json.dumps(message, ensure_ascii=False)

        self.channel.basic_publish(exchange='',
                      routing_key=self.queue,
                      body=message)


    def subscribe(self, callback, no_ack=False):
        def _callback(ch, method, properties, body):
            try:
                body = json.loads(body)
            except:
                pass
            res = callback(ch, method, properties, body)
            if not no_ack and res == True:
                ch.basic_ack(delivery_tag = method.delivery_tag)

        self.channel.basic_consume(_callback,
                    queue=self.queue,
                    no_ack=no_ack
                )
        self.channel.start_consuming()