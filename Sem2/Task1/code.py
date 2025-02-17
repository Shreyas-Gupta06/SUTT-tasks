import pandas as pd
import json
from collections import defaultdict
import re


file_path = "Mess Menu Sample.xlsx"  
xls = pd.ExcelFile(file_path)

# Load the sheet into a DataFrame
df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

# Convert the first row to date format and use it as column headers
df.columns = pd.to_datetime(df.iloc[0], errors='coerce').dt.strftime('%d-%m-%Y')
df = df[1:].reset_index(drop=True)

# List of days to exclude
days_of_week = ["SATURDAY", "SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]

# Dictionary to store the parsed menu. Creates a nested dictionary structure, so we don’t have to manually check if keys exist before adding values.
menu_dict = defaultdict(lambda: defaultdict(list))


current_meal = None

for col in df.columns:
    for item in df[col]:
        if pd.isna(item) or re.fullmatch(r'\*+', str(item)) or item in days_of_week:
            continue  # Skip  asterisks and day names

        if item in ["BREAKFAST", "LUNCH", "DINNER"]:
            current_meal = item.capitalize()
        elif current_meal:
            menu_dict[col][current_meal].append(item) #eg: menu["01-02-2025"]["Breakfast"].append("CORNFLAKES")

json_output_path = "mess_menu.json"
with open(json_output_path, "w", encoding="utf-8") as json_file:
    json.dump(menu_dict, json_file, indent=4, ensure_ascii=False)

print(f"Mess menu has been successfully saved to {json_output_path}")