import sys
sys.path.append("/opt")

import pandas as pd
from confluent_kafka import SerializingProducer, DeserializingConsumer, KafkaError
from confluent_kafka.serialization import StringSerializer, StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
import time

# địa chỉ Kafka Broker và Schema Registry
KAFKA_BROKER = 'kafka0:9093'
SCHEMA_REGISTRY_URL = 'http://schema-registry:8081'

# Tên các topic
TOPIC_RAW = 'stock-raw'
TOPIC_PROCESSED = 'stock-processed'

# Đường dẫn đến tệp schema Avro
SCHEMA_PATH_RAW = '/opt/Kafka/schema/avro_schema_raw.avsc'
SCHEMA_PATH_PROCESSED = '/opt/Kafka/schema/avro_schema_processed.avsc'

# consumer group
CONSUMER_GROUP = 'processor-group'



###########################################################################################
def runprocessor():

    # Cấu hình Schema Registry Client
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    # Tải schema Avro từ tệp
    with open(SCHEMA_PATH_RAW, 'r') as schema_file:
        avro_schema_str_raw = schema_file.read()

    with open(SCHEMA_PATH_PROCESSED, 'r') as schema_file:
        avro_schema_str_processed = schema_file.read()

    # Khởi tạo AvroSerializer và AvroDeserializer
    avro_serializer = AvroSerializer(schema_registry_client, avro_schema_str_processed)
    avro_deserializer = AvroDeserializer(schema_registry_client, avro_schema_str_raw)


    # Cấu hình Producer để gửi đến topic processed
    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': avro_serializer
    }
    producer = SerializingProducer(producer_conf)

    # Cấu hình Consumer để đọc từ topic raw
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': CONSUMER_GROUP,
        'auto.offset.reset': 'earliest',
        'key.deserializer': StringDeserializer('utf_8'),
        'value.deserializer': avro_deserializer
    }

    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([TOPIC_RAW])

    def delivery_report(err, msg):
        """Callback để báo cáo trạng thái gửi tin nhắn."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    def process_record(record):
        """Hàm xử lý dữ liệu."""
        key = record.key()  # Lấy key từ record
        value = record.value()  # Lấy value từ record

        if value is None:
            print("Received record with no value.")
            return

        # Xử lý dữ liệu từ value
        try:
            match_type = value.get('match_type')
            record_time = value.get('time')
            record_time = pd.to_datetime(record_time, unit='ms')

            if match_type == "ATO/ATC" and record_time.hour != 14:
                match_type = "ATO"
            elif match_type == "ATO/ATC" and record_time.hour == 14:
                match_type = "ATC"

            record_time = int(record_time.timestamp() * 1000)  # Chuyển đổi về milliseconds
            processed_key = key
            processed_data = {
                "time": record_time,
                "price": value.get('price'),
                "volume": value.get('volume'),
                "match_type": match_type,
                "Ma_SIC": value.get('Ma_SIC')
            }

            producer.produce(
                topic=TOPIC_PROCESSED,
                key=processed_key,
                value=processed_data,
                on_delivery=delivery_report
            )
        except Exception as e:
            print(f"Error processing record: {e}")

    try:
        start_time = time.time()
        while True:
            msg = consumer.poll(timeout=10.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"Consumer error: {msg.error()}")
                continue

            process_record(msg)
            # Kiểm tra thời gian đã trôi qua
            if time.time() - start_time >= 10:
                producer.flush()
                start_time = time.time()  # Đặt lại thời điểm bắt đầu sau khi flush
    except KeyboardInterrupt:
        producer.flush()
        consumer.close()
        print("Processing interrupted by user.")
    finally:
        producer.flush()
        consumer.close()

