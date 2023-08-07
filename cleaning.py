import json
import os
from datetime import datetime
def merge(path, out_fname):
    file_list = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            file_list.append(name)
    file_list.sort()

    data_list = []

    for filename in file_list:
        data = json.load(open(path + filename, encoding='utf-8'))
        for val in data:
            data_list.append(val)

    out_file = open(out_fname, "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()

def usa_to_aus_dates(fname):
    data = json.load(open(fname, encoding="utf-8"))
    data_list = []
    for entry in data:
        date = entry['dateTime']
        date_obj = datetime.strptime(date, "%m/%d/%y %H:%M:%S")
        entry['dateTime'] = date_obj.strftime("%d/%m/%Y")
        data_list.append(entry)
    out_file = open(fname, "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()

def add_factor():
    val_data = json.load(open("fairly-AM.json", encoding="utf-8"))
    val_data2 = json.load(open("lightly-AM.json", encoding="utf-8"))
    daily_data = json.load(open("data/daily-data-2.json", encoding="utf-8"))
    factor_list = []
    for i in range(len(val_data)):
        d = {}
        d['date'] = daily_data[i]['date']
        d['steps'] = daily_data[i]['steps']
        d['fairly_active_minutes'] = val_data[i]['value']
        d['lightly_active_minutes'] = val_data2[i]['value']
        d['hours_worn'] = daily_data[i]['hours_worn']
        factor_list.append(d)
    out_file = open("data/daily-data-2.json", "w")
    json.dump(factor_list, out_file, indent=2)
    out_file.close()

#merge("data/fairly-am/", "fairly-AM.json")
#usa_to_aus_dates("fairly-AM.json")
add_factor()
