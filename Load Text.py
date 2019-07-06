# coding: utf-8

# In[19]:


import os
import re
import csv
from datetime import datetime
import pdb


# In[2]:


def process(text):
    date=re.findall("(\d+\/\d+\/\d+)", text)[0]
    consumption=re.finditer("(\d+,\d+\n){24}", text, flags=re.M)
    items = []
    for i in consumption:
        these_matches = i[0].split("\n")
        mapped = list(map(lambda x: x.replace(",", ""), these_matches))
        print(mapped)
        items.append(mapped)
        print(i)
    return date, items[0], items[1]


# In[17]:


def create_csv(date, consumption, prediction):
    if len(consumption)!=len(prediction):
        raise Exception ("Unmathced")
    data=[]
    for i in range(24):
        datenew=date.split("/")
        print(datenew)
        thisdate=datetime(int(datenew[2]), int(datenew[1]), int(datenew[0]), i)
        this_data = [thisdate, consumption[i], prediction[i]]
        data.append(this_data)
        
    return data


# In[24]:


csv_file=open("Table.csv", "w")
writer = csv.writer(csv_file)
PATH="C:\\Users\\robin\\Documents\\shu-hack\\txtOutput"
for file in os.scandir(PATH):
    if file.name.endswith(".txt"):
        print(file)
        with open (file) as f:
            f_content=f.read()
            date, consumption, prediction=process(f_content)
            csv_data = create_csv(date, consumption, prediction)
            writer.writerows(csv_data)
             

csv_file.close()                
