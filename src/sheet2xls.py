from gsheets import Sheets
import pandas as pd
import os
import json
import csv

# Local run only
cwd = os.getcwd()
if cwd.split("/")[-1] == "src":
    from dotenv import load_dotenv
    load_dotenv()
    os.chdir("..")

client = json.loads(os.environ["CLIENT"])

with open("client.json", "w") as json_file:
    json.dump(client, json_file, indent=4)

try:
    storage = json.loads(os.environ["STORAGE"])
    with open("storage.json", "w") as json_file:
        json.dump(storage, json_file, indent=4)
except:
    print("No storage file on first run - authenticate in browser.")

directory = os.environ["SAVE_DIR"]
file_path = directory + os.environ["FILE_NAME"]
sheet_id = os.environ["SHEET_ID"]
sheet_obj = Sheets.from_files("client.json", "storage.json")
sheet = sheet_obj.get(sheet_id)
sheet.sheets[0].to_csv(file_path + ".csv", encoding="utf-8", dialect="excel")
txt_delimiter = ","

largest_column_count = 0
with open(file_path + ".csv", "r") as temp_f:
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
    file_path + ".csv", header=None, delimiter=txt_delimiter, names=column_names
)
df.to_excel(file_path + ".xlsx", index=False, header=False)

namespaces = {}

# rewrite vocabulary.csv with trailing columns and without first 17 lines
with open(file_path + ".csv") as csv_input:
    csvreader = csv.reader(csv_input, delimiter=txt_delimiter)
    with open(file_path + "_temp.csv", "w") as csv_output:
        csvwriter = csv.writer(csv_output, delimiter=txt_delimiter)
        preface_lines = True
        for row in csvreader:
            if len(row) > 2 and row[0] == "PREFIX":
                namespaces[row[1]] = row[2]
            if len(row) > 1 and row[0] == "Identifier" and row[1] == "skos:prefLabel@en":
                # this is the first line that should be written
                preface_lines = False
            if preface_lines == False:
                # once past the preface lines, write lines to new csv with trailing commas
                if len(row) < largest_column_count:
                    num_cols_to_add = largest_column_count - len(row)
                    i = 0
                    while i < num_cols_to_add:
                        row.append("")
                        i +=1
                csvwriter.writerow(row)
    csv_output.close()
csv_input.close()

os.remove(file_path + ".csv")
os.rename(file_path + "_temp.csv", file_path + ".csv")

# replace namespaces
with open(file_path + ".csv") as csv_input:
    csvreader = csv.DictReader(csv_input)
    with open(file_path + "_temp.csv", "w") as csv_output:
        csvwriter = csv.DictWriter(csv_output, fieldnames=csvreader.fieldnames, delimiter=txt_delimiter)
        csvwriter.writeheader()
        for term in csvreader:
            for namespace in namespaces.keys():
                prefix = namespace + ":"
                if prefix in term["Identifier"]:
                    term["Identifier"] = term["Identifier"].replace(prefix, namespaces[namespace])
                if prefix in term["purl_target"]:
                    term["purl_target"] = term["purl_target"].replace(prefix, namespaces[namespace])
            csvwriter.writerow(term)

os.remove(file_path + ".csv")
os.rename(file_path + "_temp.csv", file_path + ".csv")

os.remove("client.json")
os.remove("storage.json")
