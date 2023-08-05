# primed-avro
version number: 0.0.3.6
author: Matthijs van der Kroon

## Overview
A python package that provides:
* A basic Confluent Schema Registry client
* Confluent compatible Avro encoding and decoding
* High level KafkaConsumer that decodes Avro messages on the fly

WARNING: python2.7 not supported

## Installation / Usage

### To install use pip:

```bash
pip install primed_avro
```

Or clone the repo:
```bash
git clone https://gitlab.com/primedio/primed-avro
python setup.py install
```
### Example Confluent Schema Registry client
```python
from primed_avro.registry import ConfluentSchemaRegistryClient

csr = ConfluentSchemaRegistryClient(url="your_registry_url")
schemaMeta = csr.get_schema(subject=topic)
```

### Example Avro en/decoding
```python
from primed_avro.encoder import Encoder
from primed_avro.decoder import Decoder

encoder = Encoder(schema=schemaMeta.schema).get()
bytesvalue = encoder.encode(schemaMeta.id, record)

decoder = Decoder(schema=schemaMeta.schema).get()
record = decoder.decode(bytesvalue)
```

## Example High level KafkaAvroConsumer
```python
from primed_avro.consumer import AvroConsumer

c = AvroConsumer(
    topic="mytopic",
    bootstrap_servers="localhost:9092",
    registry_url="http://localhost:8081"
)

for msg in c.consume():
    print(type(msg), msg)
```

## Contributing
TBD

