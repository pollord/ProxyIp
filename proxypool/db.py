import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re

from .logger_proxy import MyLogger
logger = MyLogger.get_logger(name='db')


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        decode_responses=True,写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        例子：不加，结果前多一个b，    b'hello world'
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    # INITIAL_SCORE = 10 间接比较值大小
    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        # ZADD key score member [[score member] [score member] ...] 将一个或多个member元素及其score值加入到有序集key当中。
        # 如果某个member已经是有序集的成员，那么更新这个member的score值，并通过重新插入这个member元素，来保证该member在正确的位置上。
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            logger.info('代理不符合规范,%s丢弃' % proxy)
            return
        # REDIS_KEY = 'proxies'
        # ZSCORE key member返回有序集key中，成员member的score值。如果member元素不是有序集key的成员，或key不存在，返回nil。
        # 返回值：member成员的score值，以字符串形式表示。
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    # MAX_SCORE = 100
    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        # ZRANGEBYSCORE key min max
        # 返回有序集key中，所有score值介于min和max之间(包括等于min或max)的成员。有序集成员按 score 值递增(从小到大)次序排列。
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            # ZRANGE key start stop 返回有序集key中，指定区间内的成员。其中成员的位置按score值递增(从小到大)来排序。
            result = self.db.zrevrange(REDIS_KEY, 10, 100)
            try:
                if len(result):
                    return choice(result)
            except PoolEmptyError as e:
                logger.exception(e)  # 记录异常

    # MIN_SCORE = 0
    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            logger.info('代理%s, 当前分数%d减50' % (proxy, score))
            # ZINCRBY key increment member为有序集key的成员member的score值加上增量increment。可以通过传递一个负数值increment，
            # 让score减去相应的值，比如ZINCRBY key member -5 ，就是让member的score值减去5。
            return self.db.zincrby(REDIS_KEY, proxy, -50)
        else:
            logger.info('代理%s, 当前分数%d移除' % (proxy, score))
            # ZREM key member [member ...] 移除有序集key中的一个或多个成员，不存在的成员将被忽略。
            return self.db.zrem(REDIS_KEY, proxy)
    
    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    # MAX_SCORE = 100
    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        logger.info('代理%s可用，设置为%d' % (proxy, MAX_SCORE))
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
    
    def count(self):
        """
        获取数量
        :return: 数量
        """
        # ZCARD key 返回有序集key的基数
        return self.db.zcard(REDIS_KEY)
    
    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
    
    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        # ZREVRANGE key start stop 返回有序集key中，指定区间内的成员。其中成员的位置按score值递减(从大到小)来排列。
        # 除了成员按score值递减的次序排列这一点外， ZREVRANGE命令的其他方面和ZRANGE命令一样。
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)
