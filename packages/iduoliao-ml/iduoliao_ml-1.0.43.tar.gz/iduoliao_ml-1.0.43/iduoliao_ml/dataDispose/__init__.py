#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
from .. import es

def disposePersonas():
	worksDict = readWorks()
	while True:
		endTime = disposePersonasOnce(worksDict)
		print('endTime: ' + str(endTime) + '(' + es.timeToEsLocalTime(endTime) + ')')
		if endTime > time.time() - 3600:
			break

def disposePersonasOnce(worksDict):
	startTime = readEndTime()
	hits = es.searchPersonas(startTime)

	userActions = {}
	worksActions = {}

	aIndex = 0
	for index, hit in enumerate(hits):

		if index % 100 == 0:
			sys.stdout.write(str(index) + '\r')
			sys.stdout.flush()

		source = hit['_source']
		uid = source['uid']
		createTime = es.esTimeToTime(source['create_time']) if source.has_key('create_time') else 0
		actions = source['body'].split('\n')

		for action in actions:
			items = action.split('\t')
			if len(items) > 2 and items[2].isdigit():
				_id = str(startTime) + '$' + str(aIndex)
				_time = es.timeToEsLocalTime(float(items[0]))
				addUserAction(userActions, _id, createTime,items[2], _time, uid, items)
				addWorksAction(worksDict, worksActions, _id, createTime, items[2], _time, uid, items)
			aIndex += 1

		startTime = max(startTime, createTime)

	es.updateStatisticsData('user_actions', userActions)
	es.updateStatisticsData('works_actions', worksActions)
	writeEndTime(startTime)

	return startTime

def readEndTime():
	with open('endTime.ini', 'r') as f:
		return float(f.read())

def writeEndTime(endTime):
	with open('endTime.ini', 'w') as f:
		f.write(str(endTime))

def readWorks():
	worksDict = {}
	worksActions = {}
	for hit in es.scrollSearch('works_video_read', 'video', {"size":1000}):
		worksInfo = hit['_source']
		if worksInfo.has_key('vid') and worksInfo.has_key('aid') and worksInfo.has_key('publishtime'):
			vid = worksInfo['vid']
			worksDict[vid] = worksInfo
			worksActions[vid] = {'time': es.timeToEsLocalTime(es.esTimeToTime(worksInfo['publishtime'], True)), 'vid': vid, 'aid': worksInfo['aid'], 'duration': worksInfo['duration'], 'action': 4, 'uid': worksInfo['publisheruid'] if worksInfo.has_key('publisheruid') else 0, 'value': 1}
	es.updateStatisticsData('works_actions', worksActions)
	return worksDict

'''
2: 打开推荐页
3: 推荐页点击
4: 推荐曝光
'''

def addUserAction(userActions, _id, createTime, actionId, _time, uid, items):
	if actionId == '7' and items[1] == 'pages/common/index/index' and len(items) >= 5 and items[4] == '1':
		action = 2
		value = 1
	elif actionId == '7' and items[1] == 'pages/common/videoplay/videoplay' and items[3] == '1' and items[5] == '4':
		action = 3
		value = 1
	elif actionId == '9' and items[4] == '3':
		action = 4
		value = 1
	else:
		return
	userActions[_id] = {'createTime': createTime, 'time': _time, 'uid': uid, 'action': action, 'value': value}

'''
1: 播放时长
2: 留存播放
3: 推荐曝光
4: 发布
5: 推荐点击
'''
def addWorksAction(worksDict, worksActions, _id, createTime, actionId, _time, uid, items):
	if actionId == '6':
		vid = items[3]
		action = 1
		value = int(items[4])
	elif actionId == '9' and items[4] == '3':
		vid = items[3]
		action = 3
		value = 1
	elif actionId == '7' and items[1] == 'pages/common/videoplay/videoplay' and items[3] == '1' and items[5] == '4':
		vid = items[4]
		action = 5
		value = 1
	else:
		return
	if not worksDict.has_key(vid):
		return
	worksInfo = worksDict[vid]
	worksActions[_id] = {'createTime': createTime, 'time': _time, 'vid': vid, 'aid': worksInfo['aid'], 'duration': worksInfo['duration'], 'action': action, 'uid': uid, 'value': value}
	if actionId == '6' and (value >= 60 or value >= 0.9 * worksInfo['duration']):
		worksActions[_id + '$1'] = {'createTime': createTime, 'time': _time, 'vid': vid, 'aid': worksInfo['aid'], 'duration': worksInfo['duration'], 'action': 2, 'uid': uid, 'value': 1}





