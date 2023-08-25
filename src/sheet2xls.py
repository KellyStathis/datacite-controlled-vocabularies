from gsheets import Sheets
import pandas as pd
import os
import json
import csv

# Local run only
from dotenv import load_dotenv
load_dotenv()

client = json.loads(os.environ["CLIENT"])

with open("client.json", "w") as json_file:
    json.dump(client, json_file, indent=4)

try:
    storage = json.loads(os.environ["STORAGE"])
    with open("storage.json", "w") as json_file:
        json.dump(storage, json_file, indent=4)
except:
    print("No storage file on first run - authenticate in browser.")


file_name = os.environ["FILE_NAME"]
sheet_id = os.environ["SHEET_ID"]
sheet_obj = Sheets.from_files("client.json", "storage.json")
sheet = sheet_obj.get(sheet_id)
sheet.sheets[0].to_csv(file_name + ".csv", encoding="utf-8", dialect="excel")
txt_delimiter = ","

largest_column_count = 0
with open(file_name + ".csv", "r") as temp_f:
    lines = csv.reader(temp_f, delimiter=txt_delimiter)
    for l in lines:
        column_count = len(l) + 1
        largest_column_count = (
            column_count
            if largest_column_count < column_count
            else largest_column_count
        )
temp_f.close()


column_names = [i for i in range(0, largest_column_count)]
df = pd.read_csv(
    file_name + ".csv", header=None, delimiter=txt_delimiter, names=column_names
)
df.to_excel(file_name + ".xlsx", index=False, header=False)

# rewrite vocabulary.csv with trailing columns
with open("vocabulary.csv") as csv_input:
    csvreader = csv.reader(csv_input, delimiter=txt_delimiter)
    with open("vocabulary_fixed.csv", "w") as csv_output:
        csvwriter = csv.writer(csv_output, delimiter=txt_delimiter)
        for row in csvreader:
            if len(row) < largest_column_count:
                num_cols_to_add = largest_column_count - len(row)
                i = 0
                while i < num_cols_to_add:
                    row.append("")
                    i +=1
            csvwriter.writerow(row)
    csv_output.close()
csv_input.close()

os.remove("vocabulary.csv")
os.rename("vocabulary_fixed.csv", "vocabulary.csv")
os.remove("client.json")
os.remove("storage.json")
