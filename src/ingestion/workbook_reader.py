import pandas as pd
import json
import os
path = r"C:\Users\talma\Desktop\chart and diag\quantumlens-HSBC\data\raw\260505-1q-2026-data-pack-excel.xlsx"
output_dir = os.path.dirname(r"C:\Users\talma\Desktop\chart and diag\quantumlens-HSBC\src\ingestion\workbook_reader.py")
output_path = os.path.join(output_dir, 'workbook_metadata.json')
def read_workbook(path):
    workbook = pd.ExcelFile(path)

    metadata = []

    for sheet in workbook.sheet_names:
        sheet_df = workbook.parse(sheet)

        metadata.append({
            "sheet_name": sheet,
            "rows": int (sheet_df.shape[0]),
            "columns": int (sheet_df.shape[1]),
            "non_null_cells":int(sheet_df.notna().sum().sum()),
            "density":round(float(sheet_df.notna().sum().sum() / (sheet_df.shape[0] * sheet_df.shape[1])),2)
        })
        

    return metadata

#print(json.dumps(read_workbook(path), indent=4))
#with open(output_path, 'w') as f:
 #   json.dump(read_workbook(path), f, indent=4)

#print(f"Metadata saved to: {output_path}")
       
         