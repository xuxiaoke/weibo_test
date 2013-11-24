#!/usr/bin/env python
# -*- coding: utf8 -*-
     
from weibo import APIClient
import weibo
import urllib2
import urllib
import sys
import time
from time import clock
import csv
import random


PAGE_SIZE = 200  

# 以列表的形式输出了好友的几项主要信息：uid，性别，屏幕名称和个人描述。  
def print_users_list(ul):  
#打印用户列表的详细信息  
    index = 0  
    for user in ul:  
        uid = user["id"]  
        ugen = user["gender"]  
        uname = user["screen_name"]  
#       uloc = user["location"]  
        udesc = user["description"]  
        print "%-6d%-12d%-3s%s%s" % (index, uid, ugen, uname.ljust(20), udesc.ljust(40))  
        index += 1  
      
def get_friends(client, uid=None, maxlen=0):  
    """ 
    读取uid用户的关注用户列表，默认uid=None，此时uid赋值为client.uid，而client.uid表示的是当前授权用户的uid. 
    """  
    if not uid:  
        uid = client.uid  
    return get_users(client, False, uid, maxlen)
      
def get_followers(client, uid=None, maxlen=0):  
    """ 
    读取uid用户的粉丝列表，默认uid=None，此时uid赋值为client.uid，而client.uid表示的是当前授权用户的uid. 
    """  
    if not uid:  
        uid = client.uid
    return get_users(client, True, uid, maxlen)  
      
def get_users(client, followersorfriends, uid, maxlen):  
    """ 
    调用API读取uid用户的关注用户列表或者粉丝列表，followersorfriends为True读取粉丝列表，为False读取关注好友列表， 
    参数maxlen设置要获取的好友列表的最大长度，为0表示没有设置最大长度，此时会尝试读取整个好友列表，但是API对于读取的 
    好友列表的长度会有限制，测试等级最大只能获取一个用户的5000条好友信息。 
    """  
    fl = []  
    next_cursor = 0  
    while True:  
        if followersorfriends:  
            raw_fl = client.friendships.followers.get(uid=uid, cursor=next_cursor, count=PAGE_SIZE)  
        else:  
            raw_fl = client.friendships.friends.get(uid=uid, cursor=next_cursor, count=PAGE_SIZE)  
        fl.extend(raw_fl["users"])  
        next_cursor = raw_fl["next_cursor"]  
        if not next_cursor:  
            break  
        if maxlen and len(fl) >= maxlen:  
            break  
        time.sleep(1)  
    return fl  
 
reload(sys)
sys.setdefaultencoding('utf-8')
     
'''Step 0 Login with OAuth2.0'''
if __name__ == "__main__":
    APP_KEY = '2629178103' # app key
    APP_SECRET = '4b261e8d38d53f4982584713627d4799' # app secret
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html' # set callback url exactly like this!
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    USERID = 'xiaokeeie@gmail.com' # your weibo user id
    PASSWD = 'fifa1234' #your pw
     
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    print "referer url is : %s" % referer_url
     
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
     
    postdata = {"client_id": APP_KEY,
            "redirect_uri": CALLBACK_URL,
            "userId": USERID,
            "passwd": PASSWD,
            "isLoginSina": "0",
                "action": "submit",
            "response_type": "code",
           }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
           "Host": "api.weibo.com",
           "Referer": referer_url
          }

    req  = urllib2.Request(
              url = AUTH_URL,
           data = urllib.urlencode(postdata),
           headers = headers
              )
    try:
        resp = urllib2.urlopen(req)
        print "callback url is : %s" % resp.geturl()
        code = resp.geturl()[-32:]
        print "code is : %s" %  code
    except Exception, e:
        print e
        
#新浪返回的token，类似abc123xyz456，每天的token不一样     
r = client.request_access_token(code)
access_token1 = r.access_token # The token return by sina
expires_in = r.expires_in
uid= r.uid
 
# http://open.weibo.com/wiki/OAuth2/access_token
print "access_token=" ,access_token1
print "expires_in=" ,expires_in   # access_token lifetime by second. 

     
"""save the access token"""
client.set_access_token(access_token1, expires_in)

#有了access_token后，可以做任何事情了
client.get.friendships.followers()


#以上步骤就是授权的过程，现在的client就可以随意调用接口进行微博操作了，
#下面的代码就是用用户输入的内容发一条新微博  
#调用接口发一条新微薄，status参数就是微博内容    
try:                                
    client.statuses.update.post(status="send a weibo message by python!")  
    print "Send succesfully!"  
except:   
    print "Error! Empty content!"
         
print "===> creat client successfully, authorised uid is : ", client.client_id 
print "============================== users ==========================="  

#读取当前授权用户的粉丝列表  
#fl = get_followers(r)  
      
#读取当前授权用户的关注好友列表  
#   fl = get_friends(r)  
  
#读取uid为‘1497035431’的用户的粉丝列表  
#uid = '1497035431' #梁斌penny  
fl = get_followers(r, uid='1900136460')  
print_users_list(fl)  
