import json
from datetime import timedelta


#This gets the timetables and calculate time deltas between stops on one line in minutes

file = open('timetables.txt', 'r')

data = json.loads(file.read())

for k in data.keys():
    print(f"LINIA {k}")
    temp_time_dict = {}
    for l in data[k].keys():
        time_array = data[k][l].split(':')
        delta = timedelta(hours=int(time_array[0]), minutes=int(time_array[1]))
        temp_time_dict[l] =delta.total_seconds()/60
    dic2 = dict(sorted(temp_time_dict.items(), key=lambda x: x[1]))
    first = list(dic2.values())[0]
    dic3 = {x:int(dic2[x]-first) for x in dic2}
    data[k] = dic3

file3 = open('timetables_deltas.txt', 'w')
out3 = json.dumps(data)
file3.write(out3)
file3.close()
