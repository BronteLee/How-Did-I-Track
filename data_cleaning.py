from datetime import datetime
import pytz
import json
import os


# merges multiple json files into one
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


# Remove zero values from json file
def remove_zeros(filename, out_fname):
    data = json.load(open(filename, encoding='utf-8'))
    data_list = []
    for entry in data:
        if entry['value'] != '0':
            data_list.append(entry)
    out_file = open(out_fname, "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()


# Adds a date column to json file
def add_date(file):
    data = json.load(open(file, encoding='utf-8'))
    print(data[0])
    print(data[0]['dateTime'])
    print(data[0]['dateTime'].split(" ")[0])
    data[0]['date'] = data[0]['dateTime'].split(" ")[0]
    print(data[0])

# daily steps
def daily_steps():
    steps = []
    data = json.load(open("steps.json", encoding='utf-8'))
    for entry in data:
        if len(steps) > 5:
            break
        date = entry['dateTime'].split(" ")[0]
        if len(steps) == 0:
            d = {'date': date, 'steps': int(entry['value'])}
            steps.append(d)
        else:
            c_date = steps[-1]['date']
            if date == c_date:
                steps[-1]['steps'] += int(entry['value'])
            else:
                d = {'date': date, 'steps': int(entry['value'])}
                steps.append(d)
    print(steps)


# Convert timestamps to Local
def convert_times():
    data = json.load(open("steps.json", encoding='utf-8'))
    data_list = []
    for entry in data:
        date = entry['dateTime']
        format = "%m/%d/%y %H:%M:%S"
        utc = datetime.strptime(date, format)
        utc = utc.replace(tzinfo=pytz.timezone("utc"))
        adjusted_time = utc.astimezone(pytz.timezone("Australia/Sydney"))
        entry['dateTime'] = adjusted_time.strftime("%d/%m/%Y %H:%M:%S")
        data_list.append(entry)
    out_file = open("steps-sydney-time.json", "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()


convert_times()