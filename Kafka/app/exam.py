import sys
sys.path.append("/opt")

import time
from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer



# địa chỉ Kafka Broker và Schema Registry
KAFKA_BROKER = 'kafka0:9093'
TOPIC = 'stock-raw'

SCHEMA_REGISTRY_URL = 'http://schema-registry:8081'
SCHEMA_PATH = '/opt/Kafka/schema/avro_schema_raw.avsc'
# Cấu hình Schema Registry Client
schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
# Tải schema Avro từ tệp
with open(SCHEMA_PATH, 'r') as schema_file:
    avro_schema_str = schema_file.read()
# Khởi tạo AvroSerializer và AvroDeserializer

avro_deserializer = AvroDeserializer(schema_registry_client, avro_schema_str)

# consumer group
CONSUMER_GROUP = 'producer-group'



def load_existing_keys():
    """Tải các key hiện có từ topic vào set."""
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': f"{CONSUMER_GROUP}-{time.time()}",
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'key.deserializer': StringDeserializer('utf_8'),
        'value.deserializer': avro_deserializer
    }
    consumer = DeserializingConsumer(consumer_conf)
    # Đăng ký topic cần đọc
    consumer.subscribe([TOPIC])
    set_id = set()
    try:
        while True:
            msg = consumer.poll(timeout=15.0)
            if msg is None:
                break
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    break
                else:
                    raise KafkaException(msg.error())
            set_id.add(msg.key())  # Thêm key vào set
    except Exception as e:
        print(f"Error loading existing keys from topic: {e}")
    finally:
        consumer.close()  # Đóng consumer khi kết thúc
        print(f"Loaded {len(set_id)} existing keys from topic.")
    return set_id

set_id = load_existing_keys()
print(len(set_id))