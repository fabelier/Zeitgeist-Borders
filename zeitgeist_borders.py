#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import pymongo
except:
    pass
import re
import time
import threading
import urllib
import json
from threading import Thread
from Queue import Queue
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)

# List of all Google's domain names listed at http://www.google.com/supported_domains
# Dictionary built with ./get_google_domains.py
googles = {'Canada': 'ca', 'Saint Martin': 'gp', 'Sao Tome and Principe': 'st', 'Turkmenistan': 'tm', 'Saint Helena': 'sh', 'Lithuania': 'lt', 'Cambodia': 'kh', 'Ethiopia': 'et', 'Pridnestrovie (Transnistria)': 'md', 'Argentina': 'ar', 'Bolivia': 'bo', 'Bahamas, The': 'bs', 'Burkina Faso': 'bf', 'Bahrain': 'bh', 'Saudi Arabia': 'sa', 'Congo, Democratic Republic of the (Congo \x96 Kinshasa)': 'cd', 'Cape Verde': 'cv', 'Slovenia': 'si', 'Guatemala': 'gt', 'Bosnia and Herzegovina': 'ba', 'Jordan': 'jo', 'Saint Barthelemy': 'gp', 'Ashmore and Cartier Islands': 'au', 'Dominica': 'dm', 'China, Republic of (Taiwan)': 'tw', 'Maldives': 'mv', 'Timor-Leste (East Timor)': 'tl', 'Pakistan': 'pk', 'Oman': 'om', 'Tanzania': 'tz', 'Seychelles': 'sc', 'Gabon': 'ga', 'Niue': 'nu', 'New Zealand': 'nz', 'Jersey': 'je', 'Jamaica': 'jm', 'South Ossetia': 'ge', 'Greenland': 'gl', 'Samoa': 'ws', 'Norfolk Island': 'nf', 'United Arab Emirates': 'ae', 'India': 'in', 'Azerbaijan': 'az', 'Lesotho': 'ls', 'Saint Vincent and the Grenadines': 'vc', 'Kenya': 'ke', 'Tajikistan': 'tj', "China, People's Republic of": 'cn', 'Turkey': 'tr', 'Afghanistan': 'af', 'Bangladesh': 'bd', 'Solomon Islands': 'sb', 'San Marino': 'sm', 'Mongolia': 'mn', 'France': 'fr', 'Palestinian Territories (Gaza Strip and West Bank)': 'ps', 'Rwanda': 'rw', 'Slovakia': 'sk', 'Somalia': 'so', 'Peru': 'pe', 'Laos': 'la', 'Nauru': 'nr', 'Norway': 'no', 'Malawi': 'mw', 'Cook Islands': 'ck', 'Benin': 'bj', 'Cuba': 'cu', 'Cameroon': 'cm', 'Montenegro': 'me', 'Togo': 'tg', 'Armenia': 'am', 'Dominican Republic': 'do', 'Ukraine': 'ua', 'Ghana': 'gh', 'Tonga': 'to', 'Finland': 'fi', 'Libya': 'ly', 'Somaliland': 'so', 'Indonesia': 'id', 'Central African Republic': 'cf', 'Mauritius': 'mu', 'Liechtenstein': 'li', 'Belarus': 'by', 'British Virgin Islands': 'vg', 'Mali': 'ml', 'Russia': 'ru', 'Bulgaria': 'bg', 'United States': 'com', 'Romania': 'ro', 'Angola': 'ao', 'Chad': 'td', 'South Africa': 'za', 'Tokelau': 'tk', 'Cyprus': 'cy', 'Sweden': 'se', 'Qatar': 'qa', 'Malaysia': 'my', 'Austria': 'at', 'Vietnam': 'vn', 'Mozambique': 'mz', 'Uganda': 'ug', 'Hungary': 'hu', 'Niger': 'ne', 'Isle of Man': 'im', 'Brazil': 'br', 'U.S. Virgin Islands': 'vi', 'Kuwait': 'kw', 'Panama': 'pa', 'Guyana': 'gy', 'Costa Rica': 'cr', 'Luxembourg': 'lu', 'American Samoa': 'as', 'Andorra': 'ad', 'Gibraltar': 'gi', 'Ireland': 'ie', 'Nigeria': 'ng', 'Ecuador': 'ec', 'Czech Republic': 'cz', 'Brunei': 'bn', 'Australia': 'au', 'Vanuatu': 'vu', 'Algeria': 'dz', 'El Salvador': 'sv', 'Pitcairn Islands': 'pn', 'Congo, Republic of the (Congo \x96 Brazzaville)': 'cg', 'Chile': 'cl', 'Puerto Rico': 'pr', 'Belgium': 'be', 'Kiribati': 'ki', 'Haiti': 'ht', 'Belize': 'bz', 'Hong Kong': 'hk', 'Sierra Leone': 'sl', 'Georgia': 'ge', 'Denmark': 'dk', 'Philippines': 'ph', 'Moldova': 'md', 'Morocco': 'ma', 'Croatia': 'hr', 'Micronesia': 'fm', 'Guernsey': 'gg', 'Thailand': 'th', 'Switzerland': 'ch', 'Korea, Republic of  (South Korea)': 'kr', 'Iraq': 'iq', 'Portugal': 'pt', 'Estonia': 'ee', 'Uruguay': 'uy', 'Lebanon': 'lb', 'Northern Cyprus': 'tr', 'Uzbekistan': 'uz', 'Tunisia': 'tn', 'Djibouti': 'dj', 'Antigua and Barbuda': 'ag', 'Spain': 'es', 'Colombia': 'co', 'Burundi': 'bi', 'Fiji': 'fj', 'Madagascar': 'mg', 'Italy': 'it', 'Nepal': 'np', 'Malta': 'mt', 'Netherlands': 'nl', 'Anguilla': 'ai', 'Venezuela': 've', "Cote d'Ivoire (Ivory Coast)": 'ci', 'Israel': 'il', 'Iceland': 'is', 'Zambia': 'zm', 'Senegal': 'sn', 'Trinidad and Tobago': 'tt', 'Zimbabwe': 'zw', 'Germany': 'de', 'Abkhazia': 'ge', 'Kazakhstan': 'kz', 'Poland': 'pl', 'Kyrgyzstan': 'kg', 'Montserrat': 'ms', 'Coral Sea Islands': 'au', 'Macedonia': 'mk', 'Sri Lanka': 'lk', 'Latvia': 'lv', 'Japan': 'jp', 'Guadeloupe': 'gp', 'Honduras': 'hn', 'Mexico': 'mx', 'Egypt': 'eg', 'Nicaragua': 'ni', 'Singapore': 'sg', 'Serbia': 'rs', 'United Kingdom': 'uk', 'Gambia, The': 'gm', 'Greece': 'gr', 'Paraguay': 'py', 'Namibia': 'na', 'Nagorno-Karabakh': 'az', 'Botswana': 'bw'}
# A tiny dict for debug
#googles = {'Canada': '.ca', 'France': '.fr', 'Brazil': '.com.br', 'Germany': '.de'}


