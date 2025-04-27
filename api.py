from requests import get, patch, post

global api

p = lambda v,k='merchant': f'/{k}/{v}'
r = lambda m,v,kw: (m, p(v), kw)

api = {
    'account': { 'info': lambda **kw: r(get, 'account-info', kw) },
    'deposit': {
        'pre': lambda **kw: r(get, 'pre-deposit', kw),
        'get-address': lambda **kw: r(post, 'get-address', kw),
        'make': lambda **kw: r(post, 'deposit', kw),
    },
    'withdraw': {
        'pre': lambda **kw: r(get, 'pre-withdraw', kw),
        'make': lambda **kw: r(post, 'withdraw', kw),
    }
}


def keys_transfer(**kw):
    if not 'payment_systems' in kw.keys():
        raise ValueError('Key "payment_systems" is required')
    for x in 'code', 'keys':
        if not x in kw['payment_systems']:
            raise ValueError(f'Variable {x} is required')
    return r(post, 'keys-transfer', kw)


api.update({
    'payment_systems': {
        'keys_transfer': lambda **kw: keys_transfer(**kw),
        'api_info': lambda **kw: r(get, 'api-info', kw),
    }
})


def transaction_status(**kw):
    try:
        _p = p(f"/merchant-transaction-status/{kw.pop('id')}")
    except KeyError:
        raise ValueError(f'Transaction ID is required')
    return get, _p, kw


api['payment_systems'].update({
    'transaction_status': lambda **kw: transaction_status(**kw),
    'transactions': lambda **kw: r(get, 'transactions', kw),
    'transaction_log': lambda **kw: r(get, 'transaction-log', kw),
})


def settings(**kw):
    try:
        _p = p(f"/merchant-transaction-status/{kw.pop('settings')}")
    except KeyError:
        raise ValueError(f'Payment system code is required')
    return get, _p, kw


api['payment_systems'].update({
    'info': lambda **kw: settings(**kw),
    'payment_systems': lambda **kw: r(get, 'payment-systems', kw),
})


def check_balance(**kw):
    try:
        _p = p(f"/check-balance/{kw.pop('code')}")
    except KeyError:
        raise ValueError(f'Payment system code is required')
    return get, _p, kw


api['payment_systems'].update({
    'check_balance': lambda **kw: check_balance(**kw),
    'methods': lambda **kw: r(get, 'payment-methods-list', kw),
    'method_settings': lambda **kw: r(patch, 'payment-methods-settings', kw)
})

api = {
    'a': api['account'],
    'd': api['deposit'],
    'p': api['payment_systems'],
    'w': api['withdraw'],
}
