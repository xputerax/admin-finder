#!/usr/bin/python3
'''
Admin Page Finder
Copyleft A.D 2019
'''

import sys
import urllib3

def help():
    print('=' * 50)
    print (
        'Admin Page Finder \n' \
        'Requires python 3 and above \n' \
        '\n' \
        'python', sys.argv[0], '<website> [ext1[,ext2[,ext3...]]] \n' \
        'python', sys.argv[0], 'https://localhost/blog/ \n' \
        'python', sys.argv[0], 'https://localhost/blog/ php,php4,asp ' \
    )
    print('=' * 50)
pass

def normalize_url(url):
    normalized = ''
    if url[0:7] != 'http://' and url[0:8] != 'https://': normalized += 'http://'
    normalized += url
    if url[-1] != '/': normalized += '/'
    return normalized
pass

def find_admin_pages(url, exts):
    http = urllib3.PoolManager()
    fh = open('admin_list.txt', 'r')
    paths = []

    for line in fh.readlines():
        path = line.strip()
        if '{ext}' in path:
            for ext in exts:
                paths.append(path.replace('{ext}', ext))
        else:
            paths.append(path)

    for path in paths:
        full_url = url + path
        try:
            req = http.request('GET', full_url)

            if req.status in range(400, 501):
                print('[-] Error: {} [{}]'.format(full_url, req.status))
            elif req.status == '200':
                print('[+] Found: {} [{}]'.format(full_url, req.status))
            else:
                print('[?] ?: {} [{}]'.format(full_url, req.status))
        except Exception as e:
            print('[!] Error: {}\n{}\n'.format(full_url, str(e)))
pass

def main():
    url = ''
    exts = []

    if len(sys.argv) == 1:
        help()
        sys.exit()
    elif len(sys.argv) == 2:
        exts = ['php', 'asp']
    elif len(sys.argv) == 3:
        exts = sys.argv[2].split(',')
    else:
        help()
        sys.exit()

    url = normalize_url(sys.argv[1])

    find_admin_pages(url, exts)
pass

if __name__ == '__main__':
    main()