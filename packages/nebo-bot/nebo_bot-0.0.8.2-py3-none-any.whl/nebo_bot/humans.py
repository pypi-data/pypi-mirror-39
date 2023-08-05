from nebo_bot.result_codes import ALL_SET_TO_WORK, HOTEL_EMPTY
from nebo_bot.utils import timeout


class Humans:
    _timeout_set_to_work_on_new_floors = 300

    def __init__(self, bot_core):
        self.bot = bot_core

    @timeout()
    def set_to_work_on_new_floors(self):
        if self.bot.now_humans_in_hotel == -1:
            return HOTEL_EMPTY
        while True:
            self.bot.get('floors/0/6')
            if not self.bot.press(text='Найти работника', href='../../humans/floor/'):
                return ALL_SET_TO_WORK
            elif self.bot.get_bs.find(text='Список пуст'):
                return HOTEL_EMPTY
            self.bot.press(text='принять на работу', href='humans:0:humanPanel:selectForWorkLink::ILinkListener::')
            if self.bot.get_bs.find('span', class_='feedbackPanelERROR'):
                return HOTEL_EMPTY
            self.bot.handler_send_message.set_to_work_human(self, self.bot.user_id)
