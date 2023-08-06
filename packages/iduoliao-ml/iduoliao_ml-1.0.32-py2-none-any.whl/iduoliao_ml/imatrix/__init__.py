#! /usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *

def inOne(mats):
	col = mats.shape[0]
	matAvg = mats.mean(axis=0)
	matDiff = mats - matAvg
	matDiffSumAvg = square(matDiff).mean(axis=0)
	vari = sqrt(matDiffSumAvg)
	z = matDiff / vari
	zNoNaN = mat(where(isnan(z), mat(zeros((col, mats.shape[1]))), z))
	return sigmoid(zNoNaN)

def sigmoid(mats):
	return 1 / (1 + exp(-mats))