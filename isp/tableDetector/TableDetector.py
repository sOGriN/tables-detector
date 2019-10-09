'''
Created on Oct 5, 2019

@author: grigorii
'''
from sklearn.linear_model import LogisticRegression
from isp.tableDetector.FeatureExtractor import FeatureExtractor
class TableDetector(object):
    '''
    classdocs
    '''    
    def trainFrom(self, dirPath):
        self.fe = FeatureExtractor()
        #self.fe.initialize(dirPath)
        rA, rB = self.fe.loadExamples(dirPath, True)
        self.train(rA, rB)
        
    def predictFile(self, filePath):
        return self.__predict__(self.fe.loadExample(filePath))
        
    def train(self, features, answers):
        self.main.fit(features, answers)
        print(self.main.score(features, answers))
        
    def checkDirectory(self, dirPath):
        rA, rB = self.fe.loadExamples(dirPath)
        correct = 0
        for index, itemA in enumerate(rA):
            if self.__predict__(itemA)[0] == rB[index]:
                correct+=1
        return 1.00 * correct / len(rB)
        
    def __predict__(self, features):
        return self.main.predict([features])

    def __init__(self):
        self.main = LogisticRegression(solver='lbfgs', max_iter=200)
        self.fe = None
        '''
        Constructor
        '''
    def __del__(self):
        pass
        