#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, urllib2
from .. import ilog, es
from ..data import Data
from hot import *

def startUpdate(isTest, configFileName):
	cycleUpdateHotList(Data(), configFileName, isTest)

def cycleUpdateHotList(data, configFileName, isTest):
	updateCount = 0
	while True:
		try:
			start = time.time()
			ilog.info('start:' + str(start) + '(' + time.strftime(es.esTimeFormatNoMs, time.localtime(start)) + ')')
			onceUpdateHotList(data, configFileName, isTest)
			cost = time.time() - start
			ilog.info('-------------------------cost: ' + str(cost) + '---------------------------------')
			if updateCount % 10 == 0:
				ilog.info('save data to es')
				updateCount = 0
				data.save()
				finalTime = data.getFinalTime()
				ilog.info('newest action time is: ' + str(finalTime) + '(' + es.timeToEsTime(finalTime) + ')')
			updateCount += 1
			if cost < 600:
				time.sleep(600 - cost)
		except Exception as error:
			ilog.info('Error: ' + str(error))

def onceUpdateHotList(data, configFileName, isTest):
	updateHotList(data, readConfig(configFileName))
	#10秒后通知后台更新
	time.sleep(10)
	noticeServer(isTest)
	saveHotTopList()

def updateHotList(data, config):
	start = time.time()
	data.update()
	subjectDict, worksDict = data.getSubWorksList(config['aid']['white'])
	ilog.info('add new actions finished:' + str(time.time() - start))

	updateWeight(config['weight'])
	
	dauFactor = data.getDauFactor()
	newShowMax = data.getNewShowMax()
	ilog.info('dauFactor:' + str(dauFactor) + ' newShowMax:' + str(newShowMax))
	worksHots = calHot(dauFactor, newShowMax, subjectDict, worksDict)
	ilog.info('got hot list:' + str(time.time() - start))

	ilog.info('update works hot: ' + ('success ' if es.coverStatisticsData('works_hot', worksHots) else 'fail ') + str(time.time() - start))

def readConfig(configFileName):
	with open(configFileName, 'r') as f:
		config = json.loads(f.read())
	ilog.info('config: ' + str(config))
	return config

def noticeServer(isTest):
	try:
		noticeUpdate(1, isTest)
		noticeUpdate(2, isTest)
	except urllib2.HTTPError as error:
		ilog.info('urllib2.HTTPError: ' + str(error))

def noticeUpdate(listType, isTest):
	url = 'http://nttest.iduoliao.cn:8080' if isTest else 'https://micro.mitao.iduoliao.cn'
	data = {
		"head":{
     		"@type":"type.googleapis.com/ja.common.proto.AutReqHead",
  			"ver": 1,
  			"platform": 999,
  			"seqid": long(time.time() * 1000)
    	},
    	"type": listType
	}
	headers = {'Content-Type': 'application/json'}
	request = urllib2.Request(url=url+'/recommend/IRecommend/UpdateDataNotice', headers=headers, data=json.dumps(data))
	infoInfo = urllib2.urlopen(request).read()
	ilog.info('notice ' + ('hot' if listType == 1 else 'new') + ' list update resp: ' + str(infoInfo))
	return json.loads(infoInfo)['head']['status'] == 1

def saveHotTopList():
	body = {"sort": [{"ranking": {"order": "asc"}}],"size": 50}
	now = time.strftime('%Y-%m-%dT%H:%M:%S+0800', time.localtime(time.time()))
	print(now)
	topList = {}
	for index, hit in enumerate(es.searchStatisticsDataByBody('works_hot', body, False)):
		info = hit['_source']
		info['time'] = now
		topList[hit['_id'] + '$' + str(now)] = info
	es.updateStatisticsData('works_hot_tops', topList)








