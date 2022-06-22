import json

with open("data_file.json", "r") as read_file:
    data = json.load(read_file)

print(data)
