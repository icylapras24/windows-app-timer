#stores all times into a log, adding the times if there are multiple on the same day

import json
import datetime


def str_to_timedelta(str_of_timedelta): # input the value of the key and get out a timedelta
    converted_str = datetime.datetime.strptime(str_of_timedelta,"%H:%M:%S") # we specify the input and the format...
    converted_str = datetime.timedelta(hours=converted_str.hour, minutes=converted_str.minute, seconds=converted_str.second) # ...and use datetime's hour, min and sec properties to build a timedelta
    return converted_str

def add_to_total(old_time_val): #gets the string from both dictionaries, converts to timedelta, and outputs the total time as timedelta
    new_time = str_to_timedelta(value)
    old_time = str_to_timedelta(old_time_val)
    total_time = new_time + old_time
    return total_time


#retrieves object from data_file.json and converts to python dict
f = open("data_file.json")
json_new_dict = f.read() 
f.close()
new_dict = json.loads(json_new_dict)

#retrieves object big_log.json and converts to python dict
f = open("big_log.json")
json_big_log = f.read() 
f.close()
big_log = json.loads(json_big_log)

# stores current_date as current date and sets up date_is_today bool
current_date = str(datetime.date.today())
date_is_today = False

# if the current date is not in big_log then do this, otherwise do that
for date in big_log: # checks every "date" in the dictionary big_log
    if date == current_date: # if it matches the current date
        date_is_today = True 
        for key, value in new_dict.items(): # idk why items but idc
            if key in big_log[date]: # if the app is already in the log for that day then add to the value
                total_time = add_to_total(big_log[date][key])
                big_log[date].update({key: str(total_time)})
            else: 
                big_log[date][key] = new_dict[key]
if date_is_today != True:
    big_log.update({current_date: new_dict})

print(big_log)

choice = input("do you want to see the total use time of all applications in the big log (y/n)")
if choice == "y":
    total_dict = {}
    for date in big_log:
        for key, value in big_log[date].items():
            if key in total_dict:
                total_time = add_to_total(total_dict[key])
                total_dict.update({key: str(total_time)})
            else:
                total_dict[key] = big_log[date][key]
    print(total_dict)



jsonObject = json.dumps(big_log, indent=4) # converts timers_dict into JSON string
    
with open("big_log.json", "w") as write_file:
    write_file.write(jsonObject) # writes to JSON file
