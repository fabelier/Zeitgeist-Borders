#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# "get_google_domains.py"
# By Antoine Mazières -- http://ant1.cc/
# "AS IS" under CC_BY_SA
#

import os, sys, string, urllib, csv

## tweak a textmate bug
reload(sys) 
sys.setdefaultencoding("utf-8")
##

d = urllib.urlopen('http://www.google.com/supported_domains').read().replace('\n', '').split('.google')[1:]

country_tld = {}

with open ('../documentation/countrylist.csv', 'rb') as f:		#List found here: http://www.andrewpatton.com/countrylist.csv
	reader = csv.reader(f)
	for row in reader:
		if 'and' not in row[-1]:
			if row[-1] in d:
				country_tld[row[1]] = row[-1]
		else:
			for each in row[-1].split(' and '):
				if each in d:
					country_tld[row[1]] = each

print country_tld
