import sys
import os
sys.path.append("/opt")

import pandas as pd

def combine_csv_files(filename):
    """Gộp các file CSV tạm thời thành một file duy nhất."""
    temp_files = [f"/opt/Tasks/HistoricalData/{filename}_{i}.csv" for i in range(2)]
    combined = pd.concat([pd.read_csv(f) for f in temp_files], ignore_index=True)
    combined.to_csv(f"/opt/Tasks/HistoricalData/{filename}.csv", index=False)
    # Xóa các file tạm
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            print("Đã xóa thành công")
        except OSError as e:
            print(f"Không thể xóa {temp_file}: {e}")

def combine_all_files():
    combine_csv_files('Total_Balance')
    combine_csv_files('Total_CashFlow')
    combine_csv_files('Total_Income')

if __name__ == "__main__":
    combine_all_files()
