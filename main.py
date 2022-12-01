import requests, json
APIKEY='389532f9-51d7-45de-82b4-85de4b73f396'

get_stops_url = 'https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'

def get_api(string):
    string += f'&apikey={APIKEY}'
    output = requests.get(string)
    return json.loads(output.text)


# This gets all the stops in Warsaw transport and dumps them to csv file (<NAME OF STOP>, <STOP GROUP ID>, <STOP ID>, <PAIR OF COORDINATES>)
stops = get_api(get_stops_url)
file = open('stops.txt', 'w+')
for s in stops['result']:
    file.write(f"{s['values'][2]['value']},{s['values'][0]['value']},{s['values'][1]['value']},{s['values'][4]['value']},{s['values'][5]['value']},\n")


#helper functions to get line/timetable information

def get_lines(stop_id, stop_nr):
    get_lines_url = f'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId={stop_id}&busstopNr={stop_nr}'
    return get_api(get_lines_url)

def get_timetable(stop_id, stop_nr, line):
    get_timetable_url = f'https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId={stop_id}&busstopNr={stop_nr}&line={line}'
    return get_api(get_timetable_url)

#this asks API about every line, and maps it to stops it uses
file2 = open('lines.txt', 'w')
lines_dict = {}
i = 0
for s in stops['result']:
    stop_id, stop_nr = s['values'][0]['value'], s['values'][1]['value']
    print(stop_id, stop_nr)
    lines = get_lines(stop_id, stop_nr)
    lines_clear_list = []
    for line in lines['result']:
        lines_clear_list.append(line['values'][0]['value'])
    file2.write(f'{stop_id}{stop_nr}:{lines_clear_list}\n')
    lines_dict[f'{stop_id}:{stop_nr}'] = lines_clear_list
out = json.dumps(lines_dict)
file2.write(out)

#This uses our information on lines, and gets the timetables
with open('lines.txt', 'r') as f:
    data = json.loads(f.read())

i = 0
timetables = {}
for k in data: # for every stop
    i+=1
    print(i/len(data.keys()))
    stop_id, stop_nr = k.split(':')
    for line in data[k]: # for every line on that stop
        #6
        #print(f'FOR LINE {line} AT {stop_id} AT {stop_nr}')
        timetable = get_timetable(stop_id, stop_nr, line)

        for row in timetable['result']:
            direction = row['values'][4]['value']
            time = row['values'][5]['value']
            try:
                if k in timetables[f'{line}:{direction}'].keys():

                    continue
            except KeyError:
                timetables[f'{line}:{direction}'] = {k:time}
            timetables[f'{line}:{direction}'][k] = time

    try:
        time_9 = timetables['6:TP-GCW']
        print(time_9) #Some testing experiment to look if out scrapping works properly
    except KeyError:
        pass

file3 = open('timetables.txt', 'w')
out3 = json.dumps(timetables)
file3.write(out3)
file3.close()