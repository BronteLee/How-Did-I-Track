import json
from datetime import datetime, date, timedelta
import random
import pandas as pd
import numpy as np
import sqlite3


def timeframe(data):
    result = []
    for entry in data:
        c_date = entry['date']
        format = "%d/%m/%Y"
        current_date = datetime.strptime(c_date, format).date()
        start_date = date(2022,1,1)
        if current_date >= start_date:
            result.append(entry)
    return result

def add_data(data):
    final_date = date(2023,9,6)
    c_date = data[-1]['date']
    format = "%d/%m/%Y"
    current_date = datetime.strptime(c_date, format).date()
    current_date += timedelta(days=1)
    while current_date <= final_date:
        new_day = {}
        new_day['date'] = current_date.strftime("%d/%m/%Y")
        new_day['steps'] = random.randint(5000,14000)
        new_day["fairly_active_minutes"] = random.randint(0,40)
        new_day["lightly_active_minutes"] = random.randint(200, 480)
        new_day["hours_worn"] = random.randint(8, 18)
        new_day["calories"] = 1627
        new_day["resting_heart_rate"] = random.randint(67, 70)
        new_day["minutes_asleep"] = random.randint(320, 500)
        new_day["minutes_awake"] = random.randint(42,75)
        current_date += timedelta(days=1)
        data.append(new_day)
    return data
    


def make_gaps(data):
    result = []
    date_range1 = [date(2023,2,13), date(2023,2,26)]
    date_range2 = [date(2023,4,8), date(2023,4,14)]
    for entry in data:
        c_date = entry['date']
        format = "%d/%m/%Y"
        current_date = datetime.strptime(c_date, format).date()
        if current_date >= date_range1[0] and current_date <= date_range1[1]:
            entry['steps'] = 0
            entry["fairly_active_minutes"] = "0"
            entry["lightly_active_minutes"] = "0"
            entry["hours_worn"] = 0
            entry["calories"] = 1627
            entry["resting_heart_rate"] = 0
            entry["minutes_asleep"] = 0
            entry["minutes_awake"] = 0
        if current_date >= date_range2[0] and current_date <= date_range2[1]:
            entry['steps'] = 0
            entry["fairly_active_minutes"] = "0"
            entry["lightly_active_minutes"] = "0"
            entry["hours_worn"] = 0
            entry["calories"] = 1627
            entry["resting_heart_rate"] = 0
            entry["minutes_asleep"] = 0
            entry["minutes_awake"] = 0
        result.append(entry)
    return result

def calculate_calories(day):
    if day['hours_worn'] == 0:
        return 1627
    if day['steps'] < 3000 and day['fairly_active_minutes'] < 5 and day['lightly_active_minutes'] < 200:
        return random.randint(1700, 1900)
    if day['steps'] > 16000 and day['fairly_active_minutes'] < 45 and day['lightly_active_minutes'] > 500:
        return random.randint(2800, 3100)
    if day['steps'] > 8000 and day['fairly_active_minutes'] > 15 and day['lightly_active_minutes'] > 400:
        return random.randint(2400, 2800)
    if day['steps'] > 9000 or day['fairly_active_minutes'] > 20 and day['lightly_active_minutes'] > 300:
        return random.randint(2100, 2400)
    return random.randint(1900, 2100)

