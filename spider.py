# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import logging
import logging.config

logging.basicConfig(level=logging.ERROR,
    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a')

def get_hotword(website):
    if website=='weibo':
        return get_weibo_hotword()
    elif website=='baidu':
        return get_baidu_hotword()
    elif website=='zhihu':
        return get_zhihu_hotquestion()
    return None,None

def get_zhihu_hotquestion():
#知乎热榜. 需要有40条
#返回两个list，热度值和词表。数量不是40，返回两个None
    try:
        headers = {
                'Host':'www.zhihu.com',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Accept-Encoding':'gzip'
            }
        zh_url='https://www.zhihu.com/billboard'
        s=requests.Session()
        r=s.get(zh_url,headers=headers)
        html=r.text
        soup=BeautifulSoup(html,'lxml')
        list_no=list()
        list_word=list()
        list_score=list()
        for td01 in soup.find_all(class_='HotList-itemIndex'):
            list_no.append(td01.string)
        for w in soup.find_all(class_="HotList-itemTitle"):
            word=w.string
            word=word.encode('utf-8').decode('utf-8')
            list_word.append(word)
        for num in soup.find_all(class_="HotList-itemMetrics"):
            n=num.get_text()
            number=n.split(' ')[0]
            number=int(number)*10000
            if n.split(' ')[1]=='万热度':
                list_score.append(number)
        if not (  len(list_no) == 40 and len(list_score)==40 and len(list_word)==40 ):
            logging.error('Error: Zhihu billborad list number not 40')
            return None,None
        else:
            return list_score,list_word
    except Exception as e:
        logging.error(e.args)
        logging.error('Error: Zihu Exception occured in spider')
        return None,None

def get_weibo_hotword():
#微博热搜榜. 需要有51条，其中第一条没有热度值score
#返回两个list，热度值和词表。数量不是51，返回两个None
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
        headers = {'User-Agent' : user_agent} 
        weibo_url='http://s.weibo.com/top/summary?cate=realtimehot'
        r=requests.get(weibo_url,headers)
        html=r.text
        soup=BeautifulSoup(html,'lxml')
        s=soup.find_all('script')
        word=str(s[-2])
        word=word.replace('\\n','')
        word=word.replace('\\"','"')
        word=word.replace('\\/','/')
        hh=re.findall(r'<div class=\"hot_ranklist\">.*</div>',word)
        hh=hh[0]
        soup=BeautifulSoup(hh,'lxml')
        
        list_no=list()
        list_word=list()
        list_score=list()
        list_score.append(0)
        for td01 in soup.find_all(class_='td_01'):
            list_no.append(td01.string)
        
        for w in soup.find_all(class_="star_name"):
            word=w.a.string
            word=word.encode('latin-1').decode('unicode_escape')
            list_word.append(word)
            
        for num in soup.find_all(class_="star_num"):
            n=num.string
            list_score.append(n)
        
        if not (  len(list_no) == 51 and len(list_score)==51 and len(list_word)==51 ):
            logging.error('Error: Sina Weibo list number not 51')
            return None,None
        else:
            return list_score,list_word
    except Exception as e:
        logging.error(e.args)
        logging.error('Error: Sina Weibo Exception occured in spider')
        return None,None

        
def get_baidu_hotword():
#百度实时热点排行榜. 需要有50条
#返回两个list，热度值和词表。数量不是50，返回两个None
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
        headers = {'User-Agent' : user_agent} 
        baidu_url='http://top.baidu.com/buzz?b=1'
        r=requests.get(baidu_url,headers)
        html=r.text
        html=html.encode('latin-1').decode('gbk')
        soup=BeautifulSoup(html,'lxml')
        
        
        list_word=list()
        list_score=list()
       
        for w in soup.find_all(class_='list-title'):
            list_word.append(w.string)
        

        for num in soup.find_all('td',class_="last"):
            n=num.span.string
            list_score.append(n)
        
        if not (  len(list_score)==50 and len(list_word)==50 ):
            logging.error('Error: Baidu list number not 50')
            return None,None
        else:
            return list_score,list_word
    except Exception as e:
        logging.error(e.args)
        logging.error('Error: Baidu Exception occured in spider')
        return None,None
