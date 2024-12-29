from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from datetime import datetime

# Địa chỉ Kafka Broker và Schema Registry
KAFKA_BROKER = 'kafka0:9093'
SCHEMA_REGISTRY_URL = 'http://schema-registry:8081'

# Tên các topic
TOPIC_PROCESSED = 'stock-processed'
# Đường dẫn đến tệp schema Avro
SCHEMA_PATH_PROCESSED = '/opt/Kafka/schema/avro_schema_processed.avsc'
# Consumer group
CONSUMER_GROUP = 'consumer-group'

def runconsumer():
    # Cấu hình Schema Registry Client
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    with open(SCHEMA_PATH_PROCESSED, 'r') as schema_file:
        avro_schema_str_processed = schema_file.read()

    avro_deserializer = AvroDeserializer(schema_registry_client, avro_schema_str_processed)
    # Cấu hình Consumer để đọc từ topic processed
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': CONSUMER_GROUP,
        'auto.offset.reset': 'earliest',
        'key.deserializer': StringDeserializer('utf_8'),
        'value.deserializer': avro_deserializer
    }
    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe([TOPIC_PROCESSED])
    # Kết nối PostgreSQL
    dwh_hook = PostgresHook(postgres_conn_id="load_to_dwh")
    dwh_conn = dwh_hook.get_conn()
    dwh_cursor = dwh_conn.cursor()

    # Làm sạch giá trị cũ trong bảng
    check_query = """
        SELECT time FROM fact_intraday_trading LIMIT 1
    """
    dwh_cursor.execute(check_query)
    date_in_fact = dwh_cursor.fetchone()
    if date_in_fact is not None:
        date_value = date_in_fact[0]
        if date_value.date() != datetime.now().date():
            truncate_query = "TRUNCATE TABLE fact_intraday_trading"
            dwh_cursor.execute(truncate_query)
            dwh_conn.commit()  # Commit sau khi truncate để xác nhận thay đổi

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            value = msg.value()
            if value is None:
                continue
            time = value.get('time')
            time = pd.to_datetime(time, unit='ms')
            insert_query = """
                INSERT INTO fact_intraday_trading (Time, price, volume, Match_type, Ma_SIC)
                VALUES (%s, %s, %s, %s, %s)
            """
            dwh_cursor.execute(insert_query, (time, value.get('price'), value.get('volume'), value.get('match_type'), value.get('Ma_SIC')))
            dwh_conn.commit()  # Commit sau mỗi lần insert
            print(f"Inserted record: {value}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        consumer.close()
        dwh_cursor.close()
        dwh_conn.close()