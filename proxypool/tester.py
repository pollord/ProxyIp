import asyncio
import aiohttp
import time
import sys
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.setting import *

from .logger_proxy import MyLogger
logger = MyLogger.get_logger('tester')


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        # clientSession 客户端，TCPConnector 忽略证书验证
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # encoding
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                logger.info('正在测试%s' % proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=5, allow_redirects=False) as response:
                    # VALID_STATUS_CODES = [200, 302]
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        logger.info('代理可用%s' % proxy)
                    else:
                        self.redis.decrease(proxy)
                        logger.info('请求响应码不合法%s IP%s' % (response.status, proxy))
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                logger.info('代理请求失败%s' % proxy)
    
    def run(self):
        """
        测试主函数
        :return:
        """
        logger.info('测试器开始运行')
        try:
            count = self.redis.count()
            logger.info('当前剩余%d个代理' % count)
            # BATCH_TEST_SIZE = 10
            # In[1]: [i for i in range(0, 100, 10)] Out[2]: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                logger.info('正在测试第%d-%d个代理' % (start + 1, stop))
                test_proxies = self.redis.batch(start, stop)
                # asyncio/wait 协程
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                # 必须注释，否则报RuntimeError: Event loop is closed
                # loop.close()
                # 刷新输出
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            logger.exception('测试器发生错误%s' % e.args)


