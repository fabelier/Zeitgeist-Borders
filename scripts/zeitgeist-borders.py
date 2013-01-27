#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
#

import sys
import urllib
import re
import socket
import multiprocessing
from multiprocessing import Process, Queue

## tweak a textmate bug
reload(sys) 
sys.setdefaultencoding("utf-8")
##

socket.setdefaulttimeout(1)

# List of all Google's domain names listed at http://www.google.com/supported_domains
# Dictionary built with ./get_google_domains.py
googles = {'United States': '.com.ly','United States': '.com','Canada': '.ca', 'Sao Tome and Principe': '.st', 'Turkmenistan': '.tm', 'Saint Helena': '.sh', 'Lithuania': '.lt', 'Pridnestrovie (Transnistria)': '.md', 'Cameroon': '.cm', 'Burkina Faso': '.bf', 'Somaliland': '.so', 'Congo, Democratic Republic of the (Congo \x96 Kinshasa)': '.cd', 'American Samoa': '.as', 'Slovenia': '.si', 'Bosnia and Herzegovina': '.ba', 'Jordan': '.jo', 'Saint Barthelemy': '.gp', 'Dominica': '.dm', 'Maldives': '.mv', 'Timor-Leste (East Timor)': '.tl', 'Isle of Man': '.im', 'Gabon': '.ga', 'Niue': '.nu', 'Jersey': '.je', 'South Ossetia': '.ge', 'Greenland': '.gl', 'Samoa': '.ws', 'United Arab Emirates': '.ae', 'Azerbaijan': '.az', "China, People's Republic of": '.cn', 'Czech Republic': '.cz', 'San Marino': '.sm', 'Mongolia': '.mn', 'France': '.fr', 'Rwanda': '.rw', 'Slovakia': '.sk', 'Somalia': '.so', 'Laos': '.la', 'Nauru': '.nr', 'Norway': '.no', 'Malawi': '.mw', 'Benin': '.bj', 'Bahamas, The': '.bs', 'Montenegro': '.me', 'Togo': '.tg', 'Armenia': '.am', 'Tonga': '.to', 'Finland': '.fi', 'Central African Republic': '.cf', 'Mauritius': '.mu', 'Liechtenstein': '.li', 'British Virgin Islands': '.vg', 'Mali': '.ml', 'Russia': '.ru', 'Bulgaria': '.bg', 'Romania': '.ro', 'Portugal': '.pt', 'Tokelau': '.tk', 'Sweden': '.se', 'Senegal': '.sn', 'Hungary': '.hu', 'Niger': '.ne', 'Saint Martin': '.gp', 'Luxembourg': '.lu', 'Andorra': '.ad', 'Ireland': '.ie', 'Belarus': '.by', 'Algeria': '.dz', 'Pitcairn Islands': '.pn', 'Congo, Republic of the (Congo \x96 Brazzaville)': '.cg', 'Chile': '.cl', 'Belgium': '.be', 'Kiribati': '.ki', 'Haiti': '.ht', 'Iraq': '.iq', 'Georgia': '.ge', 'Denmark': '.dk', 'Poland': '.pl', 'Moldova': '.md', 'Croatia': '.hr', 'Guernsey': '.gg', 'Switzerland': '.ch', 'Seychelles': '.sc', 'Chad': '.td', 'Estonia': '.ee', 'Djibouti': '.dj', 'Spain': '.es', 'Burundi': '.bi', 'Madagascar': '.mg', 'Italy': '.it', 'Vanuatu': '.vu', 'Micronesia': '.fm', 'Netherlands': '.nl', "Cote d'Ivoire (Ivory Coast)": '.ci', 'Iceland': '.is', 'Austria': '.at', 'Germany': '.de', 'Abkhazia': '.ge', 'Kazakhstan': '.kz', 'Kyrgyzstan': '.kg', 'Montserrat': '.ms', 'Macedonia': '.mk', 'Trinidad and Tobago': '.tt', 'Latvia': '.lv', 'Guyana': '.gy', 'Guadeloupe': '.gp', 'Honduras': '.hn', 'Tunisia': '.tn', 'Serbia': '.rs', 'Gambia, The': '.gm', 'Greece': '.gr', 'Sri Lanka': '.lk', 'Palestinian Territories (Gaza Strip and West Bank)': '.ps', 'Nagorno-Karabakh': '.az'}

# A tiny dict for debug
#googles = {'Canada': '.ca', 'France': '.fr', 'Brazil': '.com.br', 'Germany': '.de'}

query = sys.argv[1]
query = query.replace(' ', '+')

def get_q(country, tld):
	try:
		d = re.search('\[\[.*\]\]', urllib.urlopen('http://www.google%s/complete/search?q=%s' % (tld, query)).read()).group()
		q.put((country, d))
	except IOError:
		q.put((country, 'error'))


if __name__ == '__main__':
	result = {} 
	q = Queue()
	for country, tld in googles.iteritems():
		p = multiprocessing.Process(target=get_q, args=(country, tld))
		p.start()
		#result[q.get()[0]] = result[q.get()[1]]
	while True:
		print q.get()
	p.join()

