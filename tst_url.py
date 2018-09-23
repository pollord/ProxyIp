import requests
import re
import json
from lxml import etree
import time
from pyquery import PyQuery as pq


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}


# def crawl_daili66(page_count=1):
#     """
#     获取代理66
#     :param page_count: 页码
#     :return: 代理
#     """
#     start_url = 'http://www.66ip.cn/{}.html'
#     urls = [start_url.format(page) for page in range(1, page_count + 1)]
#     for url in urls:
#         print('Crawling', url)
#         html = requests.get(url, headers=headers).text
#         if html:
#             doc = pq(html)
#             trs = doc('.containerbox table tr:gt(0)').items()
#             for tr in trs:
#                 ip = tr.find('td:nth-child(1)').text()
#                 port = tr.find('td:nth-child(2)').text()
#                 print(':'.join([ip, port]))


# def crawl_goubanjia():
#     """
#     获取Goubanjia
#     :return: 代理
#     """
#     start_url = 'http://www.goubanjia.com'
#     html = requests.get(start_url, headers=headers).text
#     if html:
#         pattern = re.compile('<tr class="success">\s*<td class="ip">\s*<p.*?<span>(.*?)</span>.*?<div style="display: inline-block;">(.*?)</div>\s*'
#                              '<div style="display: inline-block;">(.*?)</div>\s*<p style="display:none;">(.*?)</p>\s*'
#                              '<span>(.*?)</span>\s*<span style="display:inline-block;">(.*?)</span>\s*<span>(.*?)</span>'
#                              '.*?<span style="display:inline-block;">(.*?)</span>\s*<span style="display:inline-block;">'
#                              '(.*?)</span>\s*"(.*?)"\s*<span class="port GEGEA">(.*?)</span>\s*</td>')
#
#         ip_port = pattern.findall(html)
#         print(ip_port)


# def crawl_ip181():
#     start_url = 'http://www.ip181.com/'
#     html = requests.get(start_url, headers=headers).text
#     data = json.loads(html)
#     # print(type(data))
#     re_ip_address = data['RESULT']
#     # print(re_ip_address)
#     for address in re_ip_address:
#         ip = address['ip']
#         port = address['port']
#         result = ip + ':' + port
#         print(result.replace(' ', ''))

# def crawl_ip3366():
#     for page in range(1, 4):
#         start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
#         html = requests.get(start_url, headers=headers).text
#         ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
#         # \s * 匹配空格，起到换行作用
#         re_ip_address = ip_address.findall(html)
#         for address, port in re_ip_address:
#             result = address + ':' + port
#             print(result.replace(' ', ''))

# def crawl_kxdaili():
#     for i in range(1, 2):
#         start_url = 'http://ip.kxdaili.com/dailiip/1/{}.html#ip'.format(i)
#         html = requests.get(start_url, headers=headers).text
#         ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
#         # \s* 匹配空格，起到换行作用
#         re_ip_address = ip_address.findall(html)
#         for address, port in re_ip_address:
#             result = address + ':' + port
#             print(result.replace(' ', ''))

# def crawl_kuaidaili():
#     for i in range(1, 4):
#         start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
#         html = requests.get(start_url, headers=headers).text
#         if html:
#             ip_address = re.compile('<td data-title="IP">(.*?)</td>')
#             re_ip_address = ip_address.findall(html)
#             port = re.compile('<td data-title="PORT">(.*?)</td>')
#             re_port = port.findall(html)
#             for address, port in zip(re_ip_address, re_port):
#                 address_port = address + ':' + port
#                 print(address_port.replace(' ', ''))

# def crawl_xicidaili():
#     for i in range(1, 3):
#         start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
#         html = requests.get(start_url, headers=headers).text
#         if html:
#             find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
#             trs = find_trs.findall(html)
#             for tr in trs:
#                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
#                 re_ip_address = find_ip.findall(tr)
#                 find_port = re.compile('<td>(\d+)</td>')
#                 re_port = find_port.findall(tr)
#                 for address, port in zip(re_ip_address, re_port):
#                     address_port = address + ':' + port
#                     print(address_port.replace(' ', ''))

# def crawl_ip3366():
#     for i in range(1, 4):
#         start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
#         html = requests.get(start_url, headers=headers).text
#         if html:
#             find_tr = re.compile('<tr>(.*?)</tr>', re.S)
#             trs = find_tr.findall(html)
#             for s in range(1, len(trs)):
#                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
#                 re_ip_address = find_ip.findall(trs[s])
#                 find_port = re.compile('<td>(\d+)</td>')
#                 re_port = find_port.findall(trs[s])
#                 for address, port in zip(re_ip_address, re_port):
#                     address_port = address + ':' + port
#                     print(address_port.replace(' ', ''))

# def crawl_89ip():
#     for i in range(1, 3):
#         start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
#         html = requests.get(start_url, headers=headers).text
#         if html:
#             selector = etree.HTML(html)
#             address_content = selector.xpath('//div[@class="layui-col-md8"]/div//table[@class="layui-table"]/tbody/tr')
#             # print(address_content)
#             for item in address_content:
#                 ip = item.xpath('./td[1]/text()')[0].strip()
#                 port = item.xpath('./td[2]/text()')[0].strip()
#                 print((ip + ':' + port).replace(' ', ''))

# def crawl_data5u():
#     start_url = 'http://www.data5u.com/free/gngn/index.shtml'
#     html = requests.get(start_url, headers=headers).text
#     if html:
#         ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
#         re_ip_address = ip_address.findall(html)
#         for address, port in re_ip_address:
#             result = address + ':' + port
#             print(result.replace(' ', ''))

if __name__ == "__main__":
    # crawl_daili66()
    # crawl_goubanjia()
    # crawl_ip181()
    # crawl_ip3366()
    # crawl_kxdaili()
    # crawl_kuaidaili()
    # crawl_xicidaili()
    # crawl_ip3366()
    # crawl_89ip()
    # crawl_data5u()