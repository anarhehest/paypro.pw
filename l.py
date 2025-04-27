import base64
import json
import hashlib
import hmac

l = {
    'hash': {
        'query': lambda x: hashlib.md5(json.dumps(sorted(x)).encode()).hexdigest(),
        'message': lambda x, k: base64.b64encode(hmac.new(str.encode(k), str.encode(x), hashlib.sha256).digest()),
    },
}

l.update({
    'auth': {
        'key': lambda m,q,c,t,k: l['hash']['message']('\n'.join([m, l['hash']['query'](q),c,t]),k).decode()
    }
})
