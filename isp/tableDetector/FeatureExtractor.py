'''
Created on Oct 5, 2019

@author: grigorii
'''
import PyPDF2
from PyPDF2.pdf import PageObject
import os
from PyPDF2.generic import IndirectObject, ArrayObject
from _operator import index
class FeatureExtractor(object):
    '''
    classdocs
    '''
    def __freeIndex__(self):
        if self.indexFile != None:
            self.indexFile.close()        
    
    def __loadIndex__(self, dirPath):
        if self.indexFile != None:
            self.indexFile.close()
        self.indexFile = open(os.path.join(dirPath, 'index.txt'), 'r')
        
    def initialize(self, dirPath):
        self.__loadIndex__(dirPath)
        while True:
            currentLine = self.indexFile.readline();
            if currentLine == '':
                break
            fid, currentFile, currentTableFl = str.split(currentLine);
            self.__initBag__(os.path.join(dirPath, currentFile))
        self.__completeBag__()        
        self.__freeIndex__()
    def loadExamples(self, dirPath):
        resultA = []
        resultB = []        
        self.__loadIndex__(dirPath)
        while True:
            currentLine = self.indexFile.readline();
            if currentLine == '':
                break
            fid, currentFile, currentTableFl = str.split(currentLine);
            resultA.append(self.loadExample(os.path.join(dirPath, currentFile)))
            resultB.append(currentTableFl)            
        self.__freeIndex__()
        return resultA, resultB
    def __parseItem__(self, item):
        if (type(item) == ArrayObject):
            for current in item:
                self.__parseItem__(current)
        else:
            if (type(item) == IndirectObject):
                self.__parseItem__(item.getObject())
            else:
                buffer = item.getData()
                for index in range(0, len(buffer) - 1):
                    self.symbols.add(buffer[index] * 256 + buffer[index+1])
    def __calcItem__(self, item, vector):
        if (type(item) == ArrayObject):
            for current in item:
                self.__calcItem__(current, vector)
        else:
            if (type(item) == IndirectObject):
                self.__calcItem__(item.getObject(), vector)
            else:
                buffer = item.getData()
                for index in range(0, len(buffer) - 1):
                    if (self.transform.get(buffer[index] * 256 + buffer[index+1]) != None):
                        vector[self.transform.get(buffer[index] * 256 + buffer[index+1])]+= 1
    def __initBag__(self, pdfFile):
        pdf = PyPDF2.PdfFileReader(pdfFile)
        for pageNum in range(0, pdf.getNumPages()):
            page = pdf.getPage(pageNum)
            self.__parseItem__(page.getContents()) 
    def __completeBag__(self):
        index = 0
        for item in self.symbols:
            self.transform[item] = index
            index+=1
        #print(self.transform)
        print(index)
    def loadExample(self, pdfFile):
        currentVector = [0 for x in range(0, len(self.symbols))]
        pdf = PyPDF2.PdfFileReader(pdfFile)
        for pageNum in range(0, pdf.getNumPages()):
            page = pdf.getPage(pageNum)
            self.__calcItem__(page.getContents(), currentVector) 
        return currentVector
    def __init__(self):
        self.symbols = set()
        self.indexFile = None
        self.transform = dict()
        '''
        Constructor
        '''
        