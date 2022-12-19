# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
#class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """

import threading
from queue import Queue

class CrawlerRunner:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        lock =  threading.Lock()
        queue = Queue()
        queue.put(startUrl)
        visited = set()
        visited.add(startUrl)
        numWorkers= 8
        workers = []

        for i in range(numWorkers):
            crawler = Crawler(baseUrl=startUrl.split("/")[2],queue=queue,htmlParser=htmlParser,visited=visited,lock=lock)
            crawler.start()
            workers.append(crawler)

        queue.join()
        for i in range(numWorkers):
            queue.put(None)
        for worker in workers:
            worker.join()

        return list(visited)

class Crawler(threading.Thread):
    def __init__(self,baseUrl,queue,htmlParser,visited,lock):
        threading.Thread.__init__(self)
        self.baseUrl = baseUrl
        self.queue =  queue
        self.visited = visited 
        self.htmlParser = htmlParser
        self.lock = lock
        
    def run(self):
        while True:
            url = self.queue.get()
            if url is None:
                return

            for next_url in self.htmlParser.getUrls(url):
                if next_url.split("/")[2] == self.baseUrl and next_url not in self.visited:
                    self.lock.acquire()
                    if next_url not in self.visited:
                        self.visited.add(next_url)
                        self.queue.put(next_url)
                    self.lock.release()
            self.queue.task_done()

    