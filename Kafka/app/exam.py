import sys
sys.path.append("/opt")

from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

# Địa chỉ Kafka Broker và Schema Registry
KAFKA_BROKER = 'kafka0:9093'
SCHEMA_REGISTRY_URL = 'http://schema-registry:8081'
# Tên topic Kafka
TOPIC = 'stock-raw'
# Đường dẫn đến tệp schema Avro
SCHEMA_PATH = '/opt/Kafka/schema/avro_schema_raw.avsc'
# Consumer group
CONSUMER_GROUP = 'consumer-group'

# Cấu hình Schema Registry Client
schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Tải schema Avro từ tệp
with open(SCHEMA_PATH, 'r') as schema_file:
    avro_schema_str = schema_file.read()

# Khởi tạo AvroDeserializer
avro_deserializer = AvroDeserializer(schema_registry_client, avro_schema_str)

# Cấu hình Consumer
consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': CONSUMER_GROUP,
    'auto.offset.reset': 'earliest',  # Đọc từ đầu
    'enable.auto.commit': False,
    'key.deserializer': StringDeserializer('utf_8'),
    'value.deserializer': avro_deserializer
}

# Khởi tạo Consumer
consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe([TOPIC])

try:
    while True:
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            print("No message received.")
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("End of partition reached.")
                break
            else:
                raise KafkaException(msg.error())
        print(f"Message key: {msg.key()}")
except Exception as e:
    print(f"Error: {e}")
finally:
    consumer.close()
    print("Consumer closed.")