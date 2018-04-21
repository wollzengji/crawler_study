from multiprocessing import Queue
import requests
import os
import multiprocessing
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#爬取jilebox图片资源

UserAgent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
Referer= "http://pppbox.com/"
headers = {"User-Agent":UserAgent,"Referer":Referer}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

#使用本地chromedriver服务
browser = webdriver.Chrome(executable_path="D:\\selenium_server\\chromedriver")

jiledict={}
def jilebox_crawler(urlQueue):
    while True:
        if urlQueue.qsize() > 0:
            href=urlQueue.get()
            try:
                os.chdir("E:\jilebox" )
                html(href)
            except Exception as e:
                print('except:', e)
        else:
            print(jiledict)
            browser.close()
            break


def html(href):  ##这个函数获取图片集页面地址
    print("开始执行列表页面:" + href)
    browser.get(href)
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.ID, "waterfall")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pin-img")))
    waterfall = BeautifulSoup(browser.page_source, 'lxml').find('div', id='waterfall')
    divs = waterfall.findAll('div', class_='pin')
    for div in divs:
        taga = div.find("a")
        page_url = "http://pppbox.com" + taga.attrs.get("href")
        jiledict[href] = jiledict.get(href, 0) + 1
        img(page_url)


def img(page_url):
    print("开始执行详情页面:" + page_url)
    browser.get(page_url)
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.ID, "tinybox")))
    tinybox = browser.find_element_by_id('tinybox')
    imgs = tinybox.find_elements_by_tag_name("img")
    for img in imgs:
        save(img.get_attribute("src"))


def save(img_url):
    try:
        print(u'开始保存：', img_url)
        name = img_url[-19:-4]
        img = requests.get(img_url,  headers=headers)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
    except Exception as e:
        print('except:', e)



def getQueue(url):
    urlQueue = Queue()
    page=1
    while (page<=50):
        pageUrl=url+"&page="+str(page)
        urlQueue.put(pageUrl)
        page+=1
    return urlQueue


def process_crawler():
    #获取待爬地址列表
    url = "http://pppbox.com/photo/top?by=30"
    urlQueue=getQueue(url)
    print("需要抓取的页面数："+str(urlQueue.qsize()))
    #jilebox_crawler(urlQueue)
    #启动多线程执行程序
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=jilebox_crawler, args=(urlQueue,))  ##创建进程
        p.start()  ##启动进程
        process.append(p)  ##添加进进程队列
    for p in process:
        p.join()  ##等待进程队列里面的进程结束
    print("所有进程执行完毕")
    browser.quit()

if __name__ == "__main__":
    process_crawler()
