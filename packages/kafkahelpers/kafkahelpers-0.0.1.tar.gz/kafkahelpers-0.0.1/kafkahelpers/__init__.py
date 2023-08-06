import asyncio
import logging
import attr
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)

@attr.s
class ReconnectingClient(object):
    """
    Wraps an aiokafka client such that it will reconnect forever.

    Provides a way to add worker functions to use the wrapped client forever.

    example:

        client = ReconnectingClient(aiokafka.AIOKafkaConsumer(), "consumer")
        loop.create_task(client.run(my_consumer_func))
    """

    client = attr.ib()
    name = attr.ib()
    retry_interval = attr.ib(default=5)
    connected = attr.ib(init=False, default=False)

    async def start(self):
        """
        Connects the wrapped client.
        """
        while not self.connected:
            try:
                logger.info("Attempting to connect %s client.", self.name)
                await self.client.start()
                logger.info("%s client connected successfully.", self.name)
                self.connected = True
            except KafkaError:
                logger.exception("Failed to connect %s client, retrying in %d seconds.", self.name, self.retry_interval)
                await asyncio.sleep(self.retry_interval)

    async def work(self, worker):
        """
        Executes the worker function.
        """
        try:
            await worker(self.client)
        except KafkaError:
            logger.exception("Encountered exception while working %s client, reconnecting.", self.name)
            self.connected = False

    def get_callback(self, worker, cond=lambda v: True):
        """
        Returns a callback function that will ensure that the wrapped client is
        connected forever.

        example:

            loop.spawn_callback(client.get_callback(my_cb))
        """
        async def _f():
            v = cond(None)
            while cond(v):
                await self.start()
                v = await self.work(worker)
                print(v, cond(v))
        return _f

    def run(self, worker, cond=lambda v: True):
        """
        Returns a coroutine that will ensure that the wrapped client is
        connected forever.

        example:

            loop.create_task(client.run(my_func))
        """
        return self.get_callback(worker, cond)()
