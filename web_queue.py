# created by @Heroku & @YongchaoHuang on 24/03/2020

import requests # pip install requests
from fake_headers import Headers  # pip install fake_headers
from multiprocessing.dummy import Pool
import datetime
import time
import logging
import os


class web_Queue(str):
    _instance = None

    def __init__(self,web_url=None):
        if web_url is None:
            print("pls provide web url")
        else:
            self.session_bags = []
            self.session_limit = os.environ.get('session_limit', 100)
            self.pool_size = 2
            self.refresh_interval = os.environ.get('refresh_interval', 60)
            self.new_session_interval = os.environ.get('new_session_interval', 600)
            self.url = web_url
            global url
            url=self.url
            print("url=",url)

    @staticmethod
    def GetInstance(url):
        if web_Queue._instance is None:
            web_Queue._instance = web_Queue(url)
        return web_Queue._instance

    def run_queue(self):
        logging.info("start queue ocado")
        funcs = []
        funcs.append({'func': self.add_new_session, 'interval': self.new_session_interval})
        funcs.append({'func': self.refresh_session_bags, 'interval': self.refresh_interval})
        with Pool(len(funcs)) as p:
            pool_requests = p.imap_unordered(
                web_Queue.cron, funcs)
            results = [r for r in pool_requests if r]
            return "finished" + str(results)

    def refresh_session_bags(self):
        with Pool(self.pool_size) as p:
            pool_requests = p.imap_unordered(
                self.refresh_session, self.session_bags)
            results = [r for r in pool_requests if r]
            return results

    def refresh_session(self, session_bag):
        res = session_bag['session'].get(
            self.url, headers=session_bag['header'], timeout=5)
        session_bag['position'] = res.text
        session_bag['queue_key'] = res.cookies.get_dict()
        session_bag['updated_time'] = datetime.datetime.now()
        logging.info("updated session: " + str(session_bag))
        logging.info('updated session/ your current position is: %s (refreshing every 1 minute). to open the website: %s?tdtoken=%s', str(session_bag['position']), str(url), str(session_bag['queue_key']['aluid']))
        posiStr=str(session_bag['position'])
        # print(posiStr)
        # posi_index = posiStr.find(" %s " % "QueuePosition"+": ")
        first="QueuePosition"
        last="QueueLength"
        start = posiStr.index(first) + len(first)
        end = posiStr.index(last, start)
        current_posi=int(posiStr[start+2:end-3])
        tol_pop=int(posiStr[end+14:len(posiStr)-2])
        if current_posi<=100:
            print("Reminder from Heroku & Yongchao: stop drinking beer - you are about to enter the website (there are less than 100 people before you)")
        else:
            print("Keep Calm and Drink Beer, Heroku & Yongchao will remind you once you are within top 100")

    def add_new_session(self):
        bag = {}
        bag['session'] = requests.Session()
        bag['header'] = web_Queue.generate_header()
        bag['start_time'] = datetime.datetime.now()
        # add session to the bags
        self.session_bags.append(bag)
        if len(self.session_bags) > self.session_limit:
            self.session_bags.pop(0)
        logging.info("new session/ " + str(bag))

    @staticmethod
    def generate_header():
        headers = Headers().generate()
        # set headers for ocado
        headers['referer'] = url
        headers['accept-language'] = 'en-US,en;q=0.9'
        headers['accept-encoding'] = 'gzip, deflate, br'
        headers['Sec-Fetch-Dest'] = 'empty'
        headers['Sec-Fetch-Mode'] = 'cors'
        headers['Sec-Fetch-Site'] = 'same-origin'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['x-td-content'] = 'json'
        return headers

    @staticmethod
    def cron(func):
        start = time.time()
        while True:
            func['func']()
            time.sleep(func['interval'] - ((time.time() - start) % func['interval']))
