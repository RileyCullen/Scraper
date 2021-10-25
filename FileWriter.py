import json

# desc: Takes in a JSON object and writes it to a file
#
# Parameters:
# ---------------
# data : JSON
#   The JSON object you want to write to a file
# filename : string
#   The name of the file
def WriteToJSON(data, filename = 'data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)