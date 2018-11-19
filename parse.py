#!/usr/bin/env python3
import json
import pathlib
from dateutil.parser import parse as parseTime
import re
from matplotlib import pyplot as plt
import os.path
from datetime import datetime

RAW = 'data1'
OUT = 'out.json'

def parse(text):
    t = 0

    ret = {}
    cTime = None
    cData = None
    for line in text.strip().split('\n'):
        if 'Nov' in line:
            if cTime is not None:
                ret[cTime] = cData
                t=0

            cTime = int(parseTime(line).timestamp())
            cData = {}
            cHost = None
            cUsers = None
            continue

        if line.startswith('cslab'):
            if cHost is not None:
                cData[cHost] = cUsers
                t += len(cUsers)
            cHost = line
            cUsers = []
            continue

        l = re.findall(r'([a-z0-9]+)\s+(pts/\d+|tty\d+)\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) ?(.+)?', line)
        if len(l) != 1:
            continue

        user, term, time, src = l[0]
        time = int(parseTime(time).timestamp())

        cUsers.append({
            'user': user,
            'term': term,
            'time': time,
            'src' : src,
        })
    return ret

SIMP = 'simp.json'
def simp(data):
    l = []
    for k in sorted(data.keys()):
        v = data[k]
        l.append({
            tk.replace('cslab', ''): len(tv)
            for tk,tv in v.items()
        })
    with open(SIMP, 'w') as f:
        json.dump(l, f)


if __name__ == '__main__':
    if not os.path.isfile(OUT):
        with open(RAW) as f:
                data = parse(f.read())

        with open(OUT, 'w') as f:
            json.dump(data, f)
    else:
        with open(OUT) as f:
            data = json.load(f)

    simp(data)