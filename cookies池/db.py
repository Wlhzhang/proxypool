import random
import redis

REDIS_HOST = '106.54.224.13'
REDIS_PORT = 6379
REDIS_PASSWORD = 'root123'

class RedisClient:
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''
        初始化redis连接
        '''
        self.db = redis.StrictRedis(host=host, port=port, password=password)
        self.type = type
        self.website = website

    def name(self):
        '''
        获取hash的名称
        :return: hash名称
        '''
        return '{}:{}'.format(self.type, self.website)

    def set(self, username, value):
        '''
        设置键值对
        :param username: 用户名
        :param value:密码或者cookies
        :return:
        '''
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        '''
        根据键获取键值
        :param username: 用户名
        :return:
        '''
        return self.db.hget(self.name(), username)

    def delete(self, username):
        '''
        根据键名删除键值对
        :param username: 用户名
        :return:
        '''
        return self.db.hdel(self.name(), username)

    def count(self):
        '''
        获取数量
        :return: 数量
        '''
        return self.db.hlen(self.name())

    def random(self):
        '''
        随机得到键值对，用于随机cookies的获取
        :return: 随机cookies
        '''
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        '''
        获取所有账户信息
        :return: 所有用户名
        '''
        return self.db.hkeys(self.name())

    def all(self):
        '''
        获取所有键值对
        :return: 用户名和密码或cookies的映射表
        '''
        return self.db.hgetall(self.name())