import pandas as pd
import json

# Load the updated CSV file
df = pd.read_csv('QFm Radio Schedule.csv')  # Update this filename as needed

# Clean the 'day' column by removing all spaces
df['day'] = df['day'].astype(str).str.replace(' ', '').str.strip()
# Group by 'day' and build the structure
days_data = []
for day_name, group in df.groupby('day'):
    day_id = str(group['day_id'].iloc[0])  # Same id for all rows in group

    # Build the list of program dictionaries
    programs = []
    for _, row in group.iterrows():
        programs.append({
            "id": row["program_id"],
            "startTime": row["startTime"],
            "endTime": row["endTime"],
            "title": row["title"],
            "host": row["host"],
            "description": row["description"],
            "imageUrl": row["imageUrl"]
        })

    # Add to days list
    days_data.append({
        "id": day_id,
        "day": day_name,
        "programs": programs
    })

# Final JSON structure
final_json = {
    "days": days_data
}

# Save as JSON file
with open('radio_schedule.json', 'w', encoding='utf-8') as f:
    json.dump(final_json, f, indent=4, ensure_ascii=False)

print("Conversion complete. JSON saved to 'radio_schedule.json'.")
