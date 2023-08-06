#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hot, es

def startUpdateHot(isTest):
	es.setEnv(isTest)
	hot.startUpdate(isTest, 'config.ini')
