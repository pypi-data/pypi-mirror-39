#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
from .. import es

def disposePersonas():
	startTime = readEndTime()
	hits = es.searchPersonas(startTime)

	userActions = {}

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
				addUserAction(userActions, _id, uid, items)
			aIndex += 1

		if source.has_key('create_time'):
			startTime = max(startTime, es.esTimeToTime(source['create_time']))

	es.updateStatisticsData('user_actions', userActions)
	writeEndTime(startTime)

def readEndTime():
	with open('endTime.ini', 'r') as f:
		return float(f.read())

def writeEndTime(endTime):
	with open('endTime.ini', 'w') as f:
		f.write(str(endTime))

'''
1: 播放
2: 打开推荐页
3: 推荐页点击
4: 推荐曝光
5: 播放时长
'''

def addUserAction(userActions, _id, uid, items):
	 actionId = items[2]
	 if actionId == '1':
	 	action = 1
	 	value = 1
	 elif actionId == '7' and items[1] == 'pages/common/index/index':
	 	action = 2
	 	value = 1
	 elif actionId == '7' and items[1] == 'pages/common/videoplay/videopaly' and items[3] == '1' and item[5] == '4':
	 	action = 3
	 	value = 1
	 elif actionId == '9' and items[4] == '3':
	 	action = 4
	 	value = 1
	 elif actionId == '6':
	 	action = 5
	 	value = int(items[4])
	 else:
	 	return
	 userActions[_id] = {'time': time.strftime('%Y-%m-%dT%H:%M:%S+0800', time.localtime(float(items[0]))), 'uid': uid, 'action': action, 'value': value}

'''
1: 大于60s作品播放
2: 大于60s作品播放时长大于60
3: 小于60s作品播放
4: 小于60s作品播放达90%
'''




