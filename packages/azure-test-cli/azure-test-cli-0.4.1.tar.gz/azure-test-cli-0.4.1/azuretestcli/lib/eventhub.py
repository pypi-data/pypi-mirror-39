import asyncio

from azure.eventhub import Offset, EventHubClientAsync, EventData
from azure.eventhub.client import EventHubClient
from click import echo


class EventHubDelegate:
    """
        Delegate to communicate with eventhub
    """
    def __init__(self, namespace, name, sasname, saskey):
        super().__init__()
        self.client = EventHubClient(self._build_url(namespace, name), debug=False, username=sasname, password=saskey)
        self.async_client = EventHubClientAsync(self._build_url(namespace, name),
                                                debug=False, username=sasname, password=saskey)

    def send(self, message, repeat):
        sender = self.client.add_sender()
        self.client.run()
        try:
            count = 0
            while count < repeat:
                sender.send(EventData(message))
                echo('{} messages sent'.format(count + 1))
                count += 1
        except:
            raise
        finally:
            self.client.stop()

    def receive(self, consumergroup):
        OFFSET = Offset("-1")
        loop = asyncio.get_event_loop()
        info = self.async_client.get_eventhub_info()
        partitionIdList = info['partition_ids']
        echo("Reading from {} partitions.".format(len(partitionIdList)))
        tasks = [asyncio.ensure_future(self.pump("{}".format(i), consumergroup, OFFSET)) for i in partitionIdList]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.run_until_complete(self.async_client.stop_async())
        loop.close()

    async def pump(self, partition, consumergroup, offset):
        TIMEOUT = 30
        receiver = self.async_client.add_async_receiver(consumergroup, partition, offset, prefetch=5)
        await self.async_client.run_async()
        total = 0
        batch = await receiver.receive(timeout=TIMEOUT)
        while batch:
            for event_data in batch:
                last_offset = event_data.offset
                last_sn = event_data.sequence_number
                echo("Received: {}, {}".format(last_offset.value, last_sn))
                echo(event_data.body_as_str())
                total += 1
            batch = await receiver.receive(timeout=TIMEOUT)
        echo("Received {} messages from partition {}.".format(total, partition))

    @staticmethod
    def _build_url(namespace, eventhubname):
        return "amqps://{}.servicebus.windows.net/{}".format(namespace, eventhubname)
