#!/usr/bin/env python3
"""Будує покажчик обвинувачених із НАДІЙНИМ ідентифікатором.

Надійний тут = Discord ID (snowflake): він видається раз і назавжди, на
відміну від ніка. Discord вкладає профіль згаданого користувача в саме
повідомлення, тож разом з ID ми отримуємо його нік СТАНОМ НА ДЕНЬ ЕКСПОРТУ,
а не той, що був у 2022.
"""
import json, pathlib, re, sys, collections

W = pathlib.Path(sys.argv[1])
GUILD_IDS = {
    'Dream-Market-Place': '948850425141002290', 'ABYSS-Market': '1309917041234280498',
    'Coolix-Market': '1244667730758598728', 'Europe-Market': '972502585825173514',
    'Klauzo-Treasury': '1350105552155574292', 'Loja-do-Bestial': '1162207038647054387',
    'Rucoy-Market': '985707520486150186',
    'Rucoy-Online-Market-Place': '1036340340245934212',
    'Rucoy-World': '1461772543269667014',
}
AVATAR = re.compile(r'cdn\.discordapp\.com/avatars/(\d{15,22})/')
BOLD = re.compile(r'\*\*(.+?)\*\*')
BOTS = {'Carl-bot', 'Dyno', 'MEE6', 'Wick', 'ProBot'}
# ігровий нік персонажа: згадка поруч зі словами про гру
INGAME = re.compile(r'(?:ign|in[- ]?game|nick(?:name)?|char(?:acter)?|acc(?:ount)?)\s*[:\-=]?\s*([A-Za-z][\w \'\-]{2,20})', re.I)

people = {}      # discordId -> запис
by_name = {}     # нік без ID -> запис

def person(uid):
    return people.setdefault(uid, {
        'discordId': uid, 'currentUsername': None, 'displayNames': set(),
        'avatarUrl': None, 'reports': []})

def named(nick):
    return by_name.setdefault(nick, {'handle': nick, 'hasDiscriminator': '#' in nick,
                                     'reports': []})

for f in sorted(W.glob('*/*.json')):
    server = f.parent.name
    gid = GUILD_IDS.get(server, '')
    d = json.loads(f.read_text(encoding='utf-8'))
    channel = f.stem
    cid = d.get('channel', {}).get('id', '')
    for m in d.get('messages', []):
        author = m.get('author', {}) or {}
        content = m.get('content', '') or ''
        link = f'https://discord.com/channels/{gid}/{cid}/{m.get("id")}' if gid and cid else None
        ev = {'server': server, 'channel': channel, 'timestamp': m.get('timestamp'),
              'reportedBy': author.get('name'), 'text': content, 'link': link,
              'attachments': [a.get('url') for a in m.get('attachments', []) if a.get('url')]}
        ig = INGAME.search(content)
        if ig:
            ev['inGameNickGuess'] = ig.group(1).strip()

        hit = False
        for mm in m.get('mentions', []):
            if mm.get('isBot'):
                continue
            p = person(mm['id'])
            if mm.get('name') and mm['name'] != 'Deleted User':
                p['currentUsername'] = mm['name']
            if mm.get('nickname'):
                p['displayNames'].add(mm['nickname'])
            p['avatarUrl'] = p['avatarUrl'] or mm.get('avatarUrl')
            p['reports'].append(ev)
            hit = True

        for e in m.get('embeds', []):
            blob = json.dumps(e)
            for uid in AVATAR.findall(blob):
                person(uid)['reports'].append(ev); hit = True
            a = (e.get('author') or {}).get('name') or ''
            if 'banned' in a.lower():
                named(a.split(' has been')[0].strip())['reports'].append(ev); hit = True

        if not hit and author.get('name') in BOTS and 'anned' in content:
            for g in BOLD.findall(content):
                named(g.strip())['reports'].append(ev)

for p in people.values():
    p['displayNames'] = sorted(p['displayNames'])
    p['reportCount'] = len(p['reports'])
    p['servers'] = sorted({r['server'] for r in p['reports']})
for p in by_name.values():
    p['reportCount'] = len(p['reports'])
    p['servers'] = sorted({r['server'] for r in p['reports']})

ident = sorted(people.values(), key=lambda p: -p['reportCount'])
names = sorted(by_name.values(), key=lambda p: -p['reportCount'])
(W / 'identified.json').write_text(json.dumps(
    {'note': 'discordId is permanent; currentUsername is as of the export date',
     'count': len(ident), 'people': ident}, ensure_ascii=False, indent=1), encoding='utf-8')
(W / 'by-name-only.json').write_text(json.dumps(
    {'note': 'no permanent id available - handle only, may be stale',
     'count': len(names), 'people': names}, ensure_ascii=False, indent=1), encoding='utf-8')

print(f"  з постійним Discord ID: {len(ident)}")
print(f"    з них із поточним ніком: {sum(1 for p in ident if p['currentUsername'])}")
print(f"    згадані більш ніж на одному сервері: {sum(1 for p in ident if len(p['servers'])>1)}")
print(f"  лише нік, без ID: {len(names)}")
print(f"    з них уже в новому форматі (нік живий): {sum(1 for p in names if not p['hasDiscriminator'])}")
print(f"    зі старим Name#1234 (нік мертвий): {sum(1 for p in names if p['hasDiscriminator'])}")
ig = sum(1 for p in ident for r in p['reports'] if 'inGameNickGuess' in r)
print(f"  повідомлень, де згадано ігровий нік: {ig}")
print()
print("  найчастіше згадувані (з ID):")
for p in ident[:8]:
    print(f"    {p['discordId']}  {p['currentUsername'] or '—':<22} згадок={p['reportCount']:<3} серверів={len(p['servers'])}")
