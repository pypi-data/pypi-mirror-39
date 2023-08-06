import uuid

from azure.servicebus import ServiceBusService, Message
from click import echo


class ServiceBusDelegate:
    """
        Delegate to interact with servicebus
    """
    def __init__(self, namespace, sasname, saskey):
        self.service_bus_service = ServiceBusService(namespace, shared_access_key_name=sasname, shared_access_key_value=saskey)

    def send_queue_message(self, name, message, repeat):
        for i in range(repeat):
            self.service_bus_service.send_queue_message(name, Message(message))
            echo('Sent message: "{}", iteration: {}'.format(message, i))

    def receive_queue_messages(self, name):
        TIMEOUT = 60
        total = 0
        try:
            message = self.service_bus_service.read_delete_queue_message(name, timeout=TIMEOUT)
            while message.body is not None:
                echo('Received message: "{}" from queue {}'.format(message.body, name))
                total += 1
                message = self.service_bus_service.read_delete_queue_message(name, timeout=TIMEOUT)
            echo('Received {} messages from "{}" queue'.format(total, name))
        except KeyboardInterrupt as exc:
            raise

    def send_topic_message(self, topicname, message, repeat):
        for i in range(repeat):
            self.service_bus_service.send_topic_message(topicname, Message(message))
            echo('Sent message: "{}", iteration: {}'.format(message, i))

    def receive_topic_messages(self, topicname):
        TIMEOUT_IN_SEC = 60
        total = 0
        subscription_name = str(uuid.uuid4())
        self.service_bus_service.create_subscription(topicname, subscription_name)
        echo("Created temporary subscription: {} for topic {}".format(subscription_name, topicname))
        try:
            message = self.service_bus_service.read_delete_subscription_message(topicname, subscription_name,
                                                                            timeout=TIMEOUT_IN_SEC)
            while message.body is not None:
                total += 1
                echo('Received message: "{}" from topic {}'.format(message.body, topicname))
                message = self.service_bus_service.read_delete_subscription_message(topicname, subscription_name,
                                                                            timeout=TIMEOUT_IN_SEC)
            echo("{} messages received from topic {}.".format(total, topicname))
        except KeyboardInterrupt as exc:
            raise
        finally:
            self.service_bus_service.delete_subscription(topicname, subscription_name)
            echo("Deleted temporary subscription: {} for topic {}".format(subscription_name, topicname))

