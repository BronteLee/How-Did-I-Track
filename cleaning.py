import operator
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
    daily_data = json.load(open("data/daily-data-2.json", encoding="utf-8"))
    factor_list = []
    for i in range(len(val_data)):
        d = {}
        d['date'] = daily_data[i]['date']
        d['steps'] = daily_data[i]['steps']
        d['fairly_active_minutes'] = daily_data[i]['fairly_active_minutes']
        d['lightly_active_minutes'] = daily_data[i]['lightly_active_minutes']
        d['hours_worn'] = daily_data[i]['hours_worn']
        factor_list.append(d)
    out_file = open("data/daily-data-2.json", "w")
    json.dump(factor_list, out_file, indent=2)
    out_file.close()

def sleep_merge(path):
    file_list = []
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            file_list.append(name)
    file_list.sort()
    data_list = []
    for filename in file_list:
        data = json.load(open(path + filename, encoding='utf-8'))
        index = len(data)-1
        while index >= 0:
            val = data[index]
            if val['mainSleep']:
                if len(data_list) > 0:
                    if val['dateOfSleep'] != data_list[-1]['date']:
                        d = {}
                        d['date'] = val['dateOfSleep']
                        d['minutes_asleep'] = val['minutesAsleep']
                        d['minutes_awake'] = val['minutesAwake']
                        data_list.append(d)
                else:
                    d = {}
                    d['date'] = val['dateOfSleep']
                    d['minutes_asleep'] = val['minutesAsleep']
                    d['minutes_awake'] = val['minutesAwake']
                    data_list.append(d)
            index -= 1
    out_file = open("sleep.json", "w")
    json.dump(data_list, out_file, indent=2)
    out_file.close()

def extract_sleep():
    data = json.load(open("sleep.json", encoding="utf-8"))
    sleep_list = []
    for entry in data:
        d = {}
        if entry['mainSleep']:
            date_obj = datetime.strptime(entry['dateOfSleep'], "%Y-%m-%d")
            d['date'] = date_obj
            d['minutes_asleep'] = entry['minutesAsleep']
            d['minutes_awake'] = entry['minutesAwake']
            sleep_list.append(d)
    
    sleep_list.sort(key=operator.itemgetter('date'))

    for entry in sleep_list:
        entry['date'] = entry['date'].strftime("%d/%m/%Y")
    for i in range(len(sleep_list)-1):
        if sleep_list[i]['date'] == sleep_list[i+1]['date']:
            print(sleep_list[i]['date'])
    #print(sleep_list)
    print(len(sleep_list))

#merge("data/fairly-am/", "fairly-AM.json")
#usa_to_aus_dates("fairly-AM.json")
#add_factor()
#extract_sleep()

def add_sleep():
    daily = json.load(open("data/daily-data-2.json", encoding="utf-8"))
    sleep = json.load(open("sleep.json", encoding="utf-8"))
    new_data = []
    idaily = 0
    isleep = 0

    while idaily < len(daily):
        sleep_date = datetime.strptime(sleep[isleep]['date'], "%d/%m/%Y").strftime("%d/%m/%Y")
        if sleep_date != daily[idaily]['date']:
            new_data.append(daily[idaily])
        else:
            d = daily[idaily]
            d['minutes_asleep'] = sleep[isleep]['minutes_asleep']
            d['minutes_awake'] = sleep[isleep]['minutes_awake']
            new_data.append(d)
            isleep += 1
        idaily += 1
    out_file = open("data/daily-data-2.json", "w")
    json.dump(new_data, out_file, indent=2)
    out_file.close()
add_sleep()