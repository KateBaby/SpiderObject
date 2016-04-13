__author__ = 'zuoyan'
#coding=gbk
import urllib2, urllib, cookielib, threading
import os
import requests
import re
import bs4
import sys

urlMap = {'key': "", 'value': ""}
urllist = []
databasepath = 'D:\\1\\midi\\baselinklist'
urlpath = 'D:\\1\midi\\linklist'


def findLinks(htmlString):
    #linkPattern = re.compile(r"<a.*?href=.*?<\/a>")
    linkPattern = re.compile("href=\"(.+?)\"")
    return linkPattern.findall(htmlString)


def get_content_by_proxy(url, proxy, loginparams):
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), urllib2.HTTPHandler(debuglevel=1))
    urllib2.install_opener(opener)

    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Referer": 'http://www.baidu.com'}

    req = urllib2.Request(url, urllib.urlencode(loginparams), headers=i_headers)
    content = urllib2.urlopen(req).read()
    print content
   # content = bs4.BeautifulSoup(content, from_encoding='GB18030')
    for i in findLinks(content):
        print urlMap.has_key(i)
        if urlMap.has_key(i) == False:
            urlMap.setdefault(i, "")
            datafile1 = open(databasepath, 'a')
            datafile1.write(i+'\n')
            datafile1.close()
        if i.find("https") == 0:
            if requests.get(i).status_code == 200:
                if i.find("pdf") == 0:
                    print i
                    datafile = open(urlpath, 'a')
                    datafile.write(i+'\n')
                    datafile.close()
                else:
                    get_content_by_proxy(i, proxy, loginparams)
        elif i.find("/user/") == 0 or i.find("/sheetmusic?page=") == 0:
            if urlMap.has_key(i) == False:
                unurl = "https://musescore.com"+i
                datafile1 = open(databasepath, 'a')
                datafile1.write(unurl+'\n')
                datafile1.close()
                get_content_by_proxy(unurl, proxy, loginparams)

    return "ok"


if __name__ == '__main__':
    username = 'kate.zuo'
    password = 'w123456789'
    form_build_id = 'form-a106ac5e54b729075d0d4d8add8f95dc'
    form_id = 'user_login'
    logindomain = '.musescore.com'
    loginparams = {'domain': logindomain, 'name': username, 'pass': password, 'form_build_id': form_build_id, 'form_id': form_id, 'op': 'Log in'}
    url = "https://musescore.com/sheetmusic"
    proxy = "135.238.92:9090"
    print get_content_by_proxy(url,proxy,loginparams)