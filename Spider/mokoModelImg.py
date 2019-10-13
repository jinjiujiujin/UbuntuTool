#----------------------------------------------------------------------------------
#spider working on getting model pictures on moko website
#author zyyz
#version 1.0.0
#latest update 2019/10/13
#----------------------------------------------------------------------------------
from GetHtml import GetHtml_2 as GetHtml
import re


def GetUserPages(url):
    html = GetHtml(url)
    pageNums = re.findall(r'onfocus=\"this\.blur\(\)\">(\d*?)<', html, re.S)
    pageNum = max(pageNums)
    return int(pageNum)    

def GetUsers(url, users):
    html = GetHtml(url)
    urls = re.findall(r'<a class=\"imgBorder\" href="(.*?)" hidefocus=\"true\">', html, re.S)
    for s in urls:
        users.append("http://www.moko.cc"+s)

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
    