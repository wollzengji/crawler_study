from multiprocessing import Queue
import requests
import os
import multiprocessing
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#爬取jilebox短视频资源

UserAgent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
Referer= "http://pppbox.com/"
headers = {"User-Agent":UserAgent,"Referer":Referer}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

#使用本地chromedriver服务
browser = webdriver.Chrome(executable_path="D:\\selenium_server\\chromedriver")
jiledict={}
def jileboxvideo_crawler(urlQueue):
    while True:
        if urlQueue.qsize() > 0:
            href=urlQueue.get()
            try:
                os.chdir("E:\jileboxVideo25")
                html(href)
            except Exception as e:
                print('except:', e)
        else:
            print(jiledict)
            browser.close()
            break


def html(href):  ##这个函数获取视频集页面地址
    browser.get(href)
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.ID, "waterfall")))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pin-img")))
    waterfall = BeautifulSoup(browser.page_source, 'lxml').find('div', id='waterfall')
    divs=waterfall.findAll('div', class_='pin')
    for div in divs:
        taga=div.find("a")
        page_url="http://pppbox.com"+taga.attrs.get("href")
        print("所属页面:"+href+",下载页面："+page_url)
        jiledict[href] = jiledict.get(href,0)+1
        video(page_url)


def video(page_url):
    browser.get(page_url)
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.ID, "baidu_image_holder")))
    baidu_image_holder = browser.find_element_by_id('baidu_image_holder')
    video=baidu_image_holder.find_element_by_tag_name("video")
    save(video.get_attribute("src"))


def save(video_url):
    try:
        pass
        print(u'开始保存：', video_url)
        name = video_url[-30:-4]
        video = requests.get(video_url,  headers=headers)
        f = open(name + '.mp4', 'ab')
        f.write(video.content)
        f.close()
    except Exception as e:
        print('except:', e)



def getQueue(url):
    urlQueue = Queue()
    urlQueue.put(url+"&page=15")
    urlQueue.put(url + "&page=16")
    page=19
    while (page<=25):
        pageUrl=url+"&page="+str(page)
        urlQueue.put(pageUrl)
        page+=1
    return urlQueue


def process_crawler():
    #获取待爬地址列表
    url = "http://pppbox.com/video/top?by=100"
    urlQueue=getQueue(url)
    #jileboxvideo_crawler(urlQueue)
    #启动多线程执行程序
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=jileboxvideo_crawler, args=(urlQueue,))  ##创建进程
        p.start()  ##启动进程
        process.append(p)  ##添加进进程队列
    for p in process:
        p.join()  ##等待进程队列里面的进程结束
    print("所有进程执行完毕")
    browser.quit()

if __name__ == "__main__":
    process_crawler()