def update_steps(data):
    avoid = [date(2022,6,30), date(2022,7,7)]
    date_range1 = [date(2022,1,1), date(2022,8,31)] # early in fitness journey
    date_range2 = [date(2022,9,1), date(2023,5,31)] # increasing fitness
    date_range3 = [date(2023,6,1), date(2023,9,12)] # Fun run training
    result = []
    for entry in data: 
        c_date = entry['date']
        format = "%d/%m/%Y"
        current_date = datetime.strptime(c_date, format).date()
        if current_date < avoid[0] or current_date > avoid[1]:
        # Walk less on weekdays
            if current_date.weekday() >= 0 and current_date.weekday() < 5 and entry['hours_worn'] > 8:
                if current_date >= date_range1[0] and current_date <= date_range1[1]: 
                    if entry['steps'] > 9000:
                        entry['steps'] = random.randint(3000, 5000)
                if current_date >= date_range2[0] and current_date <= date_range2[1]: 
                    if entry['steps'] > 14000 or entry['steps'] < 5000:
                        entry['steps'] = random.randint(7000, 11000)
            elif (current_date.weekday() == 5 or current_date.weekday() == 6) and entry['hours_worn'] > 8:
                if current_date >= date_range2[0] and current_date <= date_range2[1]: 
                    if entry['steps'] > 16000 or entry['steps'] < 6000:
                        entry['steps'] = random.randint(7000, 11000)
                elif entry['steps'] > 13000:
                    entry['steps'] = random.randint(7000, 12000)
            # Fun run training days
            if current_date >= date_range3[0] and current_date <= date_range3[1] and entry['hours_worn'] > 8:
                if current_date.weekday() == 1 or current_date.weekday() == 5:
                    if entry['steps'] < 12000:
                        entry['steps'] = random.randint(11000, 17000)
        result.append(entry)
    return result

def update_ams(data):
    result = []
    avoid = [date(2022,6,30), date(2022,7,7)]
    date_range1 = [date(2022, 2, 10), date(2023, 8, 31)] # Zumba
    date_range2 = [date(2022, 4, 1), date(2022, 8, 28)] # weekly gym
    date_range3 = [date(2022, 8, 29), date(2022, 10, 23)] # Exercise program
    date_range4 = [date(2022, 10, 28), date(2023, 9, 20)] # Twice weekly gym
    date_range5 = [date(2023, 2, 10), date(2023, 9, 20)] # Volleyball
    for entry in data:
        entry['fairly_active_minutes'] = int(entry['fairly_active_minutes'])
        entry['lightly_active_minutes'] = int(entry['lightly_active_minutes'])
        c_date = entry['date']
        format = "%d/%m/%Y"
        current_date = datetime.strptime(c_date, format).date()
        if entry['hours_worn'] > 8 and (current_date < avoid[0] or current_date > avoid[1]):
            # Mondays
            if current_date.weekday() == 0:
                if entry['fairly_active_minutes'] > 25:
                    entry['fairly_active_minutes'] = random.randint(0,10)
                if entry['lightly_active_minutes'] > 350:
                    entry['lightly_active_minutes'] = random.randint(150, 280)
                if current_date == date(2022,10,10):
                    entry['fairly_active_minutes'] = 67
                    entry['lightly_active_minutes'] = 546
            # Tuesdays
            if current_date.weekday() == 1:
                # Exercise Program 1st day and Gym 2nd day
                if (current_date >= date_range3[0] and current_date <= date_range3[1]) or (current_date >= date_range4[0] and current_date <= date_range4[1]):
                    if entry['fairly_active_minutes'] < 30:
                        entry['fairly_active_minutes'] = random.randint(35, 50)
                        entry['lightly_active_minutes'] += 40
                elif entry['fairly_active_minutes'] > 20:
                    entry['fairly_active_minutes'] = random.randint(6, 15)
                    entry['lightly_active_minutes'] -= 60
                if current_date == date(2022,10,11):
                    entry['fairly_active_minutes'] = 58
                    entry['lightly_active_minutes'] = 534
            #Wednesdays
            if current_date.weekday() == 2:
                # Zumba
                if current_date >= date_range1[0] and current_date <= date_range1[1]: 
                    entry['fairly_active_minutes'] = random.randint(35, 55) if entry['fairly_active_minutes'] < 30 else entry['fairly_active_minutes']
                    entry['lightly_active_minutes'] += 60
                elif entry['fairly_active_minutes'] > 30:
                    entry['fairly_active_minutes'] = random.randint(0, 15)
                    entry['lightly_active_minutes'] = random.randint(220, 300)
                if current_date == date(2022,10,12):
                    entry['fairly_active_minutes'] = 8
                    entry['lightly_active_minutes'] = 297
            # Thursdays
            elif current_date.weekday() == 3:
                # Exercise program 2nd day and Volleyball
                if current_date >= date_range3[0] and current_date <= date_range3[1]:
                    if entry['fairly_active_minutes'] < 40:
                        entry['fairly_active_minutes'] = random.randint(35, 65)
                        entry['lightly_active_minutes'] += 80
                elif current_date >= date_range5[0] and current_date <= date_range5[1]:
                    entry['hours_worn'] -= 3
                    if entry['fairly_active_minutes'] > 40:
                        entry['fairly_active_minutes'] = random.randint(10, 25)
                        entry['lightly_active_minutes'] -= 120
                elif entry['fairly_active_minutes'] > 30:
                    entry['fairly_active_minutes'] = random.randint(0, 20)
                    entry['lightly_active_minutes'] -= 40
                if current_date == date(2022,10,13):
                    entry['fairly_active_minutes'] = 53
                    entry['lightly_active_minutes'] = 576
            # Fridays
            elif current_date.weekday() == 4:
                if entry['fairly_active_minutes'] > 50:
                    entry['fairly_active_minutes'] = random.randint(8, 35)
                if entry['lightly_active_minutes'] > 350:
                    entry['lightly_active_minutes'] = random.randint(180, 300)
            # Saturdays
            elif current_date.weekday() == 5:
                # Gym
                if (current_date >= date_range2[0] and current_date <= date_range2[1]) or (current_date >= date_range4[0] and current_date <= date_range4[1]):
                    if entry['fairly_active_minutes'] < 25:
                        entry['fairly_active_minutes'] = random.randint(30, 60)
                        entry['lightly_active_minutes'] += 60
                else:
                    if entry['fairly_active_minutes'] > 50:
                        entry['fairly_active_minutes'] = random.randint(10, 30)
                    if entry['lightly_active_minutes'] > 400:
                        entry['lightly_active_minutes'] = random.randint(200, 350)
                if current_date == date(2022,10,10):
                    entry['fairly_active_minutes'] = 73
                    entry['lightly_active_minutes'] = 602
            # Sunday
            elif current_date.weekday() == 6:
                # Exercise program 3rd day
                if current_date >= date_range3[0] and current_date <= date_range3[1]:
                    if entry['fairly_active_minutes'] < 40:
                        entry['fairly_active_minutes'] = random.randint(35, 65)
                        entry['lightly_active_minutes'] += 80
                elif entry['fairly_active_minutes'] > 50:
                    entry['fairly_active_minutes'] = random.randint(10, 30)
                    entry['lightly_active_minutes'] = random.randint(250, 400)
        result.append(entry)
    return result
