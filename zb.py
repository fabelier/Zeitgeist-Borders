# -*- coding: utf-8 -*-
import os
import re
import logging
import pymongo
import random
import sys
import urllib
import socket
import multiprocessing
import json
from multiprocessing import Process, Queue

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.httpexceptions import HTTPFound
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import view_config


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))

# List of all Google's domain names listed at http://www.google.com/supported_domains
# Dictionary built with ./get_google_domains.py
#googles = {'Canada': '.ca', 'Sao Tome and Principe': '.st', 'Turkmenistan': '.tm', 'Saint Helena': '.sh', 'Lithuania': '.lt', 'Pridnestrovie (Transnistria)': '.md', 'Cameroon': '.cm', 'Burkina Faso': '.bf', 'Somaliland': '.so', 'Congo, Democratic Republic of the (Congo \x96 Kinshasa)': '.cd', 'American Samoa': '.as', 'Slovenia': '.si', 'Bosnia and Herzegovina': '.ba', 'Jordan': '.jo', 'Saint Barthelemy': '.gp', 'Dominica': '.dm', 'Maldives': '.mv', 'Timor-Leste (East Timor)': '.tl', 'Isle of Man': '.im', 'Gabon': '.ga', 'Niue': '.nu', 'Jersey': '.je', 'South Ossetia': '.ge', 'Greenland': '.gl', 'Samoa': '.ws', 'United Arab Emirates': '.ae', 'Azerbaijan': '.az', "China, People's Republic of": '.cn', 'Czech Republic': '.cz', 'San Marino': '.sm', 'Mongolia': '.mn', 'France': '.fr', 'Rwanda': '.rw', 'Slovakia': '.sk', 'Somalia': '.so', 'Laos': '.la', 'Nauru': '.nr', 'Norway': '.no', 'Malawi': '.mw', 'Benin': '.bj', 'Bahamas, The': '.bs', 'Montenegro': '.me', 'Togo': '.tg', 'Armenia': '.am', 'Tonga': '.to', 'Finland': '.fi', 'Central African Republic': '.cf', 'Mauritius': '.mu', 'Liechtenstein': '.li', 'British Virgin Islands': '.vg', 'Mali': '.ml', 'Russia': '.ru', 'Bulgaria': '.bg', 'Romania': '.ro', 'Portugal': '.pt', 'Tokelau': '.tk', 'Sweden': '.se', 'Senegal': '.sn', 'Hungary': '.hu', 'Niger': '.ne', 'Saint Martin': '.gp', 'Luxembourg': '.lu', 'Andorra': '.ad', 'Ireland': '.ie', 'Belarus': '.by', 'Algeria': '.dz', 'Pitcairn Islands': '.pn', 'Congo, Republic of the (Congo \x96 Brazzaville)': '.cg', 'Chile': '.cl', 'Belgium': '.be', 'Kiribati': '.ki', 'Haiti': '.ht', 'Iraq': '.iq', 'Georgia': '.ge', 'Denmark': '.dk', 'Poland': '.pl', 'Moldova': '.md', 'Croatia': '.hr', 'Guernsey': '.gg', 'Switzerland': '.ch', 'Seychelles': '.sc', 'Chad': '.td', 'Estonia': '.ee', 'Djibouti': '.dj', 'Spain': '.es', 'Burundi': '.bi', 'Madagascar': '.mg', 'Italy': '.it', 'Vanuatu': '.vu', 'Micronesia': '.fm', 'Netherlands': '.nl', "Cote d'Ivoire (Ivory Coast)": '.ci', 'Iceland': '.is', 'Austria': '.at', 'Germany': '.de', 'Abkhazia': '.ge', 'Kazakhstan': '.kz', 'Kyrgyzstan': '.kg', 'Montserrat': '.ms', 'Macedonia': '.mk', 'Trinidad and Tobago': '.tt', 'Latvia': '.lv', 'Guyana': '.gy', 'Guadeloupe': '.gp', 'Honduras': '.hn', 'Tunisia': '.tn', 'Serbia': '.rs', 'Gambia, The': '.gm', 'Greece': '.gr', 'Sri Lanka': '.lk', 'Palestinian Territories (Gaza Strip and West Bank)': '.ps', 'Nagorno-Karabakh': '.az'}

# A tiny dict for debug
googles = {'Canada': '.ca', 'France': '.fr', 'Brazil': '.com.br', 'Germany': '.de'}

def get_q(queue, country, tld, query):
    try:
        response = urllib.urlopen('http://www.google%s/complete/search?q=%s' % (tld, query)).read()
        result = json.loads(response.replace('window.google.ac.h(', '')[:-1].decode('latin1'))
        queue.put((country, result))
    except IOError:
        queue.put((country, 'error'))


@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    result = []
    q = Queue()
    if request.method == 'POST' and request.POST.get('query'):
        query = request.POST['query']
        query = query.replace(' ', '+')
        for country, tld in googles.iteritems():
            p = multiprocessing.Process(target=get_q, args=(q, country, tld, query))
            p.start()
        waiting = len(googles)
        while waiting > 0:
            result.append(q.get())
            waiting -= 1
        p.join()
        return {'result': result}
    else:
        return {}


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    return {}


@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    pass

@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    log.warn('Initializing database...')

session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

settings = {"mako.directories": os.path.join(here, "templates")}
config = Configurator(settings=settings, session_factory=session_factory)

config.add_route('home', '/')

config.add_static_view('static', os.path.join(here, 'static'))

config.scan()

application = config.make_wsgi_app()
