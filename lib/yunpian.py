import requests

from LV.common_settings import APIKEY_YUNPIAN


def single_send(mobile, text):
    url = 'https://sms.yunpian.com/v2/sms/batch_send.json'
    payload = dict(mobile=mobile, text=text)
    return _send(url, payload=payload)


def _send(url, method='POST', payload=None):
    headers = {
        'Accept': 'application/json',
        'charset': 'utf-8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload['apikey'] = APIKEY_YUNPIAN
    if method == 'POST':
        return requests.post(url, data=payload, headers=headers)
    elif method == 'GET':
        return requests.get(url, params=payload, headers=headers)