"""
data = json.load(open("data/synthetic-daily-data.json", encoding='utf-8'))
result = []
for day in data:
    if day['fairly_active_minutes'] > 30:
        day['minutes_asleep'] += 30
    result.append(day)
out_file = open("data/synthetic-daily-data.json", "w")
json.dump(result, out_file, indent=2)
out_file.close()"""


def analyse():
    df = pd.read_json("data/synthetic-daily-data.json", convert_dates=False)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    months = []
    month_index = 0
    week_index = 0
    weeks = []
    hours_worn = []
    longest_gap = 0
    gap = []
    current_gap = [None, None]
    index = 0
    last_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    while index < len(last_day):
        start_date = date(2022,index+1,1)
        end_date = date(2022,index+1,last_day[index])
        dff = df.query("date >= @start_date & date <= @end_date & hours_worn > 0")
        months.append(int(round(np.mean(dff['steps']), 0)))
        index += 1
    for i in months:
        print(i)

def add_prompt():
    prompt_con = sqlite3.connect('data/reflecting.db')
    prompt_cur = prompt_con.cursor()
    pa_type = 'steps'
    complete = 0
    start_date = '1/7/2022'
    end_date = '31/7/2022'
    prompt = 'Low Average Step Count Month'
    text = 'In July you recorded your lowest montly average step count for 2022. You took the least steps on the 1st.'
    question1 = 'Why do you think you did less steps in this month?'
    question2 = 'Is there something you could do or avoid doing in the future to increase your steps?'
    prompt_cur.execute("INSERT INTO prompts(type, complete, start_date, end_date, prompt, text, question1, question2) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (pa_type, complete, start_date, end_date, prompt, text, question1, question2))
    prompt_con.commit()
    prompt_con.close()

analyse()
