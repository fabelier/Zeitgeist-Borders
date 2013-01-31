#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

f = open('2013-01-29-zeigeist.cache_alphabetonly.json', 'r')
d = {}
stats1 = {}
stats2 = {}
nb_tld = 186

for line in f.readlines():
	d = {}
	j = json.loads(line, encoding='utf-8')
	# print j
	# print type(j)
	letter =  j['_id']
	d[letter] = {}
	# print len(j['value'].keys())
	for each in j[u'value']:
		try:
			first_suggestion = j['value'][each][0].encode('utf-8')
		except:
			break
		# print each, first_suggestion
		try:
			d[letter][first_suggestion] += 1
		except:
			d[letter][first_suggestion] = 1
	print d
	stats1[letter] = float(sorted(d[letter].values(), reverse=True)[0]) / float(nb_tld)
	stats2[letter] = len(d[letter].keys()) - 1
	# stats2[letter] = 

	# maxi = sorted(d[letter].values(), reverse=True)[0]
	# print d[letter]
	# print len(d[letter].keys())
	# for each in d[letter]:
	# 	if d[letter][each] == maxi:
	# 		print each
	# for k, v in d[letter]:
	# 	if v == sorted(d[letter].values(), reverse=True)[0]:
	# 		print k, v
	print stats1[letter]
	print stats2[letter]
	# break


result1 = sum(stats1.values())/len(stats1.values())
result2 = sum(stats2.values())/len(stats2.values())
print "In average, , approximatively %s%% of TLDs (%s over %s), are served with the exact same first suggestion for each letter" % ( int(result1*100), int(result1*nb_tld), nb_tld )
# print "The other %s TLDs are served with an average of %s different first suggestions." % ( int((1-result1)*nb_tld), result2 )
print "This means that an average of %s different first suggestions are disrtributed over the other %s TLDs. This represents an approximate ratio of first suggestion uniqueness equal to %s for 70%% of TLDs " % ( result2, int((1-result1)*nb_tld), round(float(result2)/float((1-result1)*nb_tld),2)  )
# print "This means that, in average, approximatively %s diffrent first suggestions are served over %s%% of TLDs" % ( int((1-result1)*100),  )





