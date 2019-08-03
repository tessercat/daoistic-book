#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import urllib2
from bs4 import BeautifulSoup
from collections import OrderedDict


def _html(url):
    """ Return the URL as HTML. """
    request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        print err.headers
        print err.read()
        return
    return response.read()

def _process(chapter, data):
    """ Populate the ``data`` dict with chapter characters. """
    soup = BeautifulSoup(data[chapter].get('html'))
    table = soup.find(id='pg0')
    if table:
        for tr in table.findAll('tr'):
            anchors = tr.contents[0].findAll('a')
            if anchors[0]['href'] == 'mawangdui':
                tag = anchors[1]['href']
            else:
                tag = anchors[0]['href']
            print 'Chapter %s tag %s processed' % (chapter, tag)
            data[chapter][tag] = tr.contents[1].span.text
        return True
    print 'Error processing HTML for chapter %s' % chapter

def scrape(nodes):
    """ Scrape ctext parallel passage nodes.

    The ``nodes`` argument is a dict mapping chapter number to a ctext
    parallel passage node ID.
    
    This script reads chapter data from a json-formatted file, processes raw
    ctext data for per-source chapter data, and writes the dict back to file.
    Data output includes raw HTML scraped from ctext. If present, this data
    is used to generate soup. If absent, the page is downloaded from ctext
    and stored in the dict before processing. This should avoid hammering
    ctext too much, even if this script isn't strictly within the limits of
    ctext's no-automated-access rule.
    """

    # Get existing data.
    try:
        with open('ctext.json') as fd:
            data = json.load(fd)
    except:
        data = {}

    # Process the data.
    for chapter, node in nodes.iteritems():
        if data.get(chapter) and data[chapter].get('html'):

            # Found existing soup, process it.
            print 'Found soup for chapter %s' % chapter
            if not _process(chapter, data):
                break
            time.sleep(45)
            continue

        # Get new soup, process it.
        url = 'http://ctext.org/text.pl?node=%s&if=en&show=parallel' % node
        print 'Fetching HTML for chapter %s from %s' % (chapter, url)
        data[chapter] = {'html': _html(url)}
        if not _process(chapter, data):
            break

    # Write the data.
    with open('ctext.json', 'w') as fd:
        json.dump(data, fd, sort_keys=True, indent=4)

if __name__ == '__main__':
    nodes = OrderedDict()
    base_node = 11591
    for index in range(1, 82):
        nodes[str(index).zfill(2)] = str(base_node + index)
    scrape(nodes)
