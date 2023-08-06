__version__ = "0.0.3"

from minty import Base
import amqpstorm
import threading


class AMQPInfrastructure(Base):
    __slots__ = ["cache_lock", "connections"]

    def __init__(self):
        """Initialize the AMQP infrastructure"""
        self.cache_lock = threading.Lock()
        self.connections = {}

    def __call__(self, config: dict):
        """Create a new AMQP connection using the specified configuration

        :param config: Configuration to read amqp:// URL from
        :type config: dict
        :return: A handle for a channel on a connection to an AMQP server.
        :rtype: amqpstorm.Connection
        """

        rmq_url = config["amqp"]["url"]

        with self.cache_lock:
            try:
                connection = self.connections[rmq_url]
            except KeyError:
                self.connections[rmq_url] = amqpstorm.UriConnection(rmq_url)
                connection = self.connections[rmq_url]

        return connection.channel()

    def clean_up(self, channel):
        """Close the specified AMQP channel"""
        channel.close()
