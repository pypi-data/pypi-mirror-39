# py_slack
basic webhook messages, want interactivity next

### CLI

    python3 send_hook.py https://hook_url/xxxxx/xxxx string_of_txt
  
  
### In Code
  
In practice, I use this to send JSONs of Python objects. Here's how to use it in code:
  
    from send_hook import send_msg_hook
  
    send_hook_msg(hook_url, msg, format_type)
    #hook_url expects a string url with the appropriate protocol at the beginning, for example http:// or https://
    #msg expects either a dictionary or a string
    #format_type defaults to 'snippet', but can be set to 'plain'
