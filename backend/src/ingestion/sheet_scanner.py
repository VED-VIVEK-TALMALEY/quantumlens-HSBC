
from datetime import datetime

import pandas as pd
import json 
import os 
import sys 

path = r"C:\Users\talma\Desktop\chart and diag\quantumlens-HSBC\data\raw\260505-1q-2026-data-pack-excel.xlsx"
scan_output_dir = os.path.dirname(r"C:\Users\talma\Desktop\chart and diag\quantumlens-HSBC\src\ingestion\sheet_scanner.py")
scan_output_path = os.path.join(scan_output_dir, 'scan_sheet_metadata.json')

def scan_sheets(path):
    sheet_scan_json=[]
   
    xcel= pd.ExcelFile(path)
    sheet_names = xcel.sheet_names  
    for name in sheet_names:
              
               sheet_df = xcel.parse(name)
               for row_number, row in sheet_df.iterrows():
                if row.notna().sum() == 0:
                    continue
                row_values = [
                 value.isoformat() if isinstance(value, (pd.Timestamp, datetime))
                else value
                for value in row.tolist()
                ]
                cleaned_row_values = []
                for value in row_values:
                    if pd.isna(value):
                         cleaned_row_values.append(None)
                    else :
                         cleaned_row_values.append(value)


                sheet_scan_json.append({
                    "source_workbook": path.split("\\")[-1],
                    "sheet_name": name,
                    "row_number": int(row_number + 1),
                    "row_values": cleaned_row_values,
                    "non_null_count": int(row.notna().sum())
                    })
    return sheet_scan_json

scan_sheets (path)


