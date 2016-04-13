__author__ = 'zuoyan'
#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re
import urllib2
import urllib
import requests
import cookielib
import os
import time
from multiprocessing import Pool
from bs4 import BeautifulSoup
import socket


reload(sys)
sys.setdefaultencoding("utf8")
#####################################################
socket.setdefaulttimeout(90)
loginurl = 'https://musescore.com/user/login?destination=home'
logindomain = '.musescore.com'
root_link = r'https://musescore.com'
totalresult = {}

def download_file(url):
        #local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        #print url
        rs = requests.get(url)
        print rs.headers
        local_filename = rs.headers['content-disposition'].split('=')[1].lstrip('"').rstrip('"')
        #r = requests.get(rs.url, stream=True)
        #with open(local_filename, 'wb') as f:
         #   for chunk in r.iter_content(chunk_size=1024):
                # filter out keep-alive new chunks
          #      if chunk:
           #         f.write(chunk)
            #        f.flush()

        return local_filename

class Login(object):

    def __init__(self):
        self.name = ''
        self.passwprd = ''
        self.domain = ''

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setLoginInfo(self,username,password,domain,form_build_id,form_id):
        self.name = username
        self.pwd = password
        self.domain = domain
        self.form_build_id = form_build_id
        self.form_id = form_id

    def login(self):
        loginparams = {'domain':self.domain,'name':self.name, 'pass':self.pwd, 'form_build_id':self.form_build_id, 'form_id':self.form_id, 'op':'Log in'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(loginurl, urllib.urlencode(loginparams),headers=headers)
        response = urllib2.urlopen(req)
        #print response.url
        self.operate = self.opener.open(req)
        #thePage = response.read()
        result = {}
        if response.getcode() == 200:
            soup = BeautifulSoup(response.read())
            links = soup.find_all('a',href="/sheetmusic")
            #print links
            path = [root_link+l.get('href') for l in links]
            req = requests.get(path[0],headers=headers)
            #print req
            soup = BeautifulSoup(req.text)
            links = soup.find_all('a',href=re.compile("page"))
            #print '###'
            #print links
            req = requests.post(path[0]+'?page1',headers=headers)
            soup = BeautifulSoup(req.text)
            links = soup.find_all('a',href=re.compile("scores"))
            links = [root_link + l.get('href') for l in links if l.get('href')]
            blinks = list(set(links))
            #print blinks
            downloadlinks = []
            for i in blinks:
                req = requests.post(i,headers=headers)
                soup = BeautifulSoup(req.text)
                plinks = soup.find_all('a',href=re.compile("download/pdf"))
                plinks = [root_link + l.get('href') for l in plinks if l.get('href')]
                #print plinks[0]
                r = urllib2.Request(plinks[0],headers=headers)
                response = urllib2.urlopen(r,timeout=2)
                print response.url
                link = response.url
                songname = str(response.url)
                #songname.decode('GBK')
                #songname.encode('utf-8')
                songname = songname.replace(' ', '_')
                songname = songname.replace('\n', '_')
                if totalresult.has_key(link) and len(songname) < len(totalresult[link]):
                    continue
                else:
                    totalresult[link] = songname
                    result[link] = songname
                #download_file(response.url)
                #time.sleep(10)
                #downloadlinks.append(plinks[0])
            #print downloadlinks
            #print response.url
            #pool = Pool(8)
            #results = pool.map(download_file, downloadlinks)
            return result
            print "all download finished\n"

    def writedata(databasepath):
        datafile = open(databasepath, 'a')
        for link in totalresult.keys():
            datafile.write(link, '\n')
        datafile.close()


if __name__ == '__main__':
    databasepath = 'D:\1\midi\linklist'
    path = 'D:/1/midi/dugukeji/'
    userlogin = Login()
    username = 'kate.zuo'
    password = 'w123456789'
    form_build_id = 'form-a106ac5e54b729075d0d4d8add8f95dc'
    form_id = 'user_login'
    domain = logindomain
    userlogin.setLoginInfo(username,password,domain,form_build_id,form_id)
    arr = userlogin.login()
    userlogin.writedata(databasepath)
