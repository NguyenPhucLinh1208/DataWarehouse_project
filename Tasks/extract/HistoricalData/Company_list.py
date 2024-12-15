from vnstock3 import Vnstock
import pandas as pd

stock = Vnstock().stock(symbol='VCI', source='VCI')

MaCks = stock.listing.symbols_by_industries()
# Lọc theo cột 'organ_name' chứa chữ "bất động sản" (không phân biệt hoa thường)
filtered = MaCks[MaCks['icb_name3'].str.contains('bất động sản', case=False, na=False)]
filtered = filtered.reset_index(drop=True)
MaCk_bds = filtered['symbol']
path = '/opt/Tasks/extract/HistoricalData/MaCks.txt'
MaCk_bds.to_csv(path, index=False, header=False)