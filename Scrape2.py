import requests
import time

for i in range(349, 1230):
    if i<1000:
        index="0"+str(i)
    else:
        index=str(i)
    for j in range(1, 100):
        if j<10:
            req=requests.get("http://download.terna.it/terna/0000/"+index+"/0"+str(j)+".pdf", stream=True)
        else:
            req=requests.get("http://download.terna.it/terna/0000/"+index+"/"+str(j)+".pdf", stream=True)
            
        if req.status_code != 200:
            print("Request failed "+ str(req.reason))
        else:
            req_content=req.content
        with open("file"+str(i)+"_"+str(j)+".pdf", "wb") as f:
            f.write(req_content)
        time.sleep(1)
        print("Done")
