import sys
sys.path.append("/opt")

import pandas as pd
from vnstock3 import Vnstock
from datetime import datetime

def new_price(stocks, group_id):
    TotalPrice = pd.DataFrame()
    currentdate = datetime.now().strftime('%Y-%m-%d')
    stock_block = []

    for stock_code in stocks:
        try:
            stock = Vnstock().stock(symbol=stock_code, source='VCI')
            Price_df = stock.quote.history(start=f'{currentdate}', end=f'{currentdate}')
            Price_df["Mã Chứng Khoán"] = stock_code
            TotalPrice = pd.concat([TotalPrice, Price_df], ignore_index=True)
        except Exception as e:
            print(f"Mã cổ phiếu {stock_code} hiện bị dừng giao dịch")
            stock_block.append(stock_code)

    # Lưu mã cổ phiếu bị dừng giao dịch vào tệp tạm thời
    with open(f"/opt/Tasks/extract/NewData/stock_blocks_{group_id}.txt", 'w') as file:
        for stock in stock_block:
            file.write(stock + '\n')
    if len(TotalPrice) == 0 or TotalPrice['time'].dt.strftime('%Y-%m-%d').values[0] != currentdate:
        return pd.DataFrame()
    else:
        TotalPrice['Status'] = 'New'
        return TotalPrice



