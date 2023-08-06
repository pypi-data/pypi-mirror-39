#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
from .. import es

def disposePersonas():
	startTime = readEndTime()
	hits = es.searchPersonas(startTime)

	userActions = {}
	worksActions = {}

	worksDict = readWorks()
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
				_time = time.strftime('%Y-%m-%dT%H:%M:%S+0800', time.localtime(float(items[0])))
				addUserAction(userActions, _id, items[2], _time, uid, items)
				addWorksAction(worksDict, worksActions, _id, items[2], _time, uid, items)
			aIndex += 1

		if source.has_key('create_time'):
			startTime = max(startTime, es.esTimeToTime(source['create_time']))

	es.updateStatisticsData('user_actions', userActions)
	es.updateStatisticsData('works_actions', worksActions)
	writeEndTime(startTime)

def readEndTime():
	with open('endTime.ini', 'r') as f:
		return float(f.read())

def writeEndTime(endTime):
	with open('endTime.ini', 'w') as f:
		f.write(str(endTime))

def readWorks():
	worksDict = {}
	for hit in es.scrollSearch('works_video_read', 'video', {"size":1000}):
		worksInfo = hit['_source']
		if worksInfo.has_key('vid') and worksInfo.has_key('aid'):
			worksDict[worksInfo['vid']] = worksInfo
	return worksDict

'''
2: 打开推荐页
3: 推荐页点击
4: 推荐曝光
'''

def addUserAction(userActions, _id, actionId, _time, uid, items):
	if actionId == '7' and items[1] == 'pages/common/index/index':
		action = 2
		value = 1
	elif actionId == '7' and items[1] == 'pages/common/videoplay/videopaly' and items[3] == '1' and item[5] == '4':
		action = 3
		value = 1
	elif actionId == '9' and items[4] == '3':
		action = 4
		value = 1
	else:
		return
	userActions[_id] = {'time': _time, 'uid': uid, 'action': action, 'value': value}

'''
1: 播放时长
'''
def addWorksAction(worksDict, worksActions, _id, actionId, _time, uid, items):
	if actionId == '6':
		vid = items[3]
		action = 1
		value = int(items[4])
	else:
		return
	if not worksDict.has_key(vid):
		return
	worksInfo = worksDict[vid]
	worksActions[_id] = {'time': _time, 'vid': vid, 'aid': worksInfo['aid'], 'duration': worksInfo['duration'], 'action': action, 'uid': uid, 'value': value}





