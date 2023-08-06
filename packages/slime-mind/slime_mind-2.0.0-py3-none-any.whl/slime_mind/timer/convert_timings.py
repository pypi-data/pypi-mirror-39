import csv
# timer,{turn},{function.__name__},{elapsed}
turns = []
with open('timer/timings.txt', 'r') as f:
    for line in f:
        if "timer," in line:
            parts = line.split(",")
            turn = int(parts[1])
            method = parts[2]
            elapsed = float(parts[3])

            if turn == len(turns):
                turns.append({})

            row = turns[turn]

            if method in row:
                row[method] += elapsed
            else:
                row[method] = elapsed
fieldnames = []
for turn in turns:
    for key in turn:
        if key not in fieldnames:
            fieldnames.append(key)

with open('timer/timings.csv', 'w', newline = '') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, restval = 0)
    writer.writeheader()
    writer.writerows(turns)