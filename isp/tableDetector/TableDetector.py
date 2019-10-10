'''
Created on Oct 5, 2019

@author: grigorii
'''
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from isp.tableDetector.FeatureExtractor import FeatureExtractor
class TableDetector(object):
    '''
    classdocs
    '''    
    def trainFrom(self, dirPath):
        self.fe = FeatureExtractor()
        print('Load data ...')
        rA, rB = self.fe.loadExamples(dirPath, True)
        print(str(len(rB)) + ' examples')
        rA, tA, rB, tB = train_test_split(rA,rB,test_size=0.4,random_state=0)
        self.train(rA, rB)
        print('Score: ' + str(self.main.score(tA, tB)))     
        
    def predictFile(self, filePath):
        return self.__predict__(self.fe.loadExample(filePath))
        
    def train(self, features, answers):
        print("Train ...")
        self.main.fit(features, answers)
        
    def __predict__(self, features):
        return self.main.predict([features])

    def __init__(self):
        self.main = LogisticRegression(solver='lbfgs',max_iter=200)
        self.fe = None
        
    def __del__(self):
        pass
        