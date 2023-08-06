#! /usr/bin/env python
# -*- coding: utf-8 -*-

def disposePersonas():
	startTime = 0
	with open('endTime.ini', 'r') as f:
		startTime = float(f.read())
	hits = es.searchPersonas(startTime)
	userActionWorks = {}
	for hit in hits:
		