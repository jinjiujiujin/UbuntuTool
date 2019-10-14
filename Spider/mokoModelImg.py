#----------------------------------------------------------------------------------
#spider working on getting model pictures on moko website
#author zyyz
#version 1.1.0
#latest update 2019/10/13
#----------------------------------------------------------------------------------
from GetHtml import GetHtml_2 as GetHtml
import re
import pymongo as pm
import threading

class Producer(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def Write2database(self, id, level, certificated, homePage, portrait, nikename, address, follow):
        post = {"id":id, "level":level, "certificated": certificated, "homePage":homePage, "portrait":portrait, "nikename":nikename, "address":address, "follow":follow}
        db.users.insert_one(post)#collection name

    def run(self):
        # Collect Users
        html = GetHtml(self.url)
        #get id level certificated mainpage portrait nikename address follows
        users = re.findall(r'divEditOperate_(\d*?)\".*?<span class=\"mainColor weight700\">.*?>(.*?)</span></span>(<br/>)?.*?href=(.*?) hidefocus.*?src=\"(.*?)\".*?alt=(.*?) title=.*?<p class="font12 lesserColor">(.*?)&nbsp;&nbsp;&nbsp;&nbsp;粉丝&nbsp;&gt;<span class="font12 mainColor">(\d*?)</span', html, re.S)
        #write to database
        for user in users:
            if user[2] == "":
                self.Write2database(user[0], user[1], "False", "http://www.moko.cc" + user[3], user[4], user[5], user[6], user[7])
            else:
                self.Write2database(user[0], user[1], "True", "http://www.moko.cc" + user[3], user[4], user[5], user[6], user[7])

    

def GetUserPages(url):
    html = GetHtml(url)
    pageNums = re.findall(r'onfocus=\"this\.blur\(\)\">(\d*?)<', html, re.S)
    pageNum = max(pageNums)
    return int(pageNum)   

if __name__ == "__main__":
    print("----------------------Spider is running--------------------------------")
    ##########database register
    #########after power on, you must enter root and input sudo  service mongod start
    #########otherwise you couldn't use mongo
    user = "Spider"
    pwd = "zyydbabareallynb"
    client = pm.MongoClient("localhost", 27017)
    global db
    db = client.mokoUsers#dabaseName
    db.authenticate(user, pwd)

    url = "http://www.moko.cc/subscribe/chenhaoalex/1.html"
    pageNum = GetUserPages(url)
    #for i in range(1, pageNum+1):
    for i in range(1, 5):
        page_url = "http://www.moko.cc/subscribe/chenhaoalex/{0}.html".format(i)
        p = Producer(page_url)
        p.start()
        print(" [+] Producer{0} is running...")
    
    print("----------------------Spider Finished--------------------------------")
