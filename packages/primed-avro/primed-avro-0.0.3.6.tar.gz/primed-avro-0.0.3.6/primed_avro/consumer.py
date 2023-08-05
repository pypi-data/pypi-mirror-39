import uuid
import time
from kafka import KafkaConsumer

from primed_avro.decoder import FastAvroDecoder
from primed_avro.registry import ConfluentSchemaRegistryClient

class AvroConsumer:

    def __init__(
        self,
        topic,
        bootstrap_servers,
        registry_url,
        group_id=str(uuid.uuid4()),
        auto_offset_reset="latest"
    ):
        self._consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=auto_offset_reset,
            consumer_timeout_ms=10000,
        )

        self._registry_client = ConfluentSchemaRegistryClient(url=registry_url)
        self._decoder = FastAvroDecoder(schema_registry=self._registry_client)

    def consume(self, interval=1):
        while True:
            for msg in self._consumer:
                yield self._decoder.decode(msg.value)
            time.sleep(interval)
