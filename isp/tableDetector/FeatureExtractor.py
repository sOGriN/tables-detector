'''
Created on Oct 5, 2019

@author: grigorii
'''
import PyPDF2
import os
from PyPDF2.generic import IndirectObject, ArrayObject
from _operator import index
import numpy
from sklearn import preprocessing
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
    def loadExamplesFromPdf(self, dirPath, trainFl):
        resultA = []
        resultB = []   
        self.__loadIndex__(dirPath)
        while True:
            currentLine = self.indexFile.readline();
            if currentLine == '':
                break
            fid, currentFile, currentTableFl = str.split(currentLine);
            resultA.append(self.__loadExample__(os.path.join(dirPath, currentFile), trainFl))
            resultB.append(currentTableFl)            
        self.__freeIndex__()
        if trainFl:
            for lst in resultA:
                for n in range(len(lst), self.symbolCount):
                    lst.append(0)
        return resultA, resultB
    def loadExamples(self, dirPath, trainFl=False):
        resultA, resultB, symbols = None, None, None
        if trainFl:
            self.scaler = preprocessing.StandardScaler()
            if not os.path.exists(os.path.join(dirPath, 'resultA.npy')):
                resultA, resultB = self.loadExamplesFromPdf(dirPath, trainFl)
                resultA = numpy.array(resultA)
                resultB = numpy.array(resultB)
                numpy.save(os.path.join(dirPath, 'resultA'), resultA)
                numpy.save(os.path.join(dirPath, 'resultB'), resultB)
                symbols =  [0 for x in range(0, self.symbolCount)]
                for s in self.transform.keys():
                    symbols[self.transform.get(s)] = s;
                numpy.save(os.path.join(dirPath, 'symbols.npy'), numpy.array(symbols))
            else:
                resultA = numpy.load(os.path.join(dirPath, 'resultA.npy'))
                resultB = numpy.load(os.path.join(dirPath, 'resultB.npy'))
                symbols = numpy.load(os.path.join(dirPath, 'symbols.npy'))
                self.symbolCount = len(symbols)
                for index, s in enumerate(symbols):
                    self.transform[s] = index
        else:            
            resultA, resultB = self.loadExamplesFromPdf(dirPath, trainFl)
            resultA = numpy.array(resultA)
            resultB = numpy.array(resultB)
        return self.scaler.fit_transform(resultA), resultB
    def translate(self, buffer, index):
        return buffer[index] * 256 + buffer[index+1]
    def __calcItem__(self, item, vector, trainFl):
        if (type(item) == ArrayObject):
            for current in item:
                self.__calcItem__(current, vector, trainFl)
        else:
            if (type(item) == IndirectObject):
                self.__calcItem__(item.getObject(), vector, trainFl)
            else:
                buffer = item.getData()
                for index in range(0, len(buffer) - 1):
                    if (self.transform.get(self.translate(buffer, index)) == None):
                        if (trainFl):
                            self.__addSymbol__(self.translate(buffer, index))
                            vector.append(0)
                            vector[self.transform.get(self.translate(buffer, index))]+= 1
                    else:
                        vector[self.transform.get(self.translate(buffer, index))]+= 1
    def __addSymbol__(self, symbol):
        self.transform[symbol] = self.symbolCount
        self.symbolCount += 1
    def __loadExample__(self, pdfFile, trainFl=False):
        currentVector = [0 for x in range(0, self.symbolCount)]
        pdf = PyPDF2.PdfFileReader(pdfFile)
        for pageNum in range(0, pdf.getNumPages()):
            page = pdf.getPage(pageNum)
            self.__calcItem__(page.getContents(), currentVector, trainFl) 
        return currentVector
    def loadExample(self, pdfFile):
        return self.scaler.transform([self.__loadExample__(pdfFile)])[0]
    def __init__(self):
        self.symbolCount = 0
        self.indexFile = None
        self.transform = dict()
        self.scaler = None 
        '''
        Constructor
        '''
        