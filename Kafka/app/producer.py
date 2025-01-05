import sys
sys.path.append("/opt")

import time
from confluent_kafka import SerializingProducer, DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.serialization import StringSerializer, StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from vnstock3 import Vnstock


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
avro_serializer = AvroSerializer(schema_registry_client, avro_schema_str)
avro_deserializer = AvroDeserializer(schema_registry_client, avro_schema_str)

# consumer group
CONSUMER_GROUP = 'producer-group'
# Khởi tạo Vnstock
stock = Vnstock().stock(source='VCI')


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

def runproducer():
    # Tải các key hiện có
    set_id = load_existing_keys()

    def delivery_report(err, msg):
        """Callback để báo cáo trạng thái gửi tin nhắn."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
         
    def fetch_and_send(symbols):
        """Lấy dữ liệu cổ phiếu và gửi đến Kafka."""
        producer_conf = {
            'bootstrap.servers': KAFKA_BROKER,
            'key.serializer': StringSerializer('utf_8'),
            'value.serializer': avro_serializer
        }
        producer = SerializingProducer(producer_conf)

        for symbol in symbols:
            print(f"Fetching data for {symbol}...")
            try:
                df = stock.quote.intraday(symbol=symbol, page_size=10000)
                if df is None or df.empty:
                    print(f"No data received for {symbol}. Skipping.")
                    continue

                df = df.iloc[::-1]
                df["time"] = df["time"].astype(int) // 10**6  # Chuyển thành milliseconds
                df['Ma_SIC'] = symbol

                for _, row in df.iterrows():

                    message = row.to_dict()
                    message_key = f"{message['time']}_{message['volume']}_{message['match_type']}_{message['Ma_SIC']}_{message['price']}"

                    if message_key not in set_id:
                        set_id.add(message_key)
                        try:
                            producer.produce(
                                topic=TOPIC,
                                key=message_key,
                                value=message,
                                on_delivery=delivery_report
                            )
                        except Exception as e:
                            print(f"Message production failed: {e}")
                    else:
                        break
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                continue
        producer.flush()

    # Đọc danh sách mã cổ phiếu từ file
    with open("/opt/Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
        SYMBOLS_FULL = [line.strip() for line in f]
    with open("/opt/Tasks/extract/NewData/stock_blocks.txt", "r") as f:
        SYMBOLS_BLOCK = [line.strip() for line in f]
    SYMBOLS = list(set(SYMBOLS_FULL) - set(SYMBOLS_BLOCK))

    while True:
        fetch_and_send(SYMBOLS)
        time.sleep(30)
    
if __name__ == "__main__":
    runproducer()