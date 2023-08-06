from click import option, group

from azuretestcli import BlobStorageDelegate
from azuretestcli import EventHubDelegate
from azuretestcli import ServiceBusDelegate


@group()
def cli():
    pass


@cli.group(help='Perform eventhub tests')
def eventhub():
    pass


@eventhub.command(name='send', help='Send messages to eventhub')
@option('--eventhub_namespace', '-s', required=True, help='Name of event hub namespace')
@option('--eventhub_name', '-n', required=True, help='Name of eventhub')
@option('--eventhub_sas_name', '-p', required=True, help='Name of eventhub SAS policy with send rights')
@option('--eventhub_sas_key', '-k', required=True, help='Key value of eventhub SAS policy with send rights')
@option('--message', '-m', required=True, help='Message to send. Must be in quotes')
@option('--repeat', '-r', type=int, default=1, help='Count of times to repeat the send of the message')
def eventhub_send(eventhub_namespace, eventhub_name, eventhub_sas_name, eventhub_sas_key, message, repeat):
    delegate = EventHubDelegate(eventhub_namespace, eventhub_name, eventhub_sas_name, eventhub_sas_key)
    delegate.send(message, repeat)


@eventhub.command(name='receive', help='Receive messages from eventhub')
@option('--eventhub_namespace', '-s', required=True, help='Name of event hub namespace')
@option('--eventhub_name', '-n', required=True, help='Name of eventhub')
@option('--eventhub_sas_name', '-p', required=True, help='Name of eventhub SAS policy with listen rights')
@option('--eventhub_sas_key', '-k', required=True, help='Key value of eventhub SAS policy with listen rights')
@option('--consumer_group', '-c', required=True, help='Name of event hub consumer group')
def eventhub_receive(eventhub_namespace, eventhub_name, eventhub_sas_name, eventhub_sas_key, consumer_group):
    delegate = EventHubDelegate(eventhub_namespace, eventhub_name, eventhub_sas_name, eventhub_sas_key)
    delegate.receive(consumer_group)


@cli.group(help='Perform servicebus tests')
def servicebus():
    pass


@servicebus.group(name='queue', help='Perform servicebus queue tests')
def servicebus_queue():
    pass


@servicebus_queue.command(name='send', help='Send messages onto servicebus queue')
@option('--servicebus_namespace', '-s', required=True, help='Name of servicebus namespace')
@option('--servicebus_queue_name', '-n', required=True, help='Name of queue')
@option('--servicebus_sas_name', '-p', required=True, help='Name of servicebus SAS policy with send access')
@option('--servicebus_sas_key', '-k', required=True, help='Key value of servicebus SAS policy with send access')
@option('--message', '-m', required=True, help='Message to send. Must be in quotes')
@option('--repeat', '-r', type=int, default=1, help='Count of times to repeat the send of the message')
def servicebus_queue_send(servicebus_namespace, servicebus_queue_name, servicebus_sas_name, servicebus_sas_key,
                          message, repeat):
    delegate = ServiceBusDelegate(servicebus_namespace, servicebus_sas_name, servicebus_sas_key)
    delegate.send_queue_message(servicebus_queue_name, message, repeat)


@servicebus_queue.command(name='receive', help='Receive messages onto servicebus queue')
@option('--servicebus_namespace', '-s', required=True, help='Name of servicebus namespace')
@option('--servicebus_queue_name', '-n', required=True, help='Name of queue')
@option('--servicebus_sas_name', '-p', required=True, help='Name of servicebus SAS policy with listen access')
@option('--servicebus_sas_key', '-k', required=True, help='Key value of servicebus SAS policy with listen access')
def servicebus_queue_receive(servicebus_namespace, servicebus_queue_name, servicebus_sas_name, servicebus_sas_key):
    delegate = ServiceBusDelegate(servicebus_namespace, servicebus_sas_name, servicebus_sas_key)
    delegate.receive_queue_messages(servicebus_queue_name)


@servicebus.group(name='topic', help='Perform servicebus topic tests')
def servicebus_topic():
    pass


@servicebus_topic.command(name='send', help='Send messages onto servicebus topic')
@option('--servicebus_namespace', '-s', required=True, help='Name of servicebus namespace')
@option('--servicebus_topic_name', '-n', required=True, help='Name of topic')
@option('--servicebus_sas_name', '-p', required=True, help='Name of servicebus SAS policy with send access')
@option('--servicebus_sas_key', '-k', required=True, help='Key value of servicebus SAS policy with send access')
@option('--message', '-m', required=True, help='Message to send. Must be in quotes')
@option('--repeat', '-r', type=int, default=1, help='Count of times to repeat the send of the message')
def servicebus_topic_send(servicebus_namespace, servicebus_topic_name, servicebus_sas_name, servicebus_sas_key,
                          message, repeat):
    delegate = ServiceBusDelegate(servicebus_namespace, servicebus_sas_name, servicebus_sas_key)
    delegate.send_topic_message(servicebus_topic_name, message, repeat)


