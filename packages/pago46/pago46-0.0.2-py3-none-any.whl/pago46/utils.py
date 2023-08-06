import hashlib
import hmac
import time
import urllib.parse
from collections import OrderedDict


def get_concatenated_payload(payload):
    """Concatenate payload"""
    concatenated_data = ''
    params = OrderedDict(sorted(payload.items()))

    for key, value in params.items():
        concatenated_data += "&" + urllib.parse.quote(key, safe='') + "=" + urllib.parse.quote(str(value), safe='')

    return concatenated_data


def sign_request(method, path, merchant_key, merchant_secret, payload={}):
    """sign a request to CPP of PAGO46"""
    date = str(time.time()).replace('.', '')
    encrypt_base = merchant_key + '&' + date + '&'+ method + '&' + urllib.parse.quote(str(path), safe='')
    if len(payload) > 0:
        encrypt_base += get_concatenated_payload(payload)

    message_hash = hmac.new(merchant_secret.encode('utf-8'), encrypt_base.encode('utf-8'),
                            hashlib.sha256).hexdigest()
    return message_hash, date
