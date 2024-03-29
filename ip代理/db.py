import json
import urllib.request

from pyquery import PyQuery as pq

class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


def get_page(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    return html

class Crawler(object, metaclass=ProxyMetaClass):
     def get_proxies(self, callback):
         proxies = []
         for proxy in eval("self.{}()".format(callback)):
             print('成功获取代理', proxy)
             proxies.append(proxy)
         return proxies
         
     def crawl_dail66ip(self, page_count=6):
         '''
         获取66ip代理
         :param page_count: 页码
         :return: 代理
         '''
         start_url = 'http://www.66ip.cn/{}.html'
         urls = [start_url.format(page) for page in range(1, page_count+1)]
         for url in urls:
             print('Crawling',url)
             html = get_page(url)
             if html:
                 doc = pq(html)
                 trs = doc('.containerbox tr:gt(1)').items()
                 for tr in trs:
                     ip = tr.find('td:nth-child(1)').text()
                     port = tr.find('td:nth-child(2)').text()
                     yield  ':'.join([ip, port])


     # def crawl_proxy360(self):
     #     '''
     #     获取360ip代理
     #     :return: 代理
     #     '''
     #     start_url = 'http://www.proxy360.cn/Region/China'
     #     print('Crawling', start_url)
     #     html = get_page(start_url)
     #     if html:
     #         doc = pq(html)
     #         lines = doc('div[name="list_proxy_ip"]').items()
     #         for line in lines:
     #             ip = line.find('.tbBottomLine:nth-child(1)').text()
     #             port = line.find('.tbBottomLine:nth-child(2)').text()
     #             yield ':'.join([ip, port])