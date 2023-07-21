import json
import os

fileList = []
for root, dirs, files in os.walk('data', topdown=True):
    for name in files:
        fileList.append(name)
fileList.sort()

data_list = []

for filename in fileList:
    data = json.load(open('data/'+filename, encoding='utf-8'))
    for val in data:
        data_list.append(val)

out_file = open("steps-merged.json", "w")
json.dump(data_list, out_file, indent=2)
out_file.close()
