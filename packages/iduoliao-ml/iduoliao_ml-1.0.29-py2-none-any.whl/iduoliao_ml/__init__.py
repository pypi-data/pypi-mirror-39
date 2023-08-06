#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hot, es, dataDispose

def startUpdateHot(isTest):
	es.setEnv(isTest)
	hot.startUpdate(isTest, 'config.ini')

def disposeData(isTest):
	es.setEnv(isTest)
	dataDispose.disposePersonas()
