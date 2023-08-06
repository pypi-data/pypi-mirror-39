# repobot/commands/hello.py
'''
rbot ls - LIST REPOS

Usage:
    rbot ls [--params <str>] [--limit <number>] [--all]

Description:
    List all repos user has explicit push, pull, or admin access to (via /user/repos)
    Rbot prints list of repos on owner/name format (eg. nodejs/node), seperated on each line.
    Only prints the first 30 repos found by default, unless --all or --limit is specified.

Options:
    --params <str>      space-seperated string of key=value params, as specified in the github API
                        see https://developer.github.com/v3/repos/#list-your-repositories for details

    --limit <number>    limits the amount of entries to <number>. If a number is given thats larger
                        than the number of entries, rbot simply returs all entries. Overrules --all

    --all               List all entries. If --limit is set, this option is ignored.
                        WARNING: Will likely initiate multiple requests, depending on number of repos
                        the user has access to.
'''
import sys
from .base import Base
from json import dumps
from .utils import set_token
import json
import re
from colorama import init, Fore, Style
import requests

class Ls(Base):
    '''say hello world'''

    @set_token
    def run(self, basicauth):

        limit = int(self.options['--limit']) or -1
        print(limit)
        page = 1        
        last_page = self.getlastpage(basicauth=basicauth) if self.options['--limit'] or self.options['--all'] else 1 # only one page by default
        for p in range(1, last_page+1):
            repo_res = self.getreposatpage(p, basicauth=basicauth)
            for name in repo_res['repos']:
                print(name)
                limit -= 1
                # check if limit is -1 to make limit inclusive
                # don't check with less than as -1 starting is limitless (becomes -2 on first check and never breaks)
                if limit == -1:
                    return

    def getlastpage(self, *, basicauth):
        headers = requests.head('https://api.github.com/user/repos', auth=basicauth).headers
        last_page = re.compile(r'page=(\d+)>;\srel="last"').findall(headers['Link'])[0]
        return int(last_page)

    #TODO: @set_token doesnt work here. Figure out why   
    def getreposatpage(self, page, *, basicauth):
        """ """
        params = addpageparam(parseparams(self.options['--params']), page)
        res = requests.get('https://api.github.com/user/repos' + params, auth=basicauth)
        checkforerrors(res)
        rel = re.compile(r'rel="(\w+)"').findall(res.headers['Link'])[0]
        return {'repos': self.extractreponames(res.json()), 'rel': rel,}
        
        
    def extractreponames(self, data: list):
        def mapreposforprettyprint(obj):
            permissions = obj['permissions']
            if permissions['admin'] is False and permissions['push'] is False and permissions['pull'] is True:
                readonly = read = Fore.YELLOW + 'readonly' + Style.RESET_ALL
            else:
                readonly = ''
            
            priv = Fore.RED + 'private ' + Style.RESET_ALL if obj['private'] else ' '
        
            LENGTH = 24
            return obj['full_name'] + (' ' * (24-len(obj['full_name']))) + ' ' + priv + readonly 
        return map(mapreposforprettyprint, data)


def checkforerrors(res:'Response'):
    
    if res.status_code > 399:
        print(Fore.RED + 'Couldn\'t process request' + Style.RESET_ALL)
        print(json.dumps(res.json(), indent=2))
        sys.exit(1)


def parseparams(params):
    """Parses space seperated params for query string (including the starting `?`)
    Returns empty string if no params are given"""
    
    if params is None:
        return ''
    
    return '?' + re.sub(r'\s+', '&', params)

def addpageparam(params, page):
    if page == 1:
        return params
    if len(params):
        return params + '&page=' + str(page)
    return '?page=' + str(page)
