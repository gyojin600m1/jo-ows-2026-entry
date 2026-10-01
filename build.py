import json, html
EVENTS = {
 '1': dict(no=1, gender='男子', dist='10km', day='10月3日(土)', date='2026-10-03', time='10:00'),
 '3': dict(no=3, gender='女子', dist='10km', day='10月3日(土)', date='2026-10-03', time='10:02'),
 '2': dict(no=2, gender='男子', dist='7.5km', day='10月3日(土)', date='2026-10-03', time='10:00'),
 '4': dict(no=4, gender='女子', dist='7.5km', day='10月3日(土)', date='2026-10-03', time='10:02'),
 '5': dict(no=5, gender='男子', dist='5km', day='10月4日(日)', date='2026-10-04', time='09:04'),
 '6': dict(no=6, gender='女子', dist='5km', day='10月4日(日)', date='2026-10-04', time='09:06'),
}
KAGOSHIMA = ['姶良', '加治木', '鹿児島', '原田学園']
people = {}
order = []
for line in open('data.tsv', encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    ev, bib, name, kana, team, birth, grade = f[:7]
    noc = f[7] if len(f) > 7 else 'JPN'
    key = (name, birth)
    if key not in people:
        people[key] = dict(name=name, kana=kana, team=team, birth=birth, grade=grade, noc=noc,
                           gender=EVENTS[ev]['gender'], entries=[], kagoshima=any(k in team for k in KAGOSHIMA))
        order.append(key)
    p = people[key]
    assert p['team'] == team and p['grade'] == grade, (key, team, p['team'])
    p['entries'].append(dict(ev=int(ev), bib=int(bib)))
rows = [people[k] for k in order]
evorder = [1, 3, 2, 4, 5, 6]
for r in rows:
    r['entries'].sort(key=lambda e: evorder.index(e['ev']))
rows.sort(key=lambda r: (evorder.index(r['entries'][0]['ev']), r['entries'][0]['bib']))
counts = {str(k): sum(1 for r in rows for e in r['entries'] if e['ev'] == k) for k in evorder}
data = dict(events={str(v['no']): v for v in EVENTS.values()}, eventOrder=evorder, rows=rows,
            stats=dict(people=len(rows), entries=sum(len(r['entries']) for r in rows),
                       male=sum(r['gender'] == '男子' for r in rows), female=sum(r['gender'] == '女子' for r in rows),
                       byEvent=counts))
tpl = open('template.html', encoding='utf-8').read()
out = tpl.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
open('index.html', 'w', encoding='utf-8').write(out)
print(data['stats'])
print([r['name'] + ' ' + r['team'] for r in rows if r['kagoshima']])
print('multi-event:', sum(len(r['entries']) > 1 for r in rows))
