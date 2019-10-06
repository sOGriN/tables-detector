'''
Created on Oct 6, 2019

@author: grigorii
'''

import arxiv
#import PyPDF2
import os, sys, subprocess
import PyPDF2
class ArxivInitializer(object):
    '''
    classdocs
    '''
    def __open_file__(self, filename):
        if sys.platform == "win32":
            pass#os.startfile(filename)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
    def loadArticles(self, inpString, directory, count=10):
        newDirFl = True
        try:
            os.mkdir(directory)
        except FileExistsError:
            newDirFl = False
        articles = arxiv.query(query=inpString, max_results=count * 2);
        indexFile = open(os.path.join(directory, "index.txt"), 'a')
        for article in articles:
            try:
                filename = arxiv.download(article, dirpath=directory);
                try:
                    pdf = PyPDF2.PdfFileReader(filename)               
                    count-=1
                    indexFile.write(os.path.basename(article.id) + ' ' +os.path.basename(filename) + ' 0\n')
                except Exception:
                    os.remove(filename)
            except FileExistsError:
                pass
            if count == 0:
                break
        indexFile.close()
    def markArticles(self, directory):
        if not os.path.exists(os.path.join(directory, "index.txt")):
            print(os.path.join(directory, "index.txt")+": not exists")
            return
        indexFile = open(os.path.join(directory, "index.txt"), 'r+')
        while True:
            currentLine = indexFile.readline();
            if currentLine == '':
                break
            print(currentLine)
            fid, currentFile, currentTableFl = str.split(currentLine);
            if currentTableFl != '0':
                continue
            self.__open_file__(os.path.join(directory, currentFile))
            answer = input(currentFile + ':')
            existTableFl = '0';
            if answer == 'y':
                existTableFl = 'y'
            if answer == 'n':
                existTableFl = 'n'
            if answer == 'e':
                existTableFl = 'e'
            print(indexFile.tell())
            indexFile.seek(indexFile.tell() - 2)
            indexFile.write(existTableFl)
            indexFile.flush()
            indexFile.readline();
        indexFile.close();
        print('END')
    def __init__(self):
        '''
        Constructor
        '''
        