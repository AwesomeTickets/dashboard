#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import sys

OWNERS = ['AwesomeTickets']
REPOS = ['Dashboard', 'Integration', 'ServiceServer', 'StaticPageServer', 'DatabaseServer', 'CacheServer']
URL = 'https://api.github.com/repos/%s/%s/stats/contributors'


def create_req(url):
    return urllib.request.Request(url, data=None, headers={
        'User-Agent': 'AwesomeTickets'
    })


for owner in OWNERS:
    tot = 0
    author_tot = {}
    for repo in REPOS:
        print("%s/%s:" % (owner, repo))
        req = create_req(URL % (owner, repo))
        try:
            with urllib.request.urlopen(req) as res:
                json_str = res.read().decode('utf-8')
                contribs = json.loads(json_str)
                contribs.sort(key=lambda x: x['total'], reverse=True)
                for contrib in contribs:
                    cnt = contrib["total"]
                    tot += cnt
                    author = contrib["author"]["login"]
                    if (author in author_tot):
                        author_tot[author] += cnt
                    else:
                        author_tot[author] = cnt
                    print("%-16s: %4s commits" % (author, cnt))
        except urllib.error.HTTPError as err:
            print(err)
            print(err.read().decode('utf-8'))
            sys.exit(1)
        print("")
    print("%s:" % owner)
    author_tot = [(k, author_tot[k]) for k in sorted(author_tot, key=author_tot.get, reverse=True)]
    for author, cnt in author_tot:
        print("%-16s: %4d commits (%2d%%)"
              % (author, cnt, cnt * 100 // tot))
