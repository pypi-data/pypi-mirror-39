import logging
import re

from nebo_bot.result_codes import *
from nebo_bot.utils import timeout


class Work:

    def __init__(self, bot_core):
        self.bot = bot_core
        self.max_timeout = 240

    @timeout(120)
    def get_cost(self):
        self.bot.get('floors/0/5')
        while True:
            if not self.bot.press('Собрать выручку'):
                self.bot.handler_send_message.finished_get_cost(self, self.bot.user_id)
                return FINISHED_GET_COSTS
            logging.debug('Собран выручка')

    @timeout(120)
    def get_delivery(self):
        self.bot.get('floors/0/3')
        while True:
            if not self.bot.press('Выложить товар'):
                self.bot.handler_send_message.finished_get_delivery(self, self.bot.user_id)
                return FINISHED_GET_DELIVERY
            logging.debug('Выложен товар')

    @timeout(200)
    def get_buy_products(self):
        self.bot.get('floors/0/2')
        while True:
            if self.bot.press(text='Закупить товар'):
                if self.bot.press(href='product[ABC]:emptyState:action:link::ILinkListener::'):
                    logging.debug('Куплен товар')
                    continue
            self.bot.handler_send_message.finished_get_buy_products(self, self.bot.user_id)
            return FINISHED_GET_BUY_PRODUCTS

    @timeout(240)
    def lift(self):
        self.bot.get('lift')
        while True:
            if self.bot.press(href='lift/wicket:interface/:\d+:liftState:upLink::ILinkListener::'):
                continue
            if self.bot.press(href='lift/wicket:interface/:\d+:liftState:tipsLink:link::ILinkListener::'):
                logging.debug('Поднят на лифте посетитель')
                self.bot.handler_send_message.lift_visitor_up(self, self.bot.user_id)
                continue
            try:
                if not self.bot.get_bs.find(text=re.compile(' Ждем посетителя!')).parent.attrs.get('class')[0] == 'state':
                    return self.lift()
            except (IndexError, AttributeError):
                pass
            try:
                if self.bot.get_bs.find(text=re.compile(' Новый посетитель!')).parent.attrs.get('class')[0] == 'state':
                    return self.lift()
            except (IndexError, AttributeError):
                pass

            self.bot.handler_send_message.lift_finished(self, self.bot.user_id)
            return FINISHED_LIFT_WORK

    def open_floors(self):
        self.bot.get('home')
        while True:
            if not self.bot.press(text='Открыть этаж!'):
                return OPEN_ALL_NEW_FLOORS
            self.bot.handler_send_message.open_new_floor(self, self.bot.user_id)

    def run_work_products(self):
        self.get_cost()
        self.get_delivery()
        self.get_buy_products()

    def run(self):
        self.open_floors()
        self.bot.humans.set_to_work_on_new_floors()
        self.run_work_products()
        self.lift()
        self.run_work_products()
        return FINISHED_RUN_WORKS




