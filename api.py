global api

p = lambda v,k='merchant': f'/{k}/{v}'

api = {
    'account': { 'info': lambda **kw: ('GET', p('account-info'), kw) },
    'deposit': {
        'pre': lambda **kw: ('GET', p('pre-deposit'), kw),
        'get-address': lambda **kw: ('POST', p('get-address'), kw),
        'make': lambda **kw: ('POST', p('deposit'), kw),
    },
    'withdraw': {
        'pre': lambda **kw: ('GET', p('pre-withdraw'), kw),
        'make': lambda **kw: ('POST', p('withdraw'), kw),
    }
}


def keys_transfer(**kw):
    if not 'payment_systems' in kw.keys():
        raise ValueError('Key "payment_systems" is required')
    for x in 'code', 'keys':
        if not x in kw['payment_systems']:
            raise ValueError(f'Variable {x} is required')
    return 'POST', p('keys-transfer'), kw


api.update({
    'payment_systems': {
        'keys_transfer': lambda **kw: keys_transfer(**kw),
        'api_info': lambda **kw: ('GET', p('api-info'), kw),
    }
})


def transaction_status(**kw):
    try:
        _p = p(f"/merchant-transaction-status/{kw.pop('id')}")
    except KeyError:
        raise ValueError(f'Transaction ID is required')
    return 'GET', _p, kw


api['payment_systems'].update({
    'transaction_status': lambda **kw: transaction_status(**kw),
    'transactions': lambda **kw: ('GET', p('transactions'), kw),
    'transaction_log': lambda **kw: ('GET', p('transaction-log'), kw),
})


def settings(**kw):
    try:
        _p = p(f"/merchant-transaction-status/{kw.pop('settings')}")
    except KeyError:
        raise ValueError(f'Payment system code is required')
    return 'GET', _p, kw

api['payment_systems'].update({
    'info': lambda **kw: settings(**kw),
    'payment_systems': lambda **kw: ('GET', p('payment-systems'), kw),
})


def check_balance(**kw):
    try:
        _p = p(f"/check-balance/{kw.pop('code')}")
    except KeyError:
        raise ValueError(f'Payment system code is required')
    return 'GET', _p, kw

api['payment_systems'].update({
    'check_balance': lambda **kw: check_balance(**kw),
    'methods': lambda **kw: ('GET', p('payment-methods-list'), kw),
    'method_settings': lambda **kw: ('PATCH', p('payment-methods-settings'), kw)
})

api['ps'] = api['payment_systems']
