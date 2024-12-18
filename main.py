import json

with open("voices/crystal/routes.json") as f:
    j = json.load(f)
print(j)