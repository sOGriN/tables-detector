'''
Created on Oct 6, 2019

@author: grigorii
'''
from isp.tableDetector.TableDetector import TableDetector
from isp.tableDetector import TableDetectorServer

if __name__ == '__main__':
    #td = TableDetector()
    #td.trainFrom('repository2')
    #print(td.checkDirectory('articles'))
    serv = TableDetectorServer.TableDetectorServer()
    serv.startHTTPServer(65500, 'repository2', 'articles')