@servicebus_topic.command(name='receive', help='Receive messages onto servicebus topic')
@option('--servicebus_namespace', '-s', required=True, help='Name of servicebus namespace')
@option('--servicebus_topic_name', '-n', required=True, help='Name of topic')
@option('--servicebus_sas_name', '-p', required=True, help='Name of servicebus SAS policy with listen access')
@option('--servicebus_sas_key', '-k', required=True, help='Key value of servicebus SAS policy with listen access')
def servicebus_topic_receive(servicebus_namespace, servicebus_topic_name, servicebus_sas_name, servicebus_sas_key):
    delegate = ServiceBusDelegate(servicebus_namespace, servicebus_sas_name, servicebus_sas_key)
    delegate.receive_topic_messages(servicebus_topic_name)


@cli.group(help='Perform blobstorage tests')
def storage():
    pass


@storage.group(help='Perform block blob tests')
def blockblob():
    pass


@blockblob.command(name='upload', help='Upload file to a block blob')
@option('--storage_account', '-a', required=True, help='Name of blob account')
@option('--storage_key', '-k', required=True, help='Storage access key')
@option('--container', '-c', required=True, help='Blob container name')
@option('--path', '-b', required=True, help='Blob path of uploaded file')
@option('--file', '-f', required=True, help='Content to upload to path')
def blobstorage_upload(storage_account, storage_key, container, path, file):
    blob_storage_delegate = BlobStorageDelegate(storage_account, storage_key)
    blob_storage_delegate.block_write(container, path, file)


@blockblob.command(name='download', help='Download content to a block blob')
@option('--storage_account', '-a', required=True, help='Name of blob account')
@option('--storage_key', '-k', required=True, help='Storage access key')
@option('--container', '-c', required=True, help='Blob container name')
@option('--path', '-b', required=True, help='Blob path of uploaded file')
@option('--file', '-f', required=True, help='Content to upload to path')
def blobstorage_download(storage_account, storage_key, container, path, file):
    blob_storage_delegate = BlobStorageDelegate(storage_account, storage_key)
    blob_storage_delegate.block_read(container, path, file)


@storage.group(help='Perform append blob tests')
def appendblob():
    pass


@appendblob.command(name='delete', help='Delete an append blob')
@option('--storage_account', '-a', required=True, help='Name of blob account')
@option('--storage_key', '-k', required=True, help='Name of access key')
@option('--container', '-c', required=True, help='Blob container name')
@option('--blob_path', '-b', required=True, help='Blob path of file')
def blobstorage_delete(storage_account, storage_key, container, blob_path):
    blob_storage_delegate = BlobStorageDelegate(storage_account, storage_key)
    blob_storage_delegate.append_delete(container, blob_path)


@appendblob.command(name='append', help='Upload content to an append blob')
@option('--storage_account', '-a', required=True, help='Name of blob account')
@option('--storage_key', '-k', required=True, help='Name of SAS policy with write access')
@option('--container', '-c', required=True, help='Blob container name')
@option('--blob_path', '-b', required=True, help='Blob path of uploaded file')
@option('--file_path', '-f', required=True, help='Content to upload to path')
@option('--repeat', '-r', type=int, default=1, help='Count of times to repeat the append the content')
def blobstorage_append(storage_account, storage_key, container, blob_path, file_path, repeat):
    blob_storage_delegate = BlobStorageDelegate(storage_account, storage_key)
    blob_storage_delegate.append_write(container, blob_path, file_path, repeat)


@appendblob.command(name='download', help='Download append blob to local file')
@option('--storage_account', '-a', required=True, help='Name of blob account')
@option('--storage_key', '-k', required=True, help='Name of SAS policy with write access')
@option('--container', '-c', required=True, help='Blob container name')
@option('--blob_path', '-b', required=True, help='Blob path of uploaded file')
@option('--file_path', '-f', required=True, help='Content to upload to path')
def blobstorage_download(storage_account, storage_key, container, blob_path, file_path):
    blob_storage_delegate = BlobStorageDelegate(storage_account, storage_key)
    blob_storage_delegate.append_download(container, blob_path, file_path)


@appendblob.command(name='stream', help='Stream append blob to output')
@option('--storage_account', '-a', required=True, help='Name of blob account')
@option('--storage_key', '-k', required=True, help='Name of SAS policy with write access')
@option('--container', '-c', required=True, help='Blob container name')
@option('--blob_path', '-b', required=True, help='Blob path of uploaded file')
def blobstorage_stream(storage_account, storage_key, container, blob_path):
    blob_storage_delegate = BlobStorageDelegate(storage_account, storage_key)
    blob_storage_delegate.append_stream(container, blob_path)


if __name__ == '__main__':
    cli()
