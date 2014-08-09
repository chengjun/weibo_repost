#!/usr/bin/env python
# -*- coding: utf8 -*-

from weibo import APIClient
import urllib2
import urllib
import sys
import time
from time import clock
import random

reload(sys); sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()

'''
network_surfer
App Key 63049101
App Secret fc9ed9a3b9e7f37c3e6667464f0617e
'''

'''Login with OAuth2.0'''

def weiboClient():
    APP_KEY = '663049101' # app key
    APP_SECRET = '2fc9ed9a3b9e7f37c3e6667464f0617e' # app secret
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html' # callback url
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    USERID = 'wangchj04'
    PASSWD = 'weibochengwang6' #your pw
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
    r = client.request_access_token(code)
    access_token1 = r.access_token # The token return by sina
    expires_in = r.expires_in 
     
    print "access_token=" ,access_token1
    print "expires_in=" ,expires_in   # access_token lifetime by second. http://open.weibo.com/wiki/OAuth2/access_token
    client.set_access_token(access_token1, expires_in) 
    return client



def getPageNum(mid):
    count = client.get.statuses__count(ids = mid)
    repostNum = count[0]['reposts']
    if repostNum%200 == 0:
        pages = repostNum/200
    else:
        pages = int(repostNum/200) + 1
    return pages
 


def getReposts(mid, page):    
    r = client.get.statuses__repost_timeline(id = mid, page = page, count = 200)
    if len(r) == 0:
        pass
    else:
        m = int(len(r['reposts']))
    try:
        for i in range(0, m):
            """1.1 reposts"""
            mid = r['reposts'][i].id
            text = r['reposts'][i].text.replace(",", "")
            created = r['reposts'][i].created_at
            reposts_count = r['reposts'][i].reposts_count
            comments_count = r['reposts'][i].comments_count
            """1.2 reposts.user"""
            user = r['reposts'][i].user
            user_id = user.id
            user_name = user.name
            user_province = user.province
            user_city = user.city
            user_gender = user.gender
            user_url = user.url
            user_followers = user.followers_count
            #user_bifollowers = user.bi_followers_count
            user_friends = user.friends_count
            user_statuses = user.statuses_count
            user_created = user.created_at
            user_verified = user.verified
            """2.1 retweeted_status"""
            rts = r['reposts'][i].retweeted_status
            rts_mid = rts.id
            #rts_text = rts.text.replace(",", "")
            rts_created = rts.created_at
            rts_reposts_count = rts.reposts_count
            rts_comments_count = rts.comments_count
            """2.2 retweeted_status.user"""
            rtsuser_id = rts.user.id
            rtsuser_name = rts.user.name
            rtsuser_province = rts.user.province
            rtsuser_city = rts.user.city
            rtsuser_gender = rts.user.gender
            rtsuser_url = rts.user.url
            rtsuser_followers = rts.user.followers_count
            #rtsuser_bifollowers = rts.user.bi_followers_count
            rtsuser_friends = rts.user.friends_count
            rtsuser_statuses = rts.user.statuses_count
            rtsuser_created = rts.user.created_at
            rtsuser_verified = rts.user.verified
            timePass = clock()-start
            if round(timePass) % 10 == 0:
                print mid, rts_mid, "I have been working for %s seconds" % round(timePass)
                time.sleep( random.randrange(3, 9, 1) )  # To avoid http error 504 gateway time-out
            print >>dataFile, "%s,'%s','%s',%s,%s,%s,%s,%s,'%s',%s,%s,%s,'%s',%s,%s,%s,'%s',%s,%s,'%s',%s,'%s',%s,%s,%s,'%s',%s,%s,%s,%s,%s"  % (mid, created, text,     
                         reposts_count, comments_count,rts_reposts_count, rts_comments_count,
                         user_id, user_name, user_province, user_city, user_gender,  # 5 --> 5
    				 user_url, user_followers, user_friends, user_statuses, user_created, user_verified,  # rts_text, # 6 --> 9
    				 rts_mid, rts_created, # 2
    				 rtsuser_id, rtsuser_name, rtsuser_province, rtsuser_city, rtsuser_gender, # 5 --> 18
    				 rtsuser_url, rtsuser_followers, rtsuser_friends, rtsuser_statuses, rtsuser_created, rtsuser_verified)  # 6  --> 22
    except Exception, e:
        print >> sys.stderr, 'Encountered Exception:', e, page
        time.sleep(120)
        pass
	
