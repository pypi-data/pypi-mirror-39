# TODO: Review possible operations for BlobStorage
# TODO: Add BlobStorageDelegate and appropriate operations

import time

from azure.storage.blob import BlockBlobService, AppendBlobService
from click import echo


class BlobStorageDelegate:
    def __init__(self, account_name, account_key):
        self.block_blob_service = BlockBlobService(account_name, account_key)
        self.append_blob_service = AppendBlobService(account_name, account_key)

    #Block operations
    def block_write(self, container, blob_path, file_path):
        self.block_blob_service.create_blob_from_path(container, blob_path, file_path)
        echo('Uploaded block blob to container {} at path {}'.format(container, blob_path))

    def block_read(self, container, blob_path, file_path):
        self.block_blob_service.get_blob_to_path(container, blob_path, file_path)
        echo('Downloaded block blob from container {} at path {} to local file {}'
             .format(container, blob_path, file_path))

    def block_delete(self, container, blob_path):
        self.block_blob_service.delete_blob(container, blob_path)
        echo("Deleted block blob from container {} at path {}".format(container, blob_path))

    #Append operations
    def append_write(self, container, blob_path, file_path, repeat=1):
        if file_path is not None:
            if not self.append_blob_service.exists(container, blob_path):
                self.append_blob_service.create_blob(container, blob_path)
                echo('Created append blob in container {} at path {} from local file {}'
                     .format(container, blob_path, file_path))
            for i in range(repeat):
                lease_id = self.append_blob_service.acquire_blob_lease(container, blob_path, 30)
                echo('Acquired lease with id {} for blob {}/{}'.format(lease_id, container, blob_path))
                try:
                    self.append_blob_service.append_blob_from_path(container, blob_path, file_path, lease_id=lease_id)
                    echo('Appended to blob {}/{} from local file {}'.format(container, blob_path, file_path))
                except RuntimeError as err:
                    print("Error occurred. {}".format(err))
                finally:
                    self.append_blob_service.release_blob_lease(container, blob_path, lease_id)
                    echo('Released lease with id {} for blob {}/{}'.format(lease_id, container, blob_path))

    def append_read(self, container, blob_path, file_path):
        self.append_blob_service.get_blob_to_path(container, blob_path, file_path)
        echo('Downloaded block blob from container {} at path {} to local path {}'.format(container, blob_path,
                                                                                          file_path))

    def append_delete(self, container, blob_path):
        self.append_blob_service.delete_blob(container, blob_path)

    def append_download(self, container, blob_path, file_path):
        self.append_blob_service.get_blob_to_path(container, blob_path, file_path)

    def append_stream(self, container, blob_path, timeout=60, retry_rate=5):
        elapsed_failure = 0
        blob_exists_fn = lambda: self.append_blob_service.exists(container, blob_path)
        blob_exists = blob_exists_fn()
        while not blob_exists and timeout > elapsed_failure:
            time.sleep(retry_rate)
            elapsed_failure += retry_rate
            retry_rate *= 2
            blob_exists = blob_exists_fn()
        if blob_exists:
            elapsed_failure = 0
            offset = 0
            properties = self.append_blob_service.get_blob_properties(container, blob_path).properties
            etag = None
            timed_out = lambda: timeout <= elapsed_failure
            while not timed_out():
                if properties.etag != etag:
                    elapsed_failure = 0
                    stream_block = self.append_blob_service.get_blob_to_text(container, blob_path, start_range=offset,
                                                                             end_range=properties.content_length)

                    echo(stream_block.content)
                    echo("Appended bytes {} through {}".format(offset, properties.content_length))
                    offset = properties.content_length
                    etag = properties.etag
                    properties = self.append_blob_service.get_blob_properties(container, blob_path).properties

                while properties.etag == etag and not timed_out():
                    time.sleep(retry_rate)
                    elapsed_failure += retry_rate
                    properties = self.append_blob_service.get_blob_properties(container, blob_path).properties
            if timed_out():
                echo("Stream timed out after {} seconds on blob {}/{}".format(timeout, container, blob_path))
        else:
            raise TimeoutError("Timed on streaming. Blob {}/{} does not exist.".format(container, blob_path))
