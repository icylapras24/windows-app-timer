# get the name of the filename of the application in use currently
# record the time spent on an application by subtracting previous time from current time
# 
# convert it into a format suitable for json
# write this time to a json file
from os import getpid
from time import sleep
import datetime
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
import psutil
import json 


print("---Timer for apps in Windows---")

# gets the name of the process ... (https://stackoverflow.com/questions/70574208/get-the-name-of-the-current-opened-application-in-python)
def get_process_name():
    hwnd = GetForegroundWindow()
    _,pid = GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    process_name = process.name()
    return process_name

# rounds times to nearest second
def round_seconds(obj: datetime.datetime) -> datetime.datetime:
    if obj.microsecond >= 500_000:
        obj += datetime.timedelta(seconds=1)
    return obj.replace(microsecond=0)



#gets the data for python to read from the JSON
f = open("data_file.json")
string = f.read() 

# resets the dictionary if wanted
yes_or_no = input("Do you want to reset the timers (y/n): ")
if yes_or_no == "y":
    timers_dict = {}
    print("yes"+"\n"+str(timers_dict))
elif yes_or_no == "n":
    timers_dict = json.loads(string) # turns the json object format thing into a python dictionary
    print("no")
    print(timers_dict)
else:
    timers_dict = json.loads(string)
    print("did not enter y/n, timers have not been reset")
f.close()

# setting up/initialising variables (after the input from the user so the time does not count the time spent answering the input question

old_time = round_seconds(datetime.datetime.now())
active_window = get_process_name()
new_window = ""
count = 0
statement_executed = False

while True:
    new_window = get_process_name()
    if (new_window != active_window) or (count>=30):
        current_time = round_seconds(datetime.datetime.now()) #current datetime = the datetime now and rounds to nearest second
        
        if active_window not in timers_dict:
            timers_dict.update({active_window: "0:00:00"})
        
        # getting the time from the dictionary and converting to timedelta
        total_time = timers_dict[active_window]
        total_time = datetime.datetime.strptime(total_time,"%H:%M:%S") # we specify the input and the format...
        total_time = datetime.timedelta(hours=total_time.hour, minutes=total_time.minute, seconds=total_time.second) # ...and use datetime's hour, min and sec properties to build a timedelta
        
        total_time += current_time - old_time # total time for the thing
        old_time = current_time
       
        str_total_time = str(total_time)
        timers_dict.update({active_window: str_total_time}) # updates the dictionary with the current time if the dictionary does not have that window stored
        jsonObject = json.dumps(timers_dict, indent=4) # converts timers_dict into JSON string
        
        with open("data_file.json", "w") as write_file:
                    write_file.write(jsonObject) # writes to JSON file
        
        active_window = new_window
        statement_executed = True

    if (statement_executed == True): #if the if statement before was executed or it has been 300 seconds (5 minutes) then prints the times along with the curren time
        print("Time :", datetime.datetime.now().strftime("%H:%M:%S")) #current time in hrs mins and secs
        #prints the dictionary line by line
        for apps,times in timers_dict.items():
            print(apps, ":", times) 
        print("\n" + str(psutil.Process(getpid()).memory_info().rss / 1024 ** 2), "MB of RAM", "\n") 
        statement_executed = False
        count = 0
    count +=1
    sleep(10)

print(psutil.Process(getpid()).memory_info().rss / 1024 ** 2, "MB of RAM") 
