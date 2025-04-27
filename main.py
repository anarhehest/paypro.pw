import paypro
from api import api
from cfg import cfg

r = paypro.request(api['p']['api_info'], keys=cfg['keys'])
print(r)
