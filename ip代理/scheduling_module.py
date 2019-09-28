import time

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

from multiprocessing import Process
from ip代理.api import app
from ip代理.detection_module import Tester
from ip代理.test import Getter

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        '''
        定时测试代理
        '''
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        '''
        定时获取代理
        '''
        getter = Getter()
        while True:
            print('开始获取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启api
        '''
        app.run()

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if TESTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if TESTER_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == '__main__':
    s =Scheduler()
    s.run()