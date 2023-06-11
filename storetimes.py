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
    dict(big_log).update({current_date: new_dict})

for i in dict(big_log).items():
    print(i)

# adds times from all dates if wanted by the user
choice = input("do you want to see the total use time of all applications in the big log (y/n)")
if choice == "y":
    total_dict = {} # initialises the dict for this task
    for date in big_log: # iterates through all the dates
        for key, value in big_log[date].items(): # gets all the keys and values from a date
            
            if key in total_dict: # if a key from this date is already in the total dict
                total_time = add_to_total(total_dict[key]) # add the time from the value of this key to the total time for that app in the total dict
                total_dict.update({key: str(total_time)}) # write this new value to the total dict
            
            else:
                total_dict[key] = big_log[date][key] # makes a new element for the total dict if the app is not in the total dict
    
    # turns the dictionary into an array
    total_list = list(map(list, total_dict.items()))
    print(total_list)

    for i in range(len(total_list)):
        total_list[i][1] = str_to_timedelta(total_list[i][1])
        print(total_list)
    
    # sort the list
    total_list.sort(key=lambda total_list:total_list[1], reverse=True)
    print(total_list)

    # prints the total dict out
    for rows, columns in total_list:
        print(rows, ":", str(columns))
else:
    print("no")


jsonObject = json.dumps(big_log, indent=4) # converts timers_dict into JSON string
    
with open("big_log.json", "w") as write_file:
    write_file.write(jsonObject) # writes to JSON file


new_log = {}
jsonObject = json.dumps(new_log, indent=4)
with open("data_file.json", "w") as clear_file:
    clear_file.write(jsonObject)


# make it so the output is in descending order from longest to shortest times