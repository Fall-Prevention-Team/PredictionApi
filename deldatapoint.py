"""
Tool to "browse" and delete specific 
datapoint from a csv/tsv. 
"""
import sys, os, csv, time
args = sys.argv[1:]
def display():
    with open(args[0]) as csvin:
        csv_reader = csv.reader(csvin, delimiter='\t')
        for i, row in enumerate(csv_reader):
            print(f'{i:<3}', 'TIME:', time.ctime(float(row[0])), 'CLS:', row[1])

def del_ids():
    with open(args[0], 'r') as csvin:
        csv_reader = csv.reader(csvin, delimiter='\t')
        csvcontent = []
        for row in csv_reader:
            csvcontent.append(row)
    with open(args[0], 'w') as csvout:
        csv_writer = csv.writer(csvout, delimiter='\t')
        numargs = [int(y) for y in args[1:]]
        for i, row in enumerate(csvcontent):
            if i in numargs:
                continue
            rowstr = [str(x) for x in row]
            csv_writer.writerow(row)


if not args:
    print('=> no args')
    exit()
elif os.path.exists(args[0]):
    if len(args) > 1:
        del_ids()
        print('=> ids deleted:', args[1:])
    else:
        display()
        print('=> use -d [id] ... to delete id(s)')
else:
    print('=> no effect')
exit()
    