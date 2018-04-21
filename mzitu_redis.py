from bs4 import BeautifulSoup
import os
from download import request
import redis
import datetime

class mzitu():

    def __init__(self):
        pool = redis.ConnectionPool(host='192.168.0.23', port=6379)
        self.red = redis.Redis(connection_pool=pool)

    def all_url(self, url):

        html = request.get(url, 3)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            try:
                title = a.get_text()
                path = str(title).replace("?", '_')
                #if self.mkdir(path):
                self.mkdir(path)
                href = a['href']
                if self.red.get(href):  #通过redis判断页面是否已经下载过了
                    print("已下载了："+title)
                else:
                    os.chdir("E:\mzitu\\" + path)
                    dic = {"title": title, "href": href,"time":datetime.datetime.now()}
                    self.red.set(href, dic)
                    print(u'开始下载：', title)
                    self.html(href)
            except Exception as e:
                print('except:', e)

    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        html = request.get(href, 3)
        pagenavi=BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
        if pagenavi:
            max_span =pagenavi .find_all('span')[-2].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                self.img(page_url) ##调用img函数


    def img(self, page_url):
        img_html = request.get(page_url, 3)  ##这儿更改了一下（是不是发现  self 没见了？）
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        try:
            name = img_url[-9:-4]
            print(u'开始保存：', img_url)
            img = request.get(img_url, 3)  ##这儿更改了一下（是不是发现  self 没见了？）
            f = open(name + '.jpg', 'ab')
            f.write(img.content)
            f.close()
        except Exception as e:
            print('except:', e)

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("E:\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("E:\mzitu", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False


Mzitu = mzitu()  ##实例化
Mzitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）