from mzitu_process_queue import urlQueue
from download import request
from bs4 import BeautifulSoup


def start(url):
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
            urlQueue.putValue(dictval)
            seen.add(href)
    print("队列大小为：" + str(urlQueue.size()))

url = "http://www.mzitu.com/all"
master = start(url)
