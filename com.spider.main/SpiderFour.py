# coding=utf-8
__author__ = 'zuoyan'
import urllib2, urllib
import re
import os
import sys
import cookielib
urlmapId = {}
downloadPath = "D:\\1\midi\\linklist"
baseloadPath = "D:\\1\midi\\baselinklist"
setCup = {"https://musescore.com/sheetmusic"}
hashUrl = set()
sys.setrecursionlimit(1000000);

def pageIter(url, proxy, loginparams):
    content = pageOpener(url, proxy, loginparams)
    #print "url"
    for i in parsehttpUrl(content):
        hashUrlStr = hash(i)
        if hashUrlStr in hashUrl:
            continue
        elif len(re.compile(r"/user/\d+\.?\d*/scores/\d+\.?\d*").findall(i)) > 0:
            hashUrl.add(hashUrlStr)
            writeData(baseloadPath, str(hashUrlStr) + "\t" + i)
            parsePage(i)
            continue
        elif i.find("/sheetmusic?page") == 0 and i.find("https") < 0:
            hashUrl.add(hashUrlStr)
            urlhttp = "https://musescore.com" + i
            # print urlhttp
            writeData(baseloadPath, str(hashUrlStr) + "\t" + i)
            pageIter(urlhttp, proxy, "1")
        elif i.find("https") == 0 and i.find(url) < 0:
            hashUrl.add(hashUrlStr)
            # print i
            writeData(baseloadPath, str(hashUrlStr) + "\t" + i)
            continue
            #pageIter(i,proxy,loginparams)
        elif i.find(url) == 0:
            hashUrl.add(hashUrlStr)
            writeData(baseloadPath, str(hashUrlStr) + "\t" + i)
            continue
    return


def pageOpener(url, proxy, loginparams):
    """采用递归方式，判断条件是第一页数据条数 > 某一页，则退出"""
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxy}), urllib2.HTTPHandler(debuglevel=1))
    urllib2.install_opener(opener)

    i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Referer": 'http://www.baidu.com'}
    # print url
    # req = urllib2.Request(url, headers=i_headers)
    # content = urllib2.urlopen(req).read()
    if loginparams.__len__() > 2:
        req = urllib2.Request(url, urllib.urlencode(loginparams), headers=i_headers)
        content = urllib2.urlopen(req).read()
    else:
        req = urllib2.Request(url)
        content = urllib2.urlopen(req).read()
    #print content

    return content


def parsePage(Str):
    """抽取相关标签及类似“/user/7340851/scores/1882731” 写入文件"""
    linkPattern = re.compile(r"\d+\.?\d*")
    result = linkPattern.findall(Str)
    if len(result) > 0:
        convertToDownloadUrl(result[1])
        return "ok"
    else:
        return ""


def parsehttpUrl(htmlStr):
    linkPattern = re.compile("href=\"(.+?)\"")
    return linkPattern.findall(htmlStr)


def convertToDownloadUrl(downLoadId):
    """把“/user/7340851/scores/xxxx”抽取出xxxx直接换成“https://musescore.com/score/xxxx/download/pdf”进行下载"""
    downloadUrl = "https://musescore.com/score/" + downLoadId + "/download/pdf"
    writeData(downloadPath, downLoadId + "\t" +downloadUrl)
    return "ok"



def downloadMusic(filePath, proxy, loginparams):
    """判断下载回话是否过期，完成登录，并下载文件"""
    count = 0
    for line in open(filePath):
        linkArr = line.split("\t")
        count += 1
        counet = pageOpener(linkArr[1], proxy, loginparams)
        print counet
    return ""


def writeData(path, data):
    if not os.path.exists(path):
        os.mkdir(path)
    datafile = open(path, 'a')
    datafile.write(data + '\n')
    datafile.close()


def readData(a):
    file = open(baseloadPath, 'r')
    for line in file.readlines():
        if a in line:
            return True
        else:
            writeData(baseloadPath,a)
            return False

if __name__ == '__main__':
    username = 'kate.zuo'
    password = 'w123456789'
    #form_build_id = 'form-a106ac5e54b729075d0d4d8add8f95dc'
    #form_id = 'user_login'
    #logindomain = '.musescore.com'
    #loginparams = {'domain': logindomain, 'name': username, 'pass': password, 'form_build_id': form_build_id,
    #               'form_id': form_id, 'op': 'Log in'}
    loginparams = {'name': username, 'pass': password}
    #loginparams = urllib.urlencode(loginparams)
    url = "https://musescore.com/sheetmusic"
    proxy = "135.238.92:9090"
    # try:
    #     pageIter(url, proxy, "")
    # except Exception as ex:
    #     print ex
    # print "url writes ok! ╭(′▽`)╭(′▽`)╯(让咱们一起奔向下载吧...) "
    downloadMusic(downloadPath,proxy,loginparams)