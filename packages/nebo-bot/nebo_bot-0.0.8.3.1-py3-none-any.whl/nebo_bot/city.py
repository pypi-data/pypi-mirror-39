import re
import time

from nebo_bot.utils import timeout
from nebo_bot.result_codes import *


class City:
    _timeout_go_to_city = 300

    def __init__(self, bot_core):
        self.bot = bot_core
        self.is_in_city = None
        self.current_city_name = ''
        self.city_name = ''
        self.post_in_city = ''
        self.work = Work(self.bot, self)

    def init(self):
        self.check_current_city()
        self.check_post()

    @timeout()
    def go_to_city(self, city_name):
        self.city_name = city_name
        self.check_current_city()
        if re.search(city_name, self.current_city_name, re.IGNORECASE):
            self.bot.handler_send_message.bot_exists_in_city(self, self.bot.user_id)
            return True
        else:
            self.exit_with_city()

        _to_notify_invite = False
        while True:
            if self.bot.get_bs.find('span', text=re.compile(city_name, re.IGNORECASE)):
                self.bot.press(href='notifyPanel:inviteGuildMessage:inviteG'
                                    'uildPanel:acceptLink::ILinkListener', text='принять')
                self.bot.handler_send_message.bot_in_city(self, self.bot.user_id)
                return True
            else:
                if not self.bot.press(href='notifyPanel:inviteGuildMessage:'
                                           'inviteGuildPanel:declineLink::ILinkListener', text='отклонить'):
                    self.bot.get('home')
                if not _to_notify_invite:
                    self.bot.handler_send_message.bot_wait_your_invite(self, self.bot.user_id)
                    _to_notify_invite = True
                time.sleep(2)

    def check_current_city(self):
        self.bot.get('city')
        if 'О городах' in self.bot.get_bs.title:
            self.is_in_city = False
            return True
        self.is_in_city = True
        city_name = self.bot.get_bs.find('span', class_='amount nwr')
        if re.match('\s«\s\D+\s»', city_name.text):
            self.current_city_name = city_name.find('strong').text
            return self.current_city_name
        self.current_city_name = 'NO_CITY'

    def exit_with_city(self):
        self.bot.get('city')
        if 'О городах' in self.bot.get_bs.title:
            return True
        if self.bot.press(href=':leaveLink::ILinkListener', text='Покинуть город'):
            if self.bot.press(text='Да, подтверждаю', href=':confirmLink::ILinkListener::'):
                return True

    def check_post(self):
        my_profile_link = self.bot.get_bs.find(text=re.compile('Мой профиль')).parent.attrs['href']
        self.bot.get(my_profile_link)
        post = self.bot.get_bs.find('span', class_='amount',
                                    text=re.compile(self.current_city_name)).parent.next.next.next.next.text
        self.post_in_city = post


class Work:

    def __init__(self, bot_core, city):
        self._init_timeouts()
        self.bot = bot_core
        self.city = city
        self.accept_to_invite = False
        self.invited_users = []
        self._tmp_count = 0
        self.count_invite = 0
        self.is_run = True

    def _init_timeouts(self):
        self._timeout_run_invite = 900

    def init(self):
        self.city.init()
        self.city.check_post()
        if self.city.post_in_city in ['советник', 'виц-мэр', 'и.о. мэра', 'мэр']:
            self.accept_to_invite = True

    def _wait_give_post(self):
        @timeout(180)
        def foo():
            while True:
                self.city.work.init()
                if self.accept_to_invite:
                    return GAVE_POST
                time.sleep(2)
        try:
            foo()
        except TimeoutError:
            return DOES_NOT_GAVE_POST

    @timeout()
    def run_invite(self, count_invite=50, from_lvl=10, to_lvl=80, from_day=0, to_day=-1):
        """
        MessageHandlers:
            request_give_post - For send message to notify to need give post for nebo_bot
            time_expired_wait_post - Time is expired wait a post

        """
        self.init()
        if not self.accept_to_invite:
            self.bot.handler_send_message.request_give_post(self, self.bot.user_id)
            if self._wait_give_post() == DOES_NOT_GAVE_POST:
                self.bot.handler_send_message.time_expired_wait_post(self, self.bot.user_id)
                return DOES_NOT_GAVE_POST

        if not self.accept_to_invite:
            return PERMISSION_ERROR_FOR_INITE
        while True:
            if not self.is_run:
                self.bot.handler_send_message.bot_canceled(self.bot, self.bot.user_id)
                return CANCEL_INVITING
            if self.count_invite >= count_invite:
                self.bot.handler_send_message.finish_invite(self, self.bot.user_id)
                return SUCCESS_FINISHED_INVITE
            users = self._users_for_invite()
            print(users)
            for user in users:
                self._invite_user(user['link'])
            self.update()
            time.sleep(2)

    def update(self):
        if self.count_invite == self._tmp_count:
            return
        self.bot.handler_send_message.update_invite_data(self, self.bot.user_id, self.bot.task_id)
        self._tmp_count = self.count_invite

    def _invite_user(self, user_link):
        self.bot.get(user_link)
        btn_invite = self.bot.get_bs.find(text=re.compile('Пригласить в город'))
        if btn_invite:
            if user_link in self.invited_users:
                self.bot.logging.debug('+/-')
                return True
            try:
                self.bot.request('get', btn_invite.parent.attrs['href'])
            except KeyError:
                self.count_invite += 1
                self.bot.logging.debug('--')
                return
            if self.bot.get_bs.find(class_='feedbackPanelINFO', text=re.compile('Приглашение отправлено!')):
                self.count_invite += 1
                self.invited_users.append(user_link)
                self.bot.logging.debug('+')
            else:
                self.bot.logging.debug('-')

    def _users_for_invite(self):
        def get_detail_info_user(user):
            user_link = user.attrs['href']
            # lvl = int(self.nebo_bot.get_bs.find('a', href=user_link).parent.parent.find('span', text=re.compile('\d+')).text)
            # try:
            #     day = self.nebo_bot.get_bs.find('a', href=user_link).parent.\
            #         parent.parent.find('span', class_='small minor nshd').text
            #     day_re = re.match('\D+\s(\d+)', day)
            #     if day_re:
            #         day = int(day_re.group(1))
            #     else:
            #         day = -1
            # except AttributeError:
            #     day = -1

            return {
                # 'lvl': lvl,
                'link': user_link,
                # 'day': day
            }
        self.bot.get('online/nocity')
        users = self.bot.get_bs.find_all('a', href=re.compile('../tower/id'))
        if len(users) >= 1:
            users = users[0:-1]
        return [
            {**get_detail_info_user(user)} for user in users
        ]
