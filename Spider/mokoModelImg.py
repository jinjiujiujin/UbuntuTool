#----------------------------------------------------------------------------------
#spider working on getting model pictures on moko website
#author zyyz
#version 1.0.0
#latest update 2019/10/13
#----------------------------------------------------------------------------------
from GetHtml import GetHtml_2 as GetHtml
import re
import pymongo as pm


def GetUserPages(url):
    html = GetHtml(url)
    pageNums = re.findall(r'onfocus=\"this\.blur\(\)\">(\d*?)<', html, re.S)
    pageNum = max(pageNums)
    return int(pageNum)    

def GetUsers(url, users):
    html = GetHtml(url)
    #get id level certificated mainpage portrait nikename address follows
    users = re.findall(r'divEditOperate_(\d*?)\".*?<span class=\"mainColor weight700\">.*?>(.*?)</span></span>(<br/>)?.*?href=(.*?) hidefocus.*?src=\"(.*?)\".*?alt=(.*?) title=.*?<p class="font12 lesserColor">(.*?)&nbsp;&nbsp;&nbsp;&nbsp;粉丝&nbsp;&gt;<span class="font12 mainColor">(\d*?)</span', html, re.S)
    #write to database
    for user in users:
    	Write2database(user[0], user[1], user[2], "http://www.moko.cc" + user[3], user[4], user[5], user[6], user[7])



def Write2database(id, level, certificated, homePage, portrait, nikename, address, follow):
	##########database information
    user = "Spider"
    pwd = "zyydbabareallynb"
    ##########database information
    client=pm.MongoClient("localhost", 27017)
    db = client.mokoUsers#dabaseName
    db.authenticate(user, pwd)
    post = {"id":id, "level":level, "certificated": certificated, "homePage":homePage, "portrait":portrait, "nikename":nikename, "address":address, "follow":follow}
    db.users.insert_one(post)#collection name



if __name__ == "__main__":
    print("----------------------Spider is running--------------------------------")
    
    url = "http://www.moko.cc/subscribe/chenhaoalex/1.html"
    #get all pages
    pageNum = GetUserPages(url)
    users = []
    #for i in range(1, pageNum+1):
    for i in range(1, 2):
        page_url = "http://www.moko.cc/subscribe/chenhaoalex/{0}.html".format(i)
        GetUsers(page_url, users)
    #save to database
    
    print("----------------------Spider Finished--------------------------------")
