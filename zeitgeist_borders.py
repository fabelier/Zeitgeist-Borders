#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Zeitgeist Borders (https://github.com/fabelier/Zeitgeist-Borders/) 
# Developed by Antoine Mazières, Samuel Huron and Julien Palard.
# Contact : admin at fabelier dot org
#
# Zeitgeist Borders is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zeitgeist Borders is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zeitgeist Borders.  If not, see <http://www.gnu.org/licenses/>.

try:
    import pymongo
except:
    pass
import time
import urllib
import json
from cctld import cctlds
from threading import Thread
from Queue import Queue
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)


def memoized(function):
    from pymongo.son_manipulator import SONManipulator

    class EncodeDotsInKeys(SONManipulator):

        def hide_dots(self, value):
            return value.replace('.', u'☃')

        def show_dots(self, value):
            return value.replace(u'☃', '.')

        def transform_incoming(self, son, collection):
            son = dict([(self.hide_dots(key), value)
                        for key, value
                        in son.iteritems()])
            for key, value in son.items():
                if isinstance(value, dict):
                    son[key] = self.transform_incoming(value, collection)
            return son

        def transform_outgoing(self, son, collection):
            son = dict([(self.show_dots(key), value)
                        for key, value
                        in son.iteritems()])
            for key, value in son.items():
                if isinstance(value, dict):
                    son[key] = self.transform_outgoing(value, collection)
            return son

    try:
        db = pymongo.Connection(network_timeout=.2).zeitgeist
        db.add_son_manipulator(EncodeDotsInKeys())
        cache = db.cache
    except:
        cache = None
    if cache:
        def _(arg):
            _id = arg.replace('.', '_')
            cached = cache.find_one({'_id': _id})
            if cached is not None:
                cache.update({'_id': _id}, {'$inc': {'hits': 1}})
                return cached['value']
            value = function(arg)
            cache.insert({'_id': _id, 'value': value, 'hits': 0})
            return value
    else:
        def _(arg):
            return function(arg)
    return _


def google_instant(queue, country, tld, query, tries=0):
    """
    Response look like :
    [
        "android",
        [
            "http://www.android.com/",
            "android market",
            "android",
            "android phones"
        ],
        [
            "Android.com - Experience Nexus One",
            "",
            "",
            ""
        ],
        [],
        {
            "google:suggesttype": [
                "NAVIGATION",
                "QUERY",
                "QUERY",
                "QUERY"
            ]
        }
    ]

    """
    try:
        http_query = 'http://www.google.%s/complete/search?sugexp=chrome,mod=0&client=chrome&%s' \
            % (tld, urllib.urlencode({'q': query.encode('utf-8')}))
        response = urllib.urlopen(http_query).read()
        response = unicode(response, errors='ignore')
        results = json.loads(response, encoding='utf-8')
        results = [r.replace(query + ' ', '')
                   for i, r in enumerate(results[1])
                   if r != query
                   and results[4]['google:suggesttype'][i] == 'QUERY']
        queue.put((tld, results))
    except Exception as ex:
        log.error("Error %s querying %s for country %s",
                  str(ex), http_query, country)
        if tries < 2:
            time.sleep(1)
            google_instant(queue, country, tld, query, tries + 1)
        else:
            queue.put((tld, []))


@memoized
def google_instants(query):
    q = Queue()
    result = {}
    for country, tld in cctlds.iteritems():
        Thread(target=google_instant, args=(q, country, tld, query)).start()
    waiting = len(cctlds)
    while waiting > 0:
        country, suggestions = q.get()
        result[country] = suggestions
        waiting -= 1
    return result


def update():
    """
    @todo update suggestions country that are empty or too old
    This should be started daily as a cron task.
    """
    cache = pymongo.Connection(network_timeout=.2).zeitgeist.cache
    for entry in cache.find():
        value = {}
        for country, response in entry['value'].iteritems():
            value[cctlds[country][1:]] = response
        cache.update({'_id': entry['_id']}, {'$set': {'value': value}},
                     safe=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: %s SEARCH QUERY" % sys.argv[0]
        sys.exit(1)
    if sys.argv[1] == '--update':
        update()
        sys.exit(0)
    for country, responses in google_instants(' '.join(sys.argv[1:])).iteritems():
        print country
        for response in responses:
            print " * " + response
