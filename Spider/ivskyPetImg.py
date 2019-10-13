import urllib.request as urllib2
import threading
from bs4 import BeautifulSoup
import time
import os


#spider for https://www.ivsky.com/tupian/ to get pet images
#@author zyyz
#@version 1.0.0
#@latest update：2019/10/9


imgs=[]
thrLock = threading.Lock()

headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection':'keep-alive',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
       }

#get image url
class Producer(threading.Thread):
    def __init__(self, num, url, encoding = "utf-8"):
        threading.Thread.__init__(self)
        self.num = num
        self.url = url
        self.encoding = encoding

    def GetHtml(self, url, encoding = "utf-8"):
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request)
        html = response.read()
        html = html.decode(encoding)
        return html
    
    def run(self):
        time.sleep(0.4)
        html = self.GetHtml(self.url, self.encoding)
        bs =  BeautifulSoup(html, 'html.parser')
        #get img url and add to imgs
        #True匹配给定属性为任意值的标签，None匹配那些给定的属性值为空的标签。
        img = bs.find_all("img", attrs={"alt" : True})
        #add lock
        thrLock.acquire()
        for i in img:
            #add image set name and image src
            imgs.append({"name":i["alt"], "src":"http:"+i["src"]})
        thrLock.release()
        global flags
        flags[self.num]=False



class DownImg(threading.Thread):
    #judge if is end
    #True is not end
    #using or operation
    def JudgeEnd(self):
        ans = False
        for flag in flags:
            ans = ans | flag
        return ans | (len(imgs) > 0)

    
    def run(self):
        while self.JudgeEnd() :
            if len(imgs) > 0:
                thrLock.acquire()
                i = imgs[0]
                path = i["name"]
                url = i["src"]
                del(imgs[0])
                thrLock.release()
                #getcwd means get the current directory path
                path = os.getcwd()+"/"+path
                if not os.path.exists(path):
                    os.makedirs(path)
                path = path + "/" +url[44:]
                #url :http://img.ivsky.com/img/tupian/t/201810/30/xiaonaimiao.jpg
                if os.path.exists(path):
                    print(" [-] Image {0} existing...".format(url[44:]))
                else:
                    #write to file
                    with open(path, "wb") as f:
                        response = urllib2.urlopen(urllib2.Request(url, headers = headers))
                        f.write(response.read())
                        print(" [+] Image {0} has been downloaded....".format(url[44:]))
                    

if __name__ == "__main__":
    print("-------------------Image Spider is Working------------------------")
    url = "https://www.ivsky.com/tupian/chongwu_t91/"

    num = 2#the page num to spider
    global flags
    flags=[]
    
    for index in range(0, num):
        flags.append(True)
        item_url = url + "index_{0}.html".format(index+1)
        print("Producer {0} is running...".format(index+1))
        p = Producer(index, item_url)
        p.start()

    downloader = DownImg()
    downloader.start()
    downloader.join()
    print("-------------------Image Spider Finished------------------------")

    
