from multiprocessing import Queue


class urlQueue():

    def __init__(self):
        self.url_queue = Queue()

    def putValue(self,url):
        self.url_queue.put(url)

    def size(self):
        return self.url_queue.qsize()

    def getValue(self):

        return self.url_queue.get()

urlQueue=urlQueue()