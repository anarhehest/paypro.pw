import time
from typing import Dict, Tuple, List, Union

from l import l

""" implemented with an example from API docs 
def generate_key(query:dict, date:str, post:bool) -> str:
    '''
    This function JSONifies and signs a body of API-request to create an auth key.
    Should be sent within headers under key Auth

    Input:
    * query: dict - request body
    * date:  str  - current unix timestamp as a string
    * post:  bool - whether request is POST (True) or not (False)
    
    Output:
    * Auth key formatted as 'PPS {public_key}:{signature}'
    '''
    public_key = ""
    private_key = ""

    method = 'post' if post else 'get'
    content_type = 'application/json' if post else ''

    hashs = hashlib.md5(json.dumps(sorted(query)))
    message = method + '\n' + hashs + '\n' + content_type + '\n' + date
    signature = base64.b64encode(hmac.new(private_key, message, hashlib.sha256).hexdigest())

    return 'PPS ' + public_key + ':' + signature
"""

def keygen(query:dict, post:bool, keys:Union[Tuple[str], List[str], Dict[str, str]]) -> str:
    
    if isinstance(keys, tuple):
        key, _key = keys[0], keys[1]
    elif isinstance(keys, list):
        _key = keys.pop()
        key = keys.pop()
    elif isinstance(keys, dict):
        key, _key = keys.pop('PUBLIC_KEY'), keys.pop('PRIVATE_KEY')

    t = str(int(time.time()))
    if post:
        m, ct = 'post', 'application/json'
    else:
        m, ct = 'get', str()
    return { 'Auth': f"PPS {key}:{l['auth']['key'](m,query,ct,t,_key)}", 'X-PPS-Time': t}
