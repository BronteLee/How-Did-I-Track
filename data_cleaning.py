import operator
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


# daily steps and adherence
def daily_steps():
    steps = []
    data = json.load(open("steps-sydney-time.json", encoding='utf-8'))
    hours = 0
    hour = ""
    for entry in data:
        date = entry['dateTime'].split(" ")[0]
        if len(steps) == 0:
            d = {'date': date, 'steps': int(entry['value'])}
            steps.append(d)
            hour = entry['dateTime'].split(" ")[1].split(":")[0]
            hours += 1
        else:
            c_date = steps[-1]['date']
            c_hour = entry['dateTime'].split(" ")[1].split(":")[0]
            if date == c_date:
                steps[-1]['steps'] += int(entry['value'])
                if c_hour != hour:
                    hours += 1
                    hour = c_hour
            else:
                steps[-1]['hours-worn'] = hours
                d = {'date': date, 'steps': int(entry['value'])}
                steps.append(d)
                hours = 0
                hour = c_hour
    steps[-1]['hours-worn'] = hours
    out_file = open("data/daily-data.json", "w")
    json.dump(steps, out_file, indent=2)
    out_file.close()



# Convert timestamps to Local
def convert_times(fname, outname):
    data = json.load(open(fname, encoding='utf-8'))
    data_list = []
    for entry in data:
        date = entry['dateTime']
        format = "%m/%d/%y %H:%M:%S"
        utc = datetime.strptime(date, format)
        utc = utc.replace(tzinfo=pytz.timezone("utc"))
        adjusted_time = utc.astimezone(pytz.timezone("Australia/Sydney"))
        entry['dateTime'] = adjusted_time.strftime("%d/%m/%Y %H:%M:%S")
        data_list.append(entry)
    out_file = open(outname, "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()

# minute to daily data
def minute_to_daily(fname):
    data = json.load(open(fname, encoding="utf-8"))
    data_list = []
    date = ""
    for entry in data:
        c_date = entry['dateTime'].split(" ")[0]
        if c_date == date:
            data_list[-1]['calories'] += float(entry['value'])
        else:
            date = c_date
            d = {'date': date, 'calories': float(entry['value'])}
            data_list.append(d)
    out_file = open(fname, "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()


# Add contextual factor to daily data
def add_factor(source_file, val):
    val_data = json.load(open(source_file, encoding="utf-8"))
    daily_data = json.load(open("data/daily-data.json", encoding="utf-8"))
    factor_list = []
    for i in range(len(val_data)):
        d = daily_data[i]
        d[val] = val_data[i][val]
        factor_list.append(d)
    out_file = open("data/daily-data.json", "w")
    json.dump(factor_list, out_file, indent=2)
    out_file.close()


# sort data when not in order
def sort_fix():
    data = json.load(open("data/daily-data.json", encoding="utf-8"))
    data_list = []
    for entry in data:
        data_list.append(entry)
        date = entry['date']
        d_format = "%d/%m/%Y"
        date_obj = datetime.strptime(date, d_format)
        #entry['date'] = date_obj.strftime("%Y/%m/%d")
        data_list[-1]['date'] = date_obj.strftime("%Y/%m/%d")

    data_list.sort(key=operator.itemgetter('date'))

    for d in data_list:
        n_date = d['date']
        print(n_date)
        d_format = "%Y/%m/%d"
        date_obj = datetime.strptime(n_date, d_format)
        d['date'] = date_obj.strftime("%d/%m/%Y")
    out_file = open("data/daily-data.json", "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()


def get_nested_data():
    data = json.load(open("resting-heart.json", encoding="utf-8"))
    heart_list = []
    print(len(data))
    count = 0
    for entry in data:
        h_date = entry["value"]["date"]
        h_date_obj = datetime.strptime(h_date, "%m/%d/%y")
        n_heart = {"date": h_date_obj.strftime("%d/%m/%Y"), "resting-heart-rate": int(round(entry['value']['value'],0))}
        heart_list.append(n_heart)
    out_file = open("resting-heart.json", "w")
    json.dump(heart_list, out_file, indent=2)
    out_file.close()

add_factor("resting-heart.json", "resting-heart-rate")

