# from vnstock3 import Vnstock
# import pandas as pd
# stock = Vnstock().stock(source='VCI')
# df = stock.quote.intraday(symbol='FDC', page_size=100)

# print(df.head())

# kafka-topics --bootstrap-server kafka0:9093 --delete --topic stock-raw
# kafka-topics --bootstrap-server kafka0:9093 --list 
# kafka-consumer-groups --bootstrap-server kafka0:9093 --list
# kafka-consumer-groups --bootstrap-server kafka0:9093 --delete --group producer-group
# kafka-topics --bootstrap-server kafka0:9093 --create --topic stock-raw --partitions 1 --replication-factor 1
# kafka-console-consumer --bootstrap-server kafka0:9093 --topic stock-processed --from-beginning --max-messages 10
# kafka-topics --bootstrap-server kafka0:9093 --create --topic stock-processed --partitions 1 --replication-factor 1
# kafka-console-consumer --bootstrap-server kafka0:9093 --topic stock-raw --from-beginning --max-messages 10
import sys
sys.path.append("/opt")

try:
    with open("/opt/Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
        SYMBOLS_FULL = [line.strip() for line in f]
    with open("/opt/Tasks/extract/NewData/stock_blocks.txt", "r") as f:
        SYMBOLS_BLOCK = [line.strip() for line in f]
    SYMBOLS = list(set(SYMBOLS_FULL) - set(SYMBOLS_BLOCK))
    print(f"Symbols loaded from MaCks.txt: {SYMBOLS_FULL}")
    print(f"Symbols loaded from stock_blocks.txt: {SYMBOLS_BLOCK}")
    print(f"Filtered Symbols: {SYMBOLS}")
except FileNotFoundError as e:
    print(f"Error loading symbol files: {e}")
    sys.exit(1)
