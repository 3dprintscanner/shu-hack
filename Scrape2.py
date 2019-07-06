import requests
import time

with open("output.txt") as f:
    links = f.readlines()
    numLinks = len(links)
    start = 0

for k,link in enumerate(links[start::]):
    link = link.lower()[0:-1]
    print(link)
    i,j = (link.split('/')[5], link.split('/')[6])
    
    print(repr(link))

    req = requests.get(link, stream=True)

    if req.status_code != 200:
        print("Request failed "+ str(req.reason))
    else:
        req_content=req.content
        with open("pdfOuput\\file"+i+"_"+j, "wb") as f:
            f.write(req_content)
        time.sleep(1)
        print("Done - {}/{}".format(start+k,numLinks))
