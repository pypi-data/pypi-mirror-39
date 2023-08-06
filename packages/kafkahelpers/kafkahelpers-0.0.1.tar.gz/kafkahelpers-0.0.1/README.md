# Kafka Helpers

A package with classes designed to make working with aiokafka simpler.

## Getting Started

```python
from kafkahelpers import ReconnectingClient

kafka_client = aiokafka.AIOKafkaConsumer()
client = ReconnectingClient(kafka_client, "my_client")

async def my_func(client):
    print("Hello World!")


event_loop.create_task(client.run(my_func))
```

## Installing

The package is simple.  All you need to do is install with your favorite package manager.

```
pip install kafkahelpers
```

## Running the Tests

```
pytest
```
