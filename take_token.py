from urllib.parse import urlencode


OUTH_URL = 'https://oauth.vk.com/authorize'
params = {
    'client_id': 7149833,
    'display': 'page',
    'scope': ['friends', 'groups'],
    'response_type': "token",
    'v': 5.101
}

print('?'.join((OUTH_URL, urlencode(params))))