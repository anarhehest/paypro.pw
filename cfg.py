global cfg
cfg = {'keys':{}}

with open('.env', 'r') as f:
    for l in f.readlines():
        cfg['keys'].update({l.split('=')[0]:l.split('=')[1].strip('\n').strip('\"')})
