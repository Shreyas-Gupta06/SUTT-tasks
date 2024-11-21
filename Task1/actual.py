import pandas as pd
import json

def convert_time(slot_number):
    try:
        start_hour = 8 + (int(slot_number) - 1)
        return f"{start_hour:02d}:00-{start_hour:02d}:50"
    except ValueError:
        return "Unknown Time"

def get_section_type(section_number):
    if section_number.startswith("L"):
        return "Lecture"
    elif section_number.startswith("P"):
        return "Practical"
    elif section_number.startswith("U"):
        return "Others"
    return "Unknown"

def parse_days_hours(days_hours):
    days = {}
    for part in days_hours.split(","):
        day_letter = "".join([char for char in part if char.isalpha()])
        slot_numbers = [int(char) for char in part if char.isdigit()]
        if day_letter and slot_numbers:
            if day_letter not in days:
                days[day_letter] = []
            days[day_letter].extend(slot_numbers)
    return [{"day": day, "slots": slots} for day, slots in days.items()]

def parse_excel_to_json(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        data = []

        for sheet_name in xls.sheet_names:
            sheet = pd.read_excel(xls, sheet_name=sheet_name)

            course_code = sheet.iloc[3, 1] if pd.notna(sheet.iloc[3, 1]) else "Unknown Code"
            course_title = sheet.iloc[3, 2] if pd.notna(sheet.iloc[3, 2]) else "Unknown Title"
            credits = f"{sheet.iloc[3, 3] if pd.notna(sheet.iloc[3, 3]) else '0'}-" \
                      f"{sheet.iloc[3, 4] if pd.notna(sheet.iloc[3, 4]) else '0'}-" \
                      f"{sheet.iloc[3, 5] if pd.notna(sheet.iloc[3, 5]) else '0'}"

            course_data = {
                "course_code": course_code,
                "course_title": course_title,
                "credits": credits,
                "sections": [],
            }

            last_section = None

            for idx, row in sheet.iterrows():
                if idx < 4:
                    continue

                section_code = row[6] if pd.notna(row[6]) else None
                instructor = row[7] if pd.notna(row[7]) else ""
                room = row[8] if pd.notna(row[8]) else "TBA"
                days_hours = row[9] if pd.notna(row[9]) else ""

                section_type = get_section_type(section_code) if section_code else "Unknown"
                timings = parse_days_hours(days_hours)

                if not section_code and last_section is not None:
                    last_section["instructors"].append(instructor)
                else:
                    section = {
                        "section_type": section_type,
                        "section_number": section_code if section_code else "Unknown",
                        "instructors": [instructor],
                        "room": room,
                        "timing": timings,
                    }
                    course_data["sections"].append(section)
                    last_section = section

            data.append(course_data)

        with open("timetable_v4.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Check the JSON file.")

    except Exception as e:
        print(f"Error: {e}")

file_path = "dummy.xlsx"
parse_excel_to_json(file_path)
