import time

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

def keygen(query:dict, method:callable, keys:dict[str,str]) -> str:

    match method.__name__:
        case 'get':
            m, ct = 'get', str()
        case 'post', _:
            m, ct = 'post', 'application/json'
            
    t = str(int(time.time()))    
    return {
        'Auth': f"PPS {keys['PUBLIC_KEY']}:{l['auth']['key'](m,query,ct,t,keys['PRIVATE_KEY'])}",
        'X-PPS-Time': t
    }
