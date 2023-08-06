import requests
import traceback
from multiprocessing.pool import ThreadPool

name = 'mrequests'

class PoolRequests(object):

    def __init__(self,method,**kwargs):
        self.method = method
        self.session = kwargs.pop('session',None)

        if self.session is None:
            self.session = requests.Session()

        adapter = requests.adapters.HTTPAdapter(pool_connections=100,pool_maxsize=100)
        self.session.mount("https://",adapter)

    def send_request(self,url):
        self.url = url
        try:
            self.response = self.session.request(self.method,self.url)
        except Exception as e:
            self.exception = e
            self.traceback = traceback.format_exc()
        return self.response

    def send(self,urls,**kwargs):
        pool = ThreadPool(32)
        self.urls = urls
        results = pool.map(self.send_request,self.urls)
        pool.close()
        pool.join()
        return results
