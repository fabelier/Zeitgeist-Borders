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

import os, sys, string, urllib, csv

## tweak a textmate bug
reload(sys) 
sys.setdefaultencoding("utf-8")
##

d = urllib.urlopen('http://www.google.com/supported_domains').read().replace('\n', '').split('.')[1:]
country_tld = {}

with open ('../documentation/countrylist.csv', 'rb') as f:		#List found here: http://www.andrewpatton.com/countrylist.csv
	reader = csv.reader(f)	
	for row in reader:
		if 'and' not in row[-1]:
			row[-1]= row[-1].split('.')
			if row[-1][-1] in d:
				country_tld[row[1]] = row[-1][-1]
		else:
			for each in row[-1].split(' and '):
				each = each.split('.')
				if each[-1] in d:
					country_tld[row[1]] = each[-1]
print "Result : "
print country_tld
