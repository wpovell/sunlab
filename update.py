from bs4 import BeautifulSoup

with open('Info.svg') as f:
    svg=BeautifulSoup(f.read(), features="html5lib")

svg.select('[data-name="Head"]')[0].attrs['class'].append('person')
svg.select('[data-name="Body"]')[0].attrs['class'].append('person')
svg.select('#Header > text')[1].attrs['id'] = 'time'

svg.select('#Desk > rect')[0].attrs['class'].append('remote')
for i in svg.select('#Desk > #Left_Monitor > *'):
    i.attrs['class'].append('remote')

for i in svg.select('#Desk > #Right_Monitor > *'):
    i.attrs['class'].append('remote')

for i in svg.select('#Desk > #Mouse > *'):
    i.attrs['class'].append('remote')

svg.select('style')[0].string += '\n.person{\n fill: inherit;\n stroke: inherit\n}\n.remote{\n fill: inherit;\n}'

for i in svg.select('#Rows > g'):
    if 'data-name' in i.attrs:
        i.attrs['id'] = 'Row-' + i.attrs['data-name']
        for e in i.select('use'):
            col = e.attrs['id'].split('-')[0]
            if 'class' not in e.attrs:
                e.attrs['class'] = []
            e.attrs['class'].append(col)
            if 'xlink:href' in e.attrs:
                typ = e.attrs['xlink:href'].replace('#', '')
                e.attrs['class'].append(typ)

with open('index.tmp') as f, open('index.html', 'w') as out:
    out.write(f.read().format(str(svg)))