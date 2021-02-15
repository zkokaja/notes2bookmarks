#!/usr/bin/env python

import argparse
import json
import os.path as path
import re
from os import listdir
from socket import timeout
from sys import stderr, stdout
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

# The file starts with the following text:
prelude = '''\
<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!--This is an automatically generated file.
    It will be read and overwritten.
    Do Not Edit! -->
    <Title>Bookmarks</Title>
    <H1>Bookmarks</H1>
'''

# An item may be a subfolder, shortcut, feed, Web Slice, or icon.
# If {item} refers to a subfolder, it is:
# Note - can add ADD_DATE to <H3> if needed
subfolder_begin = '''\
    <DT><H3 FOLDED>{title}</H3>
    <DL><p>
'''
subfolder_end = '''\
    </DL><p>
'''

# If {item} refers to a shortcut, it is:
# Note - can add ADD_DATE, LAST_VISIT, and LAST_MODIFIED to <A> if needed.
#        Firefox also adds a csv list of TAGS and SHORTCUTURL for keywords.
shortcut = '<DT><A HREF="{url}">{title}</A>\n'

# Do I care about ftp, file, or other protocols?
regex = r'https?://[-A-Za-z0-9\+&@#/%?=~_|.;]*[-A-Za-z0-9\+&@#/%=~_|]'
pattern = re.compile(regex, re.M)


def find_urls(filepath, folder_per_note):
    try:
        with open(filepath, 'r') as fp:
            contents = fp.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='iso-8859-1') as fp:
            contents = fp.read()

    items = [{
        'url': url,
        'type': 'shortcut',
        'path': filepath
    } for url in re.findall(pattern, contents)]

    if folder_per_note:
        dirname = path.basename(filepath).replace('.html', '')
        if len(items) == 0:
            return []
        return [{
            'title': dirname,
            'type': 'subfolder',
            'path': filepath,
            'items': items}]
    else:
        return items


def process_path(filepath, folder_per_note):
    if path.isfile(filepath):
        return find_urls(filepath, folder_per_note)
    elif path.isdir(filepath):
        items = []
        for subdir in listdir(filepath):
            nextpath = path.join(filepath, subdir)
            urls = process_path(nextpath, folder_per_note)  # Recurse
            if len(urls) > 0:
                items.extend(urls)

        dirname = path.basename(filepath)
        return [{
            'title': dirname,
            'type': 'subfolder',
            'path': filepath,
            'items': items
        }]


def get_webpage_title(url):
    try:
        with urlopen(url, timeout=10) as fp:
            dom = BeautifulSoup(fp, features='html.parser')
            if dom.title is not None:
                return dom.title.text
    except HTTPError as e:
        stderr.write(f'Got HTTP Error {e.code}: {e.reason} for site: {url}\n')
        return None
    except URLError as e:
        stderr.write(f'Got URL Error: {e} for site: {url}\n')
        return None
    except timeout:
        stderr.write(f'Socket timeout for site: {url}\n')
        return None
    except Exception:
        stderr.write(f'Possibly malformed URL: {url}\n')
        return None
    except:
        stderr.write(f'Something really strange: {url}\n')
        return None


def __json2bookmarks(data, fp, url_to_title, query_title):
    if data['type'] == 'shortcut':
        url = data['url']
        title = data.get('title')
        if title is None:
            title = url_to_title.get(url)
            if title is None and query_title:
                title = get_webpage_title(url)

        if title is None:
            title = url

        # Write out the shortcut
        fp.write(shortcut.format(url=url, title=title))
    elif data['type'] == 'subfolder':
        fp.write(subfolder_begin.format(title=data['title']))
        for item in data['items']:
            __json2bookmarks(item, fp, url_to_title, query_title)  # Recurse
        fp.write(subfolder_end)


def json2bookmarks(data, fp, url_to_title, query_title):
    fp.write(prelude)
    for item in data:
        __json2bookmarks(item, fp, url_to_title, query_title)
    fp.write('</HTML>')


def extract_titles(html_files):
    if isinstance(html_files, str):
        html_files = [html_files]
    elif not isinstance(html_files, list):
        raise ValueError

    url_to_title = {}
    for html_file in html_files:
        url_pattern = re.compile('<A HREF=\"(.*)\">(.*)</A>', re.M)
        # with open(html_file, 'r') as fp:
        contents = html_file.read()
        url_to_title.update(dict(re.findall(url_pattern, contents)))

    return url_to_title


def main(args):

    # 1. Read in the data
    data = process_path(args.notes, args.folder_per_note)[0]['items']

    # 2. Read in cached titles
    url_to_title = None
    if args.titles is not None and len(args.titles) > 0:
        url_to_title = extract_titles(args.titles)

    # 3. Convert to bookmarks
    json2bookmarks(data, args.outfile, url_to_title, args.query_title)

    # 4. Optionally save the json data
    if args.json_out is not None:
        json.dump(data, args.json_out, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('notes', type=str)
    parser.add_argument('outfile', type=argparse.FileType('w'), default=stdout)
    parser.add_argument('--json-out',
                        type=argparse.FileType('w'),
                        default=None)
    parser.add_argument('--titles', nargs='*', type=argparse.FileType('r'))
    parser.add_argument('--query-title', action='store_true')
    parser.add_argument('--folder-per-note', action='store_true')
    args = parser.parse_args()
    main(args)
