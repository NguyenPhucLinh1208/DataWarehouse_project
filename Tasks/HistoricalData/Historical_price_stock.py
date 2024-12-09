import sys
sys.path.append("/opt")

import pandas as pd
from vnstock3 import Vnstock

def historical_price(stock_codes):

    TotalHisPrice = pd.DataFrame()
    for stock_code in stock_codes:
        stock = Vnstock().stock(symbol=stock_code, source='VCI')
        HisPriceDF = stock.quote.history(start='2015-01-01', end='2024-12-7')
        HisPriceDF["Mã Chứng Khoán"] = stock_code
        TotalHisPrice = pd.concat([TotalHisPrice, HisPriceDF], ignore_index=True)
    return TotalHisPrice

