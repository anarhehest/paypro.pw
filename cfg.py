global cfg
cfg = { 'keys': dict() }

with open('.env', 'r') as f:
    for l in f.readlines():
        if 'key' in l:
            cfg['keys'].update({
                l.split('=')[0]: l.split('=')[1].strip('\n').strip('\"')
            })
