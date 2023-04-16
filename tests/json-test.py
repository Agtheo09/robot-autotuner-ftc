import json
  
data = None

with open('./tests/constants.json') as f:
    data = json.load(f)


for i in data['tags']['field']:
    print(i)
  
f.close()