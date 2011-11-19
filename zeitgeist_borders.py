#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import re
import time
import threading
import urllib
import json
import pymongo
from threading import Thread
from Queue import Queue
import logging

log = logging.getLogger(__file__)

# List of all Google's domain names listed at http://www.google.com/supported_domains
# Dictionary built with ./get_google_domains.py
googles = {'Canada': '.ca', 'Sao Tome and Principe': '.st', 'Turkmenistan': '.tm', 'Saint Helena': '.sh', 'Lithuania': '.lt', 'Pridnestrovie (Transnistria)': '.md', 'Cameroon': '.cm', 'Burkina Faso': '.bf', 'Somaliland': '.so', 'Congo, Democratic Republic of the (Congo-Kinshasa)': '.cd', 'American Samoa': '.as', 'Slovenia': '.si', 'Bosnia and Herzegovina': '.ba', 'Jordan': '.jo', 'Saint Barthelemy': '.gp', 'Dominica': '.dm', 'Maldives': '.mv', 'Timor-Leste (East Timor)': '.tl', 'Isle of Man': '.im', 'Gabon': '.ga', 'Niue': '.nu', 'Jersey': '.je', 'South Ossetia': '.ge', 'Greenland': '.gl', 'Samoa': '.ws', 'United Arab Emirates': '.ae', 'Azerbaijan': '.az', "China, People's Republic of": '.cn', 'Czech Republic': '.cz', 'San Marino': '.sm', 'Mongolia': '.mn', 'France': '.fr', 'Rwanda': '.rw', 'Slovakia': '.sk', 'Somalia': '.so', 'Laos': '.la', 'Nauru': '.nr', 'Norway': '.no', 'Malawi': '.mw', 'Benin': '.bj', 'Bahamas, The': '.bs', 'Montenegro': '.me', 'Togo': '.tg', 'Armenia': '.am', 'Tonga': '.to', 'Finland': '.fi', 'Central African Republic': '.cf', 'Mauritius': '.mu', 'Liechtenstein': '.li', 'British Virgin Islands': '.vg', 'Mali': '.ml', 'Russia': '.ru', 'Bulgaria': '.bg', 'Romania': '.ro', 'Portugal': '.pt', 'Tokelau': '.tk', 'Sweden': '.se', 'Senegal': '.sn', 'Hungary': '.hu', 'Niger': '.ne', 'Saint Martin': '.gp', 'Luxembourg': '.lu', 'Andorra': '.ad', 'Ireland': '.ie', 'Belarus': '.by', 'Algeria': '.dz', 'Pitcairn Islands': '.pn', 'Congo, Republic of the (Congo-Brazzaville)': '.cg', 'Chile': '.cl', 'Belgium': '.be', 'Kiribati': '.ki', 'Haiti': '.ht', 'Iraq': '.iq', 'Georgia': '.ge', 'Denmark': '.dk', 'Poland': '.pl', 'Moldova': '.md', 'Croatia': '.hr', 'Guernsey': '.gg', 'Switzerland': '.ch', 'Seychelles': '.sc', 'Chad': '.td', 'Estonia': '.ee', 'Djibouti': '.dj', 'Spain': '.es', 'Burundi': '.bi', 'Madagascar': '.mg', 'Italy': '.it', 'Vanuatu': '.vu', 'Micronesia': '.fm', 'Netherlands': '.nl', "Cote d'Ivoire (Ivory Coast)": '.ci', 'Iceland': '.is', 'Austria': '.at', 'Germany': '.de', 'Abkhazia': '.ge', 'Kazakhstan': '.kz', 'Kyrgyzstan': '.kg', 'Montserrat': '.ms', 'Macedonia': '.mk', 'Trinidad and Tobago': '.tt', 'Latvia': '.lv', 'Guyana': '.gy', 'Guadeloupe': '.gp', 'Honduras': '.hn', 'Tunisia': '.tn', 'Serbia': '.rs', 'Gambia, The': '.gm', 'Greece': '.gr', 'Sri Lanka': '.lk', 'Palestinian Territories (Gaza Strip and West Bank)': '.ps', 'Nagorno-Karabakh': '.az'}

# A tiny dict for debug
#googles = {'Canada': '.ca', 'France': '.fr', 'Brazil': '.com.br', 'Germany': '.de'}


def memoized(function):
    try:
        cache = pymongo.Connection(network_timeout=.2).zeitgeist.cache
    except:
        cache = None
    if cache:
        cache.ensure_index("key")
        def _(arg):
            cached = cache.find_one({'key': arg})
            if cached is not None:
                cache.update(cached, {'$inc': {'hits': 1}})
                return cached['value']
            value = function(arg)
            cache.insert({'key': arg, 'value': value, 'hits': 0})
            return value
    else:
        def _(arg):
            return function(arg)
    return _


def google_instant(queue, country, tld, query, tries=0):
    try:
        response = urllib.urlopen('http://www.google%s/complete/search?%s' % (tld, urllib.urlencode({'q': query}))).read()
        results = json.loads(response.replace('window.google.ac.h(', '')[:-1], encoding='latin1')
        results = [r[0].encode('utf-8').replace(query + ' ', '') for r in results[1] if r[0].encode('utf-8') != query]
        queue.put((country, results))
    except Exception as ex:
        log.error(str(ex))
        if tries < 2:
            time.sleep(1)
            google_instant(queue, country, tld, query, tries + 1)
        else:
            queue.put((country, {}))


@memoized
def google_instants(query):
    q = Queue()
    result = []
    for country, tld in googles.iteritems():
        Thread(target=google_instant, args=(q, country, tld, query)).start()
    waiting = len(googles)
    while waiting > 0:
        result.append(q.get())
        waiting -= 1
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: %s SEARCH QUERY" % sys.argv[0]
        sys.exit(1)
    for country, responses in google_instants(' '.join(sys.argv[1:])):
        print country
        for response in responses:
            print " * " + response
