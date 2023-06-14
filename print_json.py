import json

f = open("big_log.json")
json_big_log = f.read() 
f.close()
big_log = json.loads(json_big_log)

big_log_list = list(map(list, big_log.items()))

for count in range(len(big_log_list)):
    print("\n"+big_log_list[count][0]+ ":")
    for y, z in big_log_list[count][1].items():
        print(y,":",z)