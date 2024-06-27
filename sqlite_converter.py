import json

with open('whole.json', 'r') as f:
  data = json.load(f)

print(f"Loaded {len(data)} objects from 'whole.json'")

seen_user_ids = set()
cleaned_data = []

for obj in data:
  if obj['model'] == 'myapp.userprofile' and 'fields' in obj and 'user_id' in obj['fields']:
    user_id = obj['fields']['user_id']
    if user_id in seen_user_ids:
      print(f"Skipping duplicate user_id: {user_id}")
      continue
    print(f"Adding user_id: {user_id}")
    seen_user_ids.add(user_id)
  cleaned_data.append(obj)

print(f"Cleaned data contains {len(cleaned_data)} objects")

with open('cleaned_whole.json', 'w') as f:
  json.dump(cleaned_data, f)

print("Saved cleaned data to 'cleaned_whole.json'")