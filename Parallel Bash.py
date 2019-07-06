import os
from multiprocessing.dummy import Pool as ThreadPool
PATH="/home/aleksei/Рабочий стол/pdfOutput/"

filenames=[]
for file in os.scandir(PATH):
    if file.name.endswith(".pdf"):
        filenames.append(file.name)

def pdftotext(file):
    os.system('''FILE='''+file+'''\n pdf2txt.py $FILE > $FILE.txt ''')

pool=ThreadPool(7)
pool.map(pdftotext, filenames)
pool.close()
pool.join()
