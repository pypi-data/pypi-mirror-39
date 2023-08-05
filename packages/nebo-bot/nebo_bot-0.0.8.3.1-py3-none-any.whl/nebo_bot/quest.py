from nebo_bot.result_codes import GET_AWARD, EMPTY_AWARD


class Quest:

    def __init__(self, bot_core):
        self.bot = bot_core

    def give_awards(self):
        self.bot.get('quests')
        if self.bot.press(text='Получить награду!', href='quest:getAwarLink::ILinkListener::'):
            self.bot.handler_send_message.get_award(self, self.bot.user_id)
            return GET_AWARD
        return EMPTY_AWARD
