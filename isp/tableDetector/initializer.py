import arxiv
#import PyPDF2
import os, sys, subprocess
def open_file(filename):
    if sys.platform == "win32":
        pass#os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
def loadArticles(inpString, directory, count=10):
    newDirFl = True
    try:
        os.mkdir(directory)
    except FileExistsError:
        newDirFl = False
    articles = arxiv.query(query=inpString, max_results=count);
    indexFile = open(os.path.join(directory, "index.txt"), 'a')
    for article in articles:
        try:
            filename = arxiv.download(article, dirpath=directory);
            #try:
            #    pdfFile = open(filename, 'rb')
            #    pdf = PyPDF2.PdfFileReader(pdfFile)
            #except
            indexFile.write(os.path.basename(article.id) + ' ' +os.path.basename(filename) + ' 0\n')
        except FileExistsError:
            pass
    indexFile.close()
def markArticles(directory):
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
        open_file(os.path.join(directory, currentFile))
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
    
