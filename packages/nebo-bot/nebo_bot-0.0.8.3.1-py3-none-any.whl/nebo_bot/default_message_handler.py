from nebo_bot.city import Work
from nebo_bot.quest import Quest
from nebo_bot.city import City
from nebo_bot.humans import Humans


class BaseDefaultHandler:

    @staticmethod
    def request_give_post(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def finish_invite(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_exists_in_city(city: City, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def time_expired_wait_post(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_wait_your_invite(city: City, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_canceled(bot: object, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_in_city(city: City, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_cost(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_delivery(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_buy_products(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def lift_visitor_up(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def lift_finished(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def open_new_floor(work: Work, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def set_to_work_human(humans: Humans, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def buy_new_floor(object, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def build_new_floor(object, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def get_award(quest: Quest, user_id: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def update_invite_data(work: Work, user_id: int, task_id: int) -> None:
        raise NotImplementedError()


class DefaultHandler(BaseDefaultHandler):
    @staticmethod
    def update_invite_data(work: Work, user_id: int, task_id: int) -> None:
        pass

    @staticmethod
    def request_give_post(city: City, user_id: int) -> None:
        pass

    @staticmethod
    def finish_invite(city: City, user_id: int) -> None:
        pass

    @staticmethod
    def bot_exists_in_city(city: City, user_id: int) -> None:
        pass

    @staticmethod
    def time_expired_wait_post(city: City, user_id: int) -> None:
        pass

    @staticmethod
    def bot_wait_your_invite(city: City, user_id: int) -> None:
        pass

    @staticmethod
    def bot_canceled(bot: object, user_id: int) -> None:
        pass

    @staticmethod
    def bot_in_city(city: City, user_id: int) -> None:
        pass

    @staticmethod
    def finished_get_cost(work: Work, user_id: int) -> None:
        pass

    @staticmethod
    def finished_get_delivery(work: Work, user_id: int) -> None:
        pass

    @staticmethod
    def finished_get_buy_products(work: Work, user_id: int) -> None:
        pass

    @staticmethod
    def lift_visitor_up(work: Work, user_id: int) -> None:
        pass

    @staticmethod
    def lift_finished(work: Work, user_id: int) -> None:
        pass

    @staticmethod
    def open_new_floor(work: Work, user_id: int) -> None:
        pass

    @staticmethod
    def set_to_work_human(humans: Humans, user_id: int) -> None:
        pass

    @staticmethod
    def buy_new_floor(object, user_id: int) -> None:
        pass

    @staticmethod
    def build_new_floor(object, user_id: int) -> None:
        pass

    @staticmethod
    def get_award(quest: Quest, user_id: int) -> None:
        pass