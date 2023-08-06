#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
from elasticsearch import Elasticsearch

esTimeFormat = u"%Y-%m-%dT%H:%M:%S.%fZ"
esTimeFormatNoMs = u"%Y-%m-%dT%H:%M:%SZ"

testEsclient = Elasticsearch(['119.23.69.206:9200'])
devEsclient = Elasticsearch(['192.168.0.100:9200'])
dataEsclient = Elasticsearch(['10.168.0.119:9200', '10.168.0.121:9200', '10.168.0.118:9200'], http_auth=('huangzhen', 'df25j0934j4y09hjoijoigef'))
relEsclient = Elasticsearch(['10.32.0.223:9200', '10.33.0.11:9200', '10.167.0.246:9200', '10.0.0.53:9200'], http_auth=('huangzhen', 'huangzhen'))


isTest = True

def setEnv(test):
	global isTest
	isTest = test

def updateStatisticsAlias(index, isRead):
	indices = getEsclient().indices
	alias = 'statistics_' + index + '_' + ('read' if isRead else 'write')
	cIndex = indices.get_alias(index=alias).keys()[0]
	newIndex = cIndex[:len(cIndex)-8] if cIndex.endswith('_backups') else cIndex + '_backups'
	body = {
		"actions": [
			{"remove": {"index": cIndex, "alias": alias}},
			{"add": {"index": newIndex, "alias": alias}}
		]
	}
	indices.update_aliases(body=body)

def coverStatisticsData(index, dataDict):
	#先将读别名指向备份，再写入主索引，再将读别名指回
	updateStatisticsAlias(index, True)
	success = coverStatisticsDataReal(index, dataDict)
	#
	time.sleep(12)
	updateStatisticsAlias(index, True)
	if not success:
		return False

	#将写别名指向备份，再写入备份，再将写别名指回
	updateStatisticsAlias(index, False)
	success = coverStatisticsDataReal(index, dataDict)
	updateStatisticsAlias(index, False)
	return success

def coverStatisticsDataReal(index, dataDict):
	hits = searchStatisticsData(index, 1, False)
	updateMark = len(hits) == 0 or not hits[0]['_source']['updateMark']
	for item in dataDict.values():
		item['updateMark'] = updateMark
	if updateStatisticsData(index, dataDict):
		#操作频繁会发生冲突
		time.sleep(11)
		return deleteStatisticsData(index, {"query":{"term":{"updateMark":not updateMark}}})
	else:
		return False

def clearStatisticsData(index):
	deleteStatisticsData(index, {"query":{"match_all":{}}})

def deleteStatisticsData(index, body):
	return len(getEsclient().delete_by_query(index='statistics_' + index + '_write', doc_type='data', body=body)['failures']) == 0

def updateStatisticsData(index, dataDict):
	doc = []
	for key, value in dataDict.items():
		doc.append({"index":{"_id":key}})
		doc.append(value)
	return updateStatisticsDoc(index, doc)

def updateStatisticsDoc(index, doc):
	print('update', index, len(doc) / 2)
	start = 0
	while start < len(doc):
		end = min(start + 2500, len(doc))
		success = updateStatisticsDocResolve(index, doc[start:end])
		if success:
			start = end
	return True

def updateStatisticsDocResolve(index, doc):
	#正式环境的hot list额外在开发环境存一份用于测试
	#if not isTest and index == 'works_hot':
	#	esUpdateStatisticsDocResolve(devEsclient, index, doc)
	return esUpdateStatisticsDocResolve(getEsclient(), index, doc)

def esUpdateStatisticsDocResolve(es, index, doc):
	return not es.bulk(index='statistics_' + index + '_write', doc_type='data', body=doc)['errors']

def searchPersonas(lastPersonasTime):
	body = {
	  "query":{
	    "bool": {
	      "must": [
	        {
	          "term": {
	            "type": "personas"
	          }
	        },
	        {
	          "range": {
	            "create_time": {
	              "gt": timeToEsTime(lastPersonasTime)
	            }
	          }
	        }
	      ]
	    }
	  },
  		"size": 10000
	}
	return scrollSearch('clientlog_read', 'watch', body)

def searchStatisticsData(index, size=10000, searchAll=True):
	return searchStatisticsDataByBody(index, {"size": size}, searchAll)

def searchStatisticsDataByBody(index, body, searchAll=True):
	return scrollSearch('statistics_' + index + '_read', 'data', body, searchAll)

def scrollSearch(index, doc_type, body, searchAll=True):
	esclient = getEsclient(index)
	hits = []
	if searchAll:
		result = esclient.search(index=index, doc_type=doc_type, scroll='1m', body=body)
		while len(result['hits']['hits']) != 0:
			hits.extend(result['hits']['hits'])
			scroll_id = result['_scroll_id']
			result = esclient.scroll(scroll_id=scroll_id, scroll='1m')
	else:
		hits.extend(esclient.search(index=index, doc_type=doc_type, body=body)['hits']['hits'])
	print('get', index, len(hits))
	return hits

def getEsclient(index=None):
	return testEsclient if isTest else relEsclient if index == 'works_video_read' else dataEsclient

def timeToEsTime(pTime, hasMs=False):
	return time.strftime(esTimeFormat if hasMs else esTimeFormatNoMs, time.gmtime(pTime))

def esTimeToTime(esTime, hasMs=False):
	return time.mktime(time.strptime(esTime, esTimeFormat if hasMs else esTimeFormatNoMs)) + 28800


