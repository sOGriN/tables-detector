'''
Created on Oct 5, 2019

@author: grigorii
'''
from isp.tableDetector.FeatureExtractor import FeatureExtractor

import os
import sys
from isp.tableDetector.TableDetector import TableDetector

if __name__ == '__main__':
    print(os.path.abspath(os.path.curdir))
    fe = FeatureExtractor()
    rA, rB = fe.loadExamples('articles')
    detector = TableDetector()
    detector.train(rA, rB)
    features = fe.loadExample('__predict__.pdf')
    print(detector.__predict__(features))
    features = fe.loadExample('test2.pdf')
    print(detector.__predict__(features))