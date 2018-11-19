import json
import re

with open('out.json') as f:
    data = json.load(f)

out = []
for k in sorted(map(int, data.keys())):
    v = data[str(k)]
    d = []
    for computer, info in v.items():

        row, col =  re.findall(r'cslab(\d+)([a-z])', computer)[0]
        row = int(row)

        local = 0
        remote = 0
        for user in info:
            if user['src'].startswith('(:') and (k-user['time']) < 60*60*4:
                local += 1
            else:
                remote += 1
        d.append([row, col.upper(), local, remote])
    out.append([k, d])
with open('simp.js', 'w') as f:
    f.write('let data='+json.dumps(out))
