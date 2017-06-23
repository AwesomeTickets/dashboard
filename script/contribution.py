#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import sys

OWNERS = ['AwesomeTickets']
REPOS = ['Dashboard', 'Integration', 'ServiceServer',
         'StaticPageServer', 'DatabaseServer', 'CacheServer']
URL = 'https://api.github.com/repos/%s/%s/stats/contributors'


def create_req(url):
    return urllib.request.Request(url, data=None, headers={
        'User-Agent': 'AwesomeTickets'
    })


for owner in OWNERS:
    tot_cmt_cnt, tot_line_cnt = 0, 0
    author_cmt_cnt, author_line_cnt = {}, {}
    for repo in REPOS:
        print("%s/%s:" % (owner, repo))
        req = create_req(URL % (owner, repo))
        try:
            with urllib.request.urlopen(req) as res:
                json_str = res.read().decode('utf-8')
                contribs = json.loads(json_str)
                contribs.sort(key=lambda x: x['total'], reverse=True)
                for contrib in contribs:
                    author = contrib["author"]["login"]
                    # Count line of codes
                    line_cnt = 0
                    weeks = contrib["weeks"]
                    for week in weeks:
                        line_cnt += week["a"] + week["d"]
                    tot_line_cnt += line_cnt
                    if (author in author_line_cnt):
                        author_line_cnt[author] += line_cnt
                    else:
                        author_line_cnt[author] = line_cnt
                    # Count commits
                    cmt_cnt = contrib["total"]
                    tot_cmt_cnt += cmt_cnt
                    if (author in author_cmt_cnt):
                        author_cmt_cnt[author] += cmt_cnt
                    else:
                        author_cmt_cnt[author] = cmt_cnt
                    print("%-15s: %3s commits / %5d lines of code"
                          % (author, cmt_cnt, line_cnt))
        except urllib.error.HTTPError as err:
            print(err)
            print(err.read().decode('utf-8'))
            sys.exit(1)
        print("")
    print("%s:" % owner)
    print("Contributed commits:")
    sorted_keys = sorted(author_cmt_cnt, key=author_cmt_cnt.get, reverse=True)
    author_cmt_cnt = [(key, author_cmt_cnt[key]) for key in sorted_keys]
    for author, cmt_cnt in author_cmt_cnt:
        print("%-15s: %3d commits (%2d%%)"
              % (author, cmt_cnt, cmt_cnt * 100 // tot_cmt_cnt))
    print("Contributed line of codes:")
    sorted_keys = sorted(author_line_cnt, key=author_line_cnt.get, reverse=True)
    author_line_cnt = [(key, author_line_cnt[key]) for key in sorted_keys]
    for author, line_cnt in author_line_cnt:
        print("%-16s: %5d lines of code (%2d%%)"
              % (author, line_cnt, line_cnt * 100 // tot_line_cnt))
