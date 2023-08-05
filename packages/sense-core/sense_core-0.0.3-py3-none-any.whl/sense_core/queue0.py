import pika
from .config import config


class BaseRabbit(object):

    def __init__(self, label='rabbit'):
        host = config(label, 'host')
        port = int(config(label, 'port'))
        user = config(label, 'user')
        password = config(label, 'password')
        credentials = pika.PlainCredentials(user, password)
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, '/', credentials))
        self._channel = self._connection.channel()
        self._caller = None


class RabbitProducer0(BaseRabbit):

    def __init__(self, label='rabbit'):
        super(RabbitProducer0,self).__init__(label)

    def send(self, topic, message):
        self._channel.queue_declare(queue=topic, durable=True)
        self._channel.basic_publish(exchange='',
                                    routing_key=topic,
                                    body=message,
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,  # 使得消息持久化
                                    ))


class RabbitConsumer(BaseRabbit):

    def __init__(self, topic, label='rabbit'):
        self._topic = topic
        super(RabbitConsumer, self).__init__(label)

    def callback(self, ch, method, properties, body):
        self._caller(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def execute(self, caller, prefetch_count=2):
        self._caller = caller
        channel = self._connection.channel()
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(self.callback,
                              queue=self._topic,
                              no_ack=False)
        channel.start_consuming()
