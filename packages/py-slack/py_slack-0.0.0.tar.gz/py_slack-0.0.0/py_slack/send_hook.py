from requests import post
from json import dumps
from sys import argv

def send_hook_msg(hook_url, msg, format_type = 'snippet'):

    headers = {'Content-type':'application/json'}

    if format_type == 'snippet': formatted = '` ' + str(msg) + ' `'
    else: formatted = str(msg)

    data = dumps({'text':formatted})
    response = post(hook_url, headers=headers, data=data)

    if response.status_code != 200: print(response.status_code, response.text)

if __name__ == '__main__':
    hook_url = argv[1]
    msg = argv[2]
    
    send_hook_msg(hook_url, msg, format_type = 'plain')
