#stores all times into a log, adding the times if there are multiple on the same day

import json
import datetime
import math 

def str_to_timedelta(str_of_timedelta): # input the value of the key and get out a timedelta
    converted_str = datetime.datetime.strptime(str_of_timedelta,"%H:%M:%S") # we specify the input and the format...
    converted_str = datetime.timedelta(hours=converted_str.hour, minutes=converted_str.minute, seconds=converted_str.second) # ...and use datetime's hour, min and sec properties to build a timedelta
    return converted_str

def special_str_to_timedelta(str_of_timedelta): # input the value of the key and get out a timedelta
    converted_str = datetime.datetime.strptime(str_of_timedelta,"%H:%M:%S.%f") # we specify the input and the format...
    converted_str = datetime.timedelta(hours=converted_str.hour, minutes=converted_str.minute, seconds=converted_str.second) # ...and use datetime's hour, min and sec properties to build a timedelta
    return converted_str

def add_to_total(old_time_val): #gets the string from both dictionaries, converts to timedelta, and outputs the total time as timedelta
    new_time = str_to_timedelta(value)
    old_time = str_to_timedelta(old_time_val)
    total_time = new_time + old_time
    return total_time

# rounds times to nearest second
def round_seconds(obj: datetime.datetime) -> datetime.datetime:
    if obj.microsecond >= 500_000:
        obj += datetime.timedelta(seconds=1)
    return obj.replace(microsecond=0)

def special_round_seconds(timedelta):
    timedelta_seconds = datetime.timedelta.total_seconds(timedelta)
    timedelta_full = datetime.timedelta(seconds=int(timedelta_seconds))
    return timedelta_full

if __name__ == '__main__':

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
            print("date is in database already") 
            for key, value in new_dict.items(): 
                if key in big_log[date]: # if the app is already in the log for that day then add to the value
                    total_time = add_to_total(big_log[date][key])
                    big_log[date].update({key: str(total_time)})
                    print("program already in database, added to database")
                else: 
                    big_log[date][key] = new_dict[key]
                    print("program not in database, making new dictionary for it")
    if date_is_today != True:
        dict(big_log).update({current_date: new_dict})
        print("date is not in database")
    print(big_log)
    # adds times from all dates if wanted by the user

    total_dict = {} # initialises the dict for this task
    print("initailised total_dict")
    for date in big_log: # iterates through all the dates
        
        print("going through dates")
        
        for key, value in big_log[date].items(): # gets all the keys and values from a date
            
            if key in total_dict: # if a key from this date is already in the total dict
                total_time = add_to_total(total_dict[key]) # add the time from the value of this key to the total time for that app in the total dict
                total_dict.update({key: str(total_time)}) # write this new value to the total dict
            
            else:
                total_dict[key] = big_log[date][key] # makes a new element for the total dict if the app is not in the total dict
    
    # turns the dictionary into an array
    total_list = list(map(list, total_dict.items()))

    no_of_dates = len(big_log)

    for i in range(len(total_list)): # converts the array into timedelta and at the same time divides it by the number of dates in big log
        total_list[i][1] = str_to_timedelta(total_list[i][1]) / no_of_dates
        
    # sort the list
    total_list.sort(key=lambda total_list:total_list[1], reverse=True)
    
    deletion_complete = False
    if len(total_list) > 5: # so it doesnt crash when theres only a few values    
        for i in range(len(total_list)):
            while deletion_complete == False:
                if total_list[-i - 1][1] > datetime.timedelta(minutes=2):
                    deletion_complete = True
                elif total_list[-i - 1][1] < datetime.timedelta(minutes=2):
                    del total_list[-i - 1]

    # round the numbers before printing out
        for i in range(len(total_list)):
            total_list[i][1] = special_round_seconds(total_list[i][1])


    # prints the total dict out
    for rows, columns in total_list:
        print(rows, ":", str(columns))
        
    # writing the time for today to big log
    json_object = json.dumps(big_log, indent=4) # converts timers_dict into JSON string
        
    with open("big_log.json", "w") as write_file:
        write_file.write(json_object) # writes to JSON file

    # restarting the new log and writing the empty new log to data_file.json
    new_log = {}
    json_object = json.dumps(new_log, indent=4)
    with open("data_file.json", "w") as clear_file:
        clear_file.write(json_object)

    for i in range(len(total_list)):
        total_list[i][1] = str(total_list[i][1])

    list_of_dates = [] # for later when calculating the date range of the data
    for date in big_log:      
        list_of_dates.append(datetime.date.fromisoformat(date)) # creating a list with all the dates 

    sorted_list_of_dates = sorted(list_of_dates) # sorts the list of dates in ascending order 
    date_range = sorted_list_of_dates[-1] - sorted_list_of_dates[1] # takes away the earliest date in the list from the latest date to get a length of time
    string_range_of_days = str(date_range.days) + " days"

    range_dict = {"RANGE OF DAYS TO CALCULATE AVERAGE" : string_range_of_days}
    average_times = dict(total_list)
    average_times.update(range_dict)
    json_object = json.dumps(average_times, indent=4)
    json_range_of_days_dict = json.dumps(range_dict, indent=4)
    with open("average_times.json", "w") as f:
        f.write(json_object)

    print("RANGE OF DAYS TO CALUCLATE AVERAGE : " + string_range_of_days)
    # make it so the output is in descending order from longest to shortest times
    