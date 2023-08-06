# azure-test-cli
Command line interface to test azure resources, such as servicebus, 
eventhub, blob storate, queue storage, and table storage.

## Install

#### pip install
```bash
pip install azure-test-cli
```

#### Manually
```
git clone https://github.com/wildengineer/azure-test-cli.git
cd azure-test-cli
install_cli.sh
```
Use ```install_cli.sh -o``` if you want to override an existing install of the cli.

## Usage

### Azure Storage
Provides many tests for testing storage resources
```
Usage: aztest storage [OPTIONS] COMMAND [ARGS]...

  Perform blobstorage tests

Options:
  --help  Show this message and exit.

Commands:
  appendblob  Perform append blob tests
  blockblob   Perform block blob tests
```

#### BlockBlob Subcommands
```
Usage: aztest storage blockblob [OPTIONS] COMMAND [ARGS]...

  Perform block blob tests

Options:
  --help  Show this message and exit.

Commands:
  download  Download content to a block blob
  upload    Upload file to a block blob
```

##### Upload
```bash
Usage: aztest storage blockblob upload [OPTIONS]

  Upload file to a block blob

Options:
  -a, --storage_account TEXT  Name of blob account  [required]
  -k, --storage_key TEXT      Storage access key  [required]
  -c, --container TEXT        Blob container name  [required]
  -b, --path TEXT             Blob path of uploaded file  [required]
  -f, --file TEXT             Content to upload to path  [required]
  --help                      Show this message and exit.
```

##### Download
```bash
Usage: aztest storage blockblob download [OPTIONS]

  Download content to a block blob

Options:
  -a, --storage_account TEXT  Name of blob account  [required]
  -k, --storage_key TEXT      Storage access key  [required]
  -c, --container TEXT        Blob container name  [required]
  -b, --path TEXT             Blob path of uploaded file  [required]
  -f, --file TEXT             Content to upload to path  [required]
  --help                      Show this message and exit.

```


#### AppendBlob Subcommands
```
Usage: aztest storage appendblob [OPTIONS] COMMAND [ARGS]...

  Perform append blob tests

Options:
  --help  Show this message and exit.

Commands:
  append    Upload content to an append blob
  delete    Delete an append blob
  download  Download append blob to local file
  stream    Stream append blob to output
```

##### Append
Append a file to an append blob. If the append blob doesn't exist, 
then it's created.

```
Usage: aztest storage appendblob append [OPTIONS]

  Upload content to an append blob

Options:
  -a, --storage_account TEXT  Name of blob account  [required]
  -k, --storage_key TEXT      Name of SAS policy with write access  [required]
  -c, --container TEXT        Blob container name  [required]
  -b, --blob_path TEXT        Blob path of uploaded file  [required]
  -f, --file_path TEXT        Content to upload to path  [required]
  -r, --repeat INTEGER        Count of times to repeat the append the content
  --help                      Show this message and exit.
```

##### Stream
Stream a blob to stdout. After a timeout the operation will exit. Allows for viewing live
appends.
```bash
Usage: aztest storage appendblob stream [OPTIONS]

  Stream append blob to output

Options:
  -a, --storage_account TEXT  Name of blob account  [required]
  -k, --storage_key TEXT      Name of SAS policy with write access  [required]
  -c, --container TEXT        Blob container name  [required]
  -b, --blob_path TEXT        Blob path of uploaded file  [required]
  --help                      Show this message and exit.

```


##### Download
Download a file from an append blob.
```bash
Usage: aztest storage appendblob download [OPTIONS]

  Download append blob to local file

Options:
  -a, --storage_account TEXT  Name of blob account  [required]
  -k, --storage_key TEXT      Name of SAS policy with write access  [required]
  -c, --container TEXT        Blob container name  [required]
  -b, --blob_path TEXT        Blob path of uploaded file  [required]
  -f, --file_path TEXT        Content to upload to path  [required]
  --help                      Show this message and exit.
```

##### Delete
Delete an append blob.
```bash
Usage: aztest storage appendblob delete [OPTIONS]

  Delete an append blob

Options:
  -a, --storage_account TEXT  Name of blob account  [required]
  -k, --storage_key TEXT      Name of access key  [required]
  -c, --container TEXT        Blob container name  [required]
  -b, --blob_path TEXT        Blob path of file  [required]
  --help                      Show this message and exit.
```


### Eventhub
Provides several tests for azure eventhub.
```bash
Usage: aztest eventhub [OPTIONS] COMMAND [ARGS]...

  Perform eventhub tests

Options:
  --help  Show this message and exit.

Commands:
  receive  Receive messages from eventhub
  send     Send messages to eventhub

```

#### Send
```bash
Usage: aztest eventhub send [OPTIONS]

  Send messages to eventhub

Options:
  -s, --eventhub_namespace TEXT  Name of event hub namespace  [required]
  -n, --eventhub_name TEXT       Name of eventhub  [required]
  -p, --eventhub_sas_name TEXT   Name of eventhub SAS policy with send rights
                                 [required]
  -k, --eventhub_sas_key TEXT    Key value of eventhub SAS policy with send
                                 rights  [required]
  -m, --message TEXT             Message to send. Must be in quotes
                                 [required]
  -r, --repeat INTEGER           Count of times to repeat the send of the
                                 message
  --help                         Show this message and exit.
```

#### Receive
```bash
Usage: aztest eventhub receive [OPTIONS]

  Receive messages from eventhub

Options:
  -s, --eventhub_namespace TEXT  Name of event hub namespace  [required]
  -n, --eventhub_name TEXT       Name of eventhub  [required]
  -p, --eventhub_sas_name TEXT   Name of eventhub SAS policy with listen
                                 rights  [required]
  -k, --eventhub_sas_key TEXT    Key value of eventhub SAS policy with listen
                                 rights  [required]
  -c, --consumer_group TEXT      Name of event hub consumer group  [required]
  --help                         Show this message and exit.
```

### Service Bus
Provides several tests for azure service bus.
```bash
Usage: aztest servicebus [OPTIONS] COMMAND [ARGS]...

  Perform servicebus tests

Options:
  --help  Show this message and exit.

Commands:
  queue  Perform servicebus queue tests
  topic  Perform servicebus topic tests
```

#### Queue Subcommands
```bash
Usage: aztest servicebus queue [OPTIONS] COMMAND [ARGS]...

  Perform servicebus queue tests

Options:
  --help  Show this message and exit.

Commands:
  receive  Receive messages onto servicebus queue
  send     Send messages onto servicebus queue
```

##### Send
```bash
Usage: aztest servicebus queue send [OPTIONS]

  Send messages onto servicebus queue

Options:
  -s, --servicebus_namespace TEXT
                                  Name of servicebus namespace  [required]
  -n, --servicebus_queue_name TEXT
                                  Name of queue  [required]
  -p, --servicebus_sas_name TEXT  Name of servicebus SAS policy with send
                                  access  [required]
  -k, --servicebus_sas_key TEXT   Key value of servicebus SAS policy with send
                                  access  [required]
  -m, --message TEXT              Message to send. Must be in quotes
                                  [required]
  -r, --repeat INTEGER            Count of times to repeat the send of the
                                  message
  --help                          Show this message and exit.
```
##### Receive
```bash
Usage: aztest servicebus queue receive [OPTIONS]

  Receive messages onto servicebus queue

Options:
  -s, --servicebus_namespace TEXT
                                  Name of servicebus namespace  [required]
  -n, --servicebus_queue_name TEXT
                                  Name of queue  [required]
  -p, --servicebus_sas_name TEXT  Name of servicebus SAS policy with listen
                                  access  [required]
  -k, --servicebus_sas_key TEXT   Key value of servicebus SAS policy with
                                  listen access  [required]
  --help                          Show this message and exit.

```

