#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author: coderss
time: 17/6/29 下午3:48
contact: admin@coderss.cn
role   : Version Update
'''

# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib2
import urllib
import cookielib
import random
import string
import re
import time
import httplib
from pyquery import PyQuery as pyq

httplib.HTTPConnection.debuglevel = 1


class PhpWindApi:
    def __init__(self, forumUrl, userName, password, proxy=None):
        ''' 初始化论坛url、用户名、密码和代理服务器 '''
        self.forumUrl = forumUrl
        self.userName = userName
        self.password = password
        self.formhash = ''
        self.isLogon = False
        self.isSign = False
        self.xq = ''
        self.postOldData = {}
        self.get_post_form_data = {}
        self.jar = cookielib.CookieJar()
        self.pids = []
        self.get_reply_content = [u"顶[s:53] [s:53] ",
                                  u"菱湖人顶个贴",
                                  u"[s:48] [s:48] [s:48] 顶顶",
                                  u"老菱湖人来顶顶帖子",
                                  u"混个脸熟[s:48] [s:48]",
                                  u"[s:89] [s:89] [s:89] [s:89] ",
                                  u"[s:77] [s:77] [s:77] 菱湖人路过",
                                  u"[s:53][s:53]顶[s:53]",
                                  u"顶顶顶[s:53][s:53]",
                                  u"[s:53]路过[s:53][s:53]",
                                  u"走走看看[s:53][s:53]",
                                  u"老菱湖人看看[s:53][s:53]",
                                  u"有没有菱湖的[s:53]"]
        if not proxy:
            openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar))
        else:
            openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar),
                                           urllib2.ProxyHandler({'http': proxy}))
        urllib2.install_opener(openner)
        req = urllib2.Request(forumUrl + "/login.php?")
        content = urllib2.urlopen(req).read()
        doc = pyq(content)
        for item in doc("form").children("input").items():
            self.postOldData[item.attr("name")] = item.val()




    def login(self):
        ''' 登录论坛 '''
        url = self.forumUrl + "/login.php?XDEBUG_SESSION_START=11992"
        self.postOldData['pwuser'] = self.userName
        self.postOldData['pwpwd'] = self.password
        postData = urllib.urlencode(self.postOldData)
        req = urllib2.Request(url, postData)
        content = urllib2.urlopen(req).read()
        doc = pyq(content)
        msg_str = doc(".mb10").text()
        print msg_str
        self.isLogon = True
        print 'logon success!'
        return 1

    def get_post(self, tid):
        url = self.forumUrl + 'read.php?tid={tid}'.format(tid=tid)
        req = urllib2.Request(url)
        content = urllib2.urlopen(req).read().decode('gbk')
        doc = pyq(content)
        #获取相关提交的表单
        for item in doc("#formHiddens").children("input").items():
            self.get_post_form_data[item.attr['name']] = item.val()
        # self.get_post_form_data[doc("#atc_title_tianyang").attr('name')] = doc("#atc_title_tianyang").val().encode('utf-8')
        self.get_post_form_data[doc("#atc_title").attr('name')] = doc("#atc_title").val()
        self.get_post_form_data_url = doc("#anchor").attr("action")



    def reply(self, tid):
        ''' 回帖 '''
        url = self.forumUrl + self.get_post_form_data_url + "&XDEBUG_SESSION_START=11992"
        index = random.randint(0, len(self.get_reply_content))
        content = self.get_reply_content[index]
        print u"回复内容:%s" % content
        #额外的输入参数
        postOldData = {'atc_content': content.encode('gbk'),
                       'usernames': ''}
        self.get_post_form_data.update(postOldData)
        postData = urllib.urlencode(self.get_post_form_data)
        req = urllib2.Request(url, postData)
        content = urllib2.urlopen(req).read().decode('gbk')
        if 'success' in content:
            print 'reply success!'
        else:
            print 'reply faild!'


    def get_posts(self, fid, multi=False, index=2, size=100):
        if multi:
            for index in range(index, size, 1):
                time.sleep(random.randint(20, 60))
                url = self.forumUrl + "thread-htm-fid-{fid}-page-{page}.html".format(fid=fid,
                                                                                     page=index)
                req = urllib2.Request(url)
                content = urllib2.urlopen(req).read().decode('gbk')
                doc = pyq(content)
                data = doc("#threadlist").children(".nthtr3").items()
                for item in data:
                    pid = item.children(".subject").attr("id").split("td_")[1]
                    print "当前的帖子id: %s" % pid
                    self.pids.append(pid)
                    time.sleep(random.randint(30, 200))
                    self.get_post(pid)
                    time.sleep(random.randint(20, 200))
                    self.reply(pid)
        else:
            time.sleep(random.randint(20, 60))
            url = self.forumUrl + "thread-htm-fid-{fid}.html".format(fid=fid)
            req = urllib2.Request(url)
            content = urllib2.urlopen(req).read().decode('gbk')
            doc = pyq(content)
            for item in doc("#threadlist").children(".nthtr3").items():
                pid = item.children(".subject").attr("id").split("td_")[1]
                print "当前的帖子id: %s" % pid
                self.pids.append(pid)
                time.sleep(random.randint(30, 200))
                self.get_posts(pid)
                time.sleep(random.randint(20, 300))
                self.reply(pid)

    def person(self):
        url = self.forumUrl + 'u.php'
        req = urllib2.Request(url)
        content = urllib2.urlopen(req).read().decode('gbk')
        print content


if __name__ == '__main__':
    robot = PhpWindApi("http://bbs.nantaihu.com/", "3751260@qq.com", "****")
    robot.login()
    #robot.person()
    while True:
        robot.get_posts(4, True)