def get2stepReposts(mid, uid, page):    
    try:
        r = client.get.statuses__repost_timeline(id = mid, page = page, count = 200)
        if len(r) == 0:
            pass
        else:
            m = int(len(r['reposts']))
        for i in range(0, m):
            """1.1 reposts"""
            rt_mid = r['reposts'][i].id
            created = r['reposts'][i].created_at
            """1.2 reposts.user"""
            user = r['reposts'][i].user
            rt_uid = user.id
            print >>dataFile2, "%s,%s,%s,%s,'%s'"  % (mid, uid, rt_mid, rt_uid, created)   
    except Exception, e:
        print >> sys.stderr, 'Encountered Exception:', e, page
        time.sleep(120)
        pass 
 
client = weiboClient()


#r = client.get.statuses__repost_timeline(id = mid, page =1 , count = 200)
#count = client.get.statuses__count(ids = mid)
#[{'attitudes': 408, 'id': 3741020640174910L, 'comments': 428, 'reposts': 1060}]
#
#mid = client.get.statuses__queryid(mid = 'Bhd8k0Jv8', isBase62 = 1, type = 1)['id']
#pageNum = getPageNum(mid) 
#
#dataFile = open("D:/github/weibo_repost/weibo_repost_all.csv",'wb') 
#start = clock()
#print start
#for page in range(1, pageNum + 1):
#    getReposts(mid, page)
#dataFile.close()

f = open("D:/github/weibo_repost/weibo_repost_all.csv")
l = f.readline(); print l
line = l.strip().split(','); print line

with open("D:/github/weibo_repost/weibo_repost_all.csv") as f:
    a = 0
    for line in f:
        line = line.strip().split(',')
        repostCount = int(line[3])
        mid2step = line[0]
        uid = line[7]
        if repostCount > 0:
            print repostCount
            a += repostCount
            
            if repostCount%200 == 0:
                pages = repostCount/200
            else:
                pages = int(repostCount/200) + 1
            dataFile2 = open("D:/github/weibo_repost/weibo_repost_2_step.csv",'a') 
            for page in range(1, pages + 1):
                get2stepReposts(mid2step, uid, page)
            dataFile2.close()  

            
with open("D:/github/weibo_repost/weibo_repost_all.csv") as f:
    mids = []    
    for line in f:
        line = line.strip().split(',')
        mid = line[0]
        mids.append(mid)
            
with open("D:/github/weibo_repost/weibo_repost_2_step.csv") as f:
    toNodes = []
    for line in f:
        line = line.strip().split(',')
        mid = line[2]
        toNodes.append(mid)
        
oneStep = []        
for i in mids:
    if i not in toNodes:
        oneStep.append(i)

with open("D:/github/weibo_repost/weibo_repost_all.csv") as f:   
    for line in f:
        line = line.strip().split(',')
        created = line[1]
        mid = line[0]
        uid = line[7]
        rtmid = line[18]
        rtuid= line[20]
        with open('D:/github/weibo_repost/weibo_repost_1_step.csv', 'a') as g:
            record = rtmid + ','+ rtuid+','+ mid + ','+uid+','+created
            g.write(record+"\n")

with open("D:/github/weibo_repost/weibo_repost_1_step.csv") as f:
    for line in f:
        with open('D:/github/weibo_repost/weibo_reposts_network.csv', 'a') as g:
            g.write(line)
with open("D:/github/weibo_repost/weibo_repost_2_step.csv") as f:
    for line in f:
        with open('D:/github/weibo_repost/weibo_reposts_network.csv', 'a') as g:
            g.write(line)
            

import networkx as nx
import numpy
import matplotlib.pyplot as plt

with open('D:/github/weibo_repost/weibo_repost_network.csv', 'r') as f:
    weight = []
    for line in f:
        time= line.strip().split(',')[-1]
        day = time[7:9]
        hms= time[9:17].replace(':', '')
        time = int(day + hms)
        weight.append(time)
        

array = numpy.array(weight)
order = array.argsort()
ranks = order.argsort()
        
G = nx.Graph()
with open('D:/github/weibo_repost/weibo_repost_network.csv', 'r') as f:
    for position, line in enumerate(f):
        mid, uid, rtmid, rtuid= line.strip().split(',')[:-1]
        G.add_edge(uid, rtuid, weight = ranks[position])
        
edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
        
degree = nx.degree(G)
pos=nx.spring_layout(G)
nx.draw(G, pos, nodelist = degree.keys(),
        node_size = [v*5 for v in degree.values()], node_color = 'orange', 
        edgelist = edges, edge_color = weights, width = 5, edge_cmap=plt.cm.Blues, 
        with_labels = False)
plt.savefig("D:/github/weibo_repost/diffusion.png", dpi = 300)

degree = nx.degree(G)
closenesss = nx.closeness_centrality(G)
betweenness = nx.betweenness_centrality(G)
G.number_of_edges() # 1547
nx.diameter(G) # 2

T = nx.minimum_spanning_tree(G)
nx.draw(T, node_size = 2, with_labels = False)