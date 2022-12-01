import json

file = open('timetables_deltas.txt', 'r')

data = json.loads(file.read())

for row in list(data.keys()):
    print(row)
    line, variant = row.split(':')
    type = variant[0:2]
    print(line, variant) # unikatowy identyfikator
    #get line, variant like this
    for stop in data[row]:
        group_id, stop_id = stop.split(':')
        minute = data[row][stop]
        print(line, group_id, stop_id, minute)



