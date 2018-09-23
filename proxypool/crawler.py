import json
import re
from .utils import get_page
from pyquery import PyQuery as pq
from lxml import etree

from .logger_proxy import MyLogger
logger = MyLogger.get_logger('crawler')


class ProxyMetaclass(type):
    """
    定义元类
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        # return super(ProxyMetaclass, cls).__new__(cls, name, bases, attrs)
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """
    metaclas取自定的元类。
    第一：元类的attrs参数，收录自定义类的所有属性。
    第二：我们自定义的这个proxy mataclass，的attrs属性，额外添加了两个属性，一个是’__crawlfunc__'属性，其对应的值为列表，用来存储包含crawl_字段的所有属性名称。
          另一个额外的属性是"__crawlcount__",对应的值，存储了crawlfunc属性的个数。
    """

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            logger.info('成功获取到代理%s' % proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            logger.info('Crawling%s' % url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        data = json.loads(html)
        # print(type(data)) dict
        re_ip_address = data['RESULT']
        for address in re_ip_address:
            ip = address['ip']
            port = address['port']
            result = ip + ':' + port
            yield result.replace(' ', '')

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':' + port
                yield result.replace(' ', '')

    def crawl_kxdaili(self):
        for i in range(1, 11):
            start_url = 'http://ip.kxdaili.com/dailiip/1/{}.html#ip'.format(i)
            html = get_page(start_url)
            ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>') 
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            html = get_page(start_url)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>') 
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ', '')
    
    def crawl_ip3366(self):
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')

    def crawl_89ip(self):
        for i in range(1, 3):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            if html:
                selector = etree.HTML(html)
                address_content = selector.xpath(
                    '//div[@class="layui-col-md8"]/div//table[@class="layui-table"]/tbody/tr')
                for item in address_content:
                    ip = item.xpath('./td[1]/text()')[0].strip()
                    port = item.xpath('./td[2]/text()')[0].strip()
                    yield (ip + ':' + port).replace(' ', '')

    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')
