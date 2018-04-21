from multiprocessing import Queue
from download import request
from bs4 import BeautifulSoup
import os
import multiprocessing

#实现了由多线程加queue组合来爬取数据，但是为实现将各个类分离，mzitu_process_queue\mzitu_process_master没用到
def mzitu_crawler(urlQueue):
    while True:
        if urlQueue.qsize() > 0:
            dicval=urlQueue.get()
            href = dicval.get("url")
            title=dicval.get("title")
            try:
                if mkdir(title):
                    os.chdir("E:\mzitu\\" + title)
                    html(href)
            except Exception as e:
                print('except:', e)
        else:
            break


def html(href):  ##这个函数是处理套图地址获得图片的页面地址
    html = request.get(href, 3)
    pagenavi = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
    if pagenavi:
        max_span = pagenavi.find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            img(page_url)  ##调用img函数


def img(page_url):
    img_html = request.get(page_url, 3)
    img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
    save(img_url)


def save(img_url):
    try:
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
    except Exception as e:
        print('except:', e)


def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(os.path.join("E:\mzitu", path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join("E:\mzitu", path))
        return True
    else:
        print(u'名字叫做', path, u'的文件夹已经存在了！')
        return False

def getQueue(url):
    urlQueue = Queue()
    seen = set()  # 主要用于url去重
    seen.add(url)
    html = request.get(url, 3)
    all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
    for a in all_a:
        href = a['href']
        title = a.get_text()
        path = str(title).replace("?", '_')
        if href not in seen:
            dictval = {"url": href, "title": path}
            urlQueue.put(dictval)
            seen.add(href)
    print("队列大小为：" + str(urlQueue.qsize()))
    return urlQueue


def process_crawler():
    # 获取待爬地址列表
    url = "http://www.mzitu.com/all"
    urlQueue = getQueue(url)

    # 启动多线程执行程序
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler, args=(urlQueue,))  ##创建进程
        p.start()  ##启动进程
        process.append(p)  ##添加进进程队列
    for p in process:
        p.join()  ##等待进程队列里面的进程结束
    print("所有进程执行完毕")


if __name__ == "__main__":
    process_crawler()
