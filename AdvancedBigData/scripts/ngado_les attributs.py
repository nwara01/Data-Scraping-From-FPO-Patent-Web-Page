import json

# Read the JSON file
with open('MD_finale_wlah.json', 'r',encoding='utf-8') as json_file:
    data = json.load(json_file)

# Define the key you want to replace
old_key = 'application date'
new_key = 'application_date'
# Iterate through each dictionary in the data
for item in data:
    if old_key in item:
        item[new_key] = item.pop(old_key)

# Write the modified data back to the JSON file
with open('MD_eafak_baraka.json', 'w',encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)  # You can adjust the indent level as needed
