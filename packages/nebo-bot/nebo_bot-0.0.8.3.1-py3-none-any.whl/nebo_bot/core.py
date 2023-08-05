import logging
import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import requests

from nebo_bot.humans import Humans
from nebo_bot.default_message_handler import DefaultHandler
from nebo_bot.quest import Quest
from nebo_bot.result_codes import DOES_NOT_EMPTY_BUILDING_FOR_BUILD, BUILD_NEW_FLOOR, NOT_BUILD, NOT_BUY_BUILD
from nebo_bot.city import City
from nebo_bot._hooks import get_lvl, exists_visitors_in_lift, get_interface, get_money_new_floor, \
    is_need_to_set_to_work_floors, count_human_in_hotel, small_check_values
from nebo_bot.work import Work
from nebo_bot.utils import timeout, StopBot


class BotCore(object):

    nebo_url = 'http://nebo.mobi'
    hooks = [get_interface, get_lvl, exists_visitors_in_lift, get_money_new_floor, is_need_to_set_to_work_floors,
             count_human_in_hotel, small_check_values]

    def __init__(self, handler_send_message=None, debug=False,
                 stop_signal_handler=lambda _: False, user_id=None, task_id=None):
        logging.basicConfig(level=logging.DEBUG if debug is True else logging.INFO)
        self.logging = logging
        self.stop_signal_handler = stop_signal_handler
        self.handler_send_message = handler_send_message if handler_send_message else DefaultHandler()
        self.user_id = user_id
        self.task_id = task_id
        self.last_request = None
        self.stop_bot = False
        self.interface = 0
        self.lvl = -1
        self.visitors = -1
        self.need_get_costs = -1
        self.cost_new_floor = -1
        self.new_floor = 'None'
        self.need_get_delivery = -1
        self.need_get_buy_products = -1
        self.exists_set_to_work_floors = -1
        self.exists_empty_build_floor = -1
        self.now_humans_in_hotel = -1
        self.hotel_size = -1
        self.count_click = 0
        self.fast_click = 0
        self.session = requests.session()
        self._count_iter_stop_handler = 0
        self.bot_login = ''
        self.iter_check_stop_handler = 5
        self.city = City(self)
        self.work = Work(self)
        self.humans = Humans(self)
        self.quest = Quest(self)

    def login(self, login, password):
        self.bot_login = login
        return self._login(login, password)

    @property
    def stop(self):
        if self._count_iter_stop_handler >= self.iter_check_stop_handler:
            self._count_iter_stop_handler = 0
            if self.stop_signal_handler(self.user_id):
                return True
        self._count_iter_stop_handler += 1

    @property
    def get_bs(self):
        return BeautifulSoup(self.last_request.text, 'html.parser')

    @timeout()
    def request(self, method, url, **kwargs):
        if self.stop:
            raise StopBot()
        self.count_click += 1
        time.sleep(0.80)
        self.last_request = getattr(self.session, method)(self.join_url(url), **kwargs)
        bs = self.get_bs
        if bs.title and 'слишком быстро' in bs.title.text.lower():
            self.fast_click += 1
            time.sleep(10)
            self.request(method, url, **kwargs)
        self._run_hooks()
        return self.get_bs

    def _run_hooks(self):
        for _hook in self.hooks:
            _hook(self)

    def get(self, url):
        return self.request('get', url)

    def set_form(self, url, data):
        return self.request('post', url, data=data, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _login(self, login, password):
        self.request('get', 'login')
        bs = self.get_bs
        action = bs.form['action']
        bs = self.request('post',
                          action,
                          data={
                              'id1_hf_0': '',
                              'login': login,
                              'password': password,
                          })
        user_css = bs.find_all('span', class_='user')
        if user_css:
            if login.lower() in user_css[-1].text.lower():
                return True
        return False

    def join_url(self, url):
        return urljoin(self.nebo_url, url)

    @timeout()
    def press(self, text=None, href=None):
        if text and href:
            link = self.get_bs.find('a', href=re.compile(href), text=re.compile(text, re.IGNORECASE))
        elif text:
            link = self.get_bs.find('a', text=re.compile(text, re.IGNORECASE))
        else:
            link = self.get_bs.find('a', href=re.compile(href, re.IGNORECASE))

        if link:
            link = link.attrs.get('href', None)
            if link:
                return self.get(link)

    def _build_floor(self):
        for floor_name in ['Электроника', 'Мода', 'Продукты', 'Услуги', 'Отдых']:
            if self.press(href=':floorLink1::ILinkListener::', text=floor_name):
                self.handler_send_message.build_new_floor(self, self.user_id)
                return BUILD_NEW_FLOOR
        return NOT_BUILD

    def build_empty_building(self):
        if self.exists_empty_build_floor:
            if self.press(text='Начать строительство'):
                return self._build_floor()
        return DOES_NOT_EMPTY_BUILDING_FOR_BUILD

    def buy_floor(self):
        if not self.new_floor == 'None':
            if self.press(href=':buyNewFloorPanel:buyNewFloor'):
                if self.press(text='Да, подтверждаю'):
                    self.handler_send_message.buy_new_floor(self, self.user_id)
                    return self._build_floor()
        return NOT_BUY_BUILD

    def buy_floors(self):
        while True:
            if self.buy_floor() in [NOT_BUY_BUILD, NOT_BUILD]:
                break

    def run_works(self):
        self.buy_floors()
        self.work.run()
        self.quest.give_awards()


if __name__ == '__main__':
    def stop_signal():
        pass

    bot = BotCore(stop_signal=stop_signal)
    bot.login('miik chocolate', 'mm1998mm')