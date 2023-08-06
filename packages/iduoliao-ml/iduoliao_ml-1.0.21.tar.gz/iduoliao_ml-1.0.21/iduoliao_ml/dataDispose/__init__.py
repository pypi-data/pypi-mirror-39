#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
from .. import es

def disposePersonas():
	startTime = readEndTime()
	hits = es.searchPersonas(startTime)

	userActionWorks = {}

	aIndex = 0
	for index, hit in enumerate(hits):

		if index % 100 == 0:
			sys.stdout.write(str(index) + '\r')
			sys.stdout.flush()

		source = hit['_source']
		uid = source['uid']
		actions = source['body'].split('\n')

		for action in actions:
			items = action.split('\t')
			if len(items) > 2 and items[2].isdigit():
				_id = str(startTime) + '$' + str(aIndex)
				addUserActionWorks(userActionWorks, _id, uid, items)
			aIndex += 1

		if source.has_key('create_time'):
			startTime = max(startTime, es.esTimeToTime(source['create_time']))

	if es.updateStatisticsData('user_action_works', userActionWorks):
		writeEndTime(startTime)

def readEndTime():
	with open('endTime.ini', 'r') as f:
		return float(f.read())

def writeEndTime(endTime):
	with open('endTime.ini', 'w') as f:
		f.write(str(endTime))

def addUserActionWorks(userActionWorks, _id, uid, items):
	 actionId = items[2]
	 info = {'time': time.strftime('%Y-%m-%dT%H:%M:%S+0800', time.localtime(float(items[0]))), 'uid': uid}
	 if actionId == '1':
	 	info['vid'] = items[3]
	 	info['action'] = '播放'
	 elif actionId == '2':
	 	info['']
	 else:
	 	return
	 userActionWorks[_id] = info




