#!/usr/bin/env python3
"""Зводить вивантажені канали в один JSON для подальшої обробки.

Кожне повідомлення отримує посилання на оригінал у Discord — без нього
звинувачення на сайті буде неперевірним.
"""
import json, pathlib, sys, collections

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
GUILD_IDS = {
    'Dream-Market-Place': '948850425141002290',
    'ABYSS-Market': '1309917041234280498',
    'Coolix-Market': '1244667730758598728',
    'Europe-Market': '972502585825173514',
    'Klauzo-Treasury': '1350105552155574292',
    'Loja-do-Bestial': '1162207038647054387',
    'Rucoy-Market': '985707520486150186',
    'Rucoy-Online-Market-Place': '1036340340245934212',
    'Rucoy-World': '1461772543269667014',
}

messages, sources = [], []
for f in sorted(OUT.glob('*/*.json')):
    server, channel_file = f.parent.name, f.stem
    try:
        data = json.loads(f.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'  пропущено {f}: {e}'); continue
    gid = GUILD_IDS.get(server, '')
    cid = data.get('channel', {}).get('id', '')
    msgs = data.get('messages', [])
    sources.append({'server': server, 'channel': channel_file,
                    'channelName': data.get('channel', {}).get('name', ''),
                    'channelId': cid, 'messageCount': len(msgs)})
    for m in msgs:
        a = m.get('author', {})
        messages.append({
            'server': server,
            'channel': channel_file,
            'channelId': cid,
            'messageId': m.get('id'),
            'timestamp': m.get('timestamp'),
            'author': {'name': a.get('name'), 'nickname': a.get('nickname'),
                       'id': a.get('id')},
            'content': m.get('content', ''),
            'attachments': [x.get('url') for x in m.get('attachments', []) if x.get('url')],
            'embeds': [{'title': e.get('title'), 'description': e.get('description'),
                        'url': e.get('url')} for e in m.get('embeds', [])],
            'reactions': [{'emoji': (r.get('emoji') or {}).get('name'),
                           'count': r.get('count')} for r in m.get('reactions', [])],
            'link': f'https://discord.com/channels/{gid}/{cid}/{m.get("id")}' if gid and cid else None,
        })

messages.sort(key=lambda m: (m['timestamp'] or ''))
out = {'sources': sources, 'messageCount': len(messages), 'messages': messages}
dest = OUT / 'scammers-all.json'
dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')

print(f'  зведено: {len(messages)} повідомлень з {len(sources)} каналів')
print(f'  файл: {dest}  ({dest.stat().st_size/1048576:.1f} МБ)')
print()
print('  з вкладеннями (скріни-докази):',
      sum(1 for m in messages if m['attachments']))
by = collections.Counter(m['server'] for m in messages)
for s, c in by.most_common():
    print(f'    {c:>5}  {s}')