def memoized(function):
    try:
        cache = pymongo.Connection(network_timeout=.2).zeitgeist.cache
    except:
        cache = None
    if cache:
        def _(arg):
            cached = cache.find_one({'_id': arg})
            if cached is not None:
                cache.update({'_id': arg}, {'$inc': {'hits': 1}})
                return cached['value']
            value = function(arg)
            cache.insert({'_id': arg, 'value': value, 'hits': 0})
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
        response = urllib.urlopen('http://www.google.%s/complete/search?client=chrome&%s' % (tld, urllib.urlencode({'q': query}))).read()
        results = json.loads(response, encoding='latin1')
        results = [r.replace(query + ' ', '')
                   for i, r in enumerate(results[1])
                   if r != query and results[4]['google:suggesttype'][i] == 'QUERY']
        queue.put((tld, results))
    except Exception as ex:
        log.error("Error %s querying %s for country %s",
                  str(ex), query, country)
        if tries < 2:
            time.sleep(1)
            google_instant(queue, country, tld, query, tries + 1)
        else:
            queue.put((tld, []))

@memoized
def google_instants(query):
    q = Queue()
    result = {}
    for country, tld in googles.iteritems():
        Thread(target=google_instant, args=(q, country, tld, query)).start()
    waiting = len(googles)
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
            value[googles[country][1:]] = response
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
