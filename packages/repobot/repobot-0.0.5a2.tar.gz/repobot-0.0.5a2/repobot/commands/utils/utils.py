# repobot/commands/utils.py
'''utility functions and wrappers'''

import sys
from functools import wraps
from requests.auth import HTTPBasicAuth
import keyring
import requests
import os

def set_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = keyring.get_password('repobot', 'username')
        password = keyring.get_password('repobot', 'password')

        if password is None:
            print('Set credentials first with `repobot login`')
            sys.exit(0)

        r = requests.get('https://api.github.com/user', auth=HTTPBasicAuth(username, password))
        if r.status_code == 401:
            print('Invalid Auth credentials. Please log in again')
            sys.exit(0)

        func(*args, basicauth=HTTPBasicAuth(username, password), **kwargs)


    return wrapper


import re

def cinput(*args, expression='', error_message='Invalid'):
    while True:
        i = input(*args)
        if re.search(expression, i):
            return i
        else:
            print(error_message)

def yn_input(prompt='', default=None):
    '''wraps input command to get a yes or no response'''
    while True:
        if default is True:
            res = input(prompt + '[Y/n] : ')
            if re.search('no?', res, flags=2):
                return False
            return True
        else:
            res = input(prompt + '[y/N] : ')
            if re.search('ye?s?', res, flags=2):
                return True
            return False

def allowescape(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('\nBye')
            sys.exit()
    return wrapper

def checkshellcommand(command, quiet=True):
    """
    Only runs the decorated function if the given shell commands is installed
    quiet - Silently omits running the command if true, otherwise informs user to install the required command
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.popen('which %s' % command).read():
                return func(*args, **kwargs)            
            if not quiet:
                print('WARN: Shell command %s was needed but not found. Some things may not work' %s)
        return wrapper
    return decorator
