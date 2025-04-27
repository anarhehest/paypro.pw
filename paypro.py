import json
from http.client import HTTPConnection, HTTPResponse,  HTTPSConnection

from auth import keygen

URL = "https://api.paypro.pw"

p = lambda v,k=URL: f'{k}{v}' 


def _request(f, **kw) -> HTTPResponse:
    try:
        d = kw.pop('payload')
    except KeyError:
        d = kw
    
    m, _p, kw = f(**d)
    c, P = (HTTPSConnection, 443) if URL.startswith('https') else (HTTPConnection, 80)
    print('>', m, p(_p), P)
    
    conn = c(URL, P)
    conn.request(m, p(_p), json.dumps(d), keygen(d, m=='POST', kw.pop('keys')))
    resp = conn.getresponse()
    conn.close()
    print('<', resp.status, '\n<', resp.read().decode())
    
    return resp


def request(f, **kw):
    m, _p, kw = f(**kw)

    print('>', m, '\n>', m.__name__, p(_p))
    if not 'payload' in kw.keys():
        kw.update({ 'payload': dict() })

    r = m(p(_p), headers=keygen(kw['payload'], m, kw['keys']))
    print('<', r.content.decode())
    return r


