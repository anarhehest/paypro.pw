import json
from http.client import HTTPConnection, HTTPResponse,  HTTPSConnection

from auth import keygen

URL = "https://api.paypro.pw"

p = lambda v,k=URL: f'{k}{v}' 

def request(f, **kw) -> HTTPResponse:
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
