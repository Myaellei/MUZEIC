import pandas as pd, json

# read the CSV file you made
df = pd.read_csv("data.csv")

# convert it to JSON format and save as data.json
df.to_json("data.json", orient="records", indent=4)

print("✅ data.json created successfully from data.csv")
