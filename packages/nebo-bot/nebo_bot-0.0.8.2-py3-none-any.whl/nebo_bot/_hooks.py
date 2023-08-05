import re


def get_lvl(instance):
    try:
        lvl = int(instance.get_bs.find('span', class_='user'). \
                  find_next('img', src=re.compile('/images/icons/star.png')). \
                  find_next('span', text=re.compile('\d+')).text)
        instance.lvl = lvl
    except (IndexError, AttributeError, ValueError):
        pass
    return instance.lvl


def exists_visitors_in_lift(instance):
    if not _in_main_page(instance):
        return
    try:
        visitors = instance.get_bs.find(text=re.compile('0. Вестибюль')).parent.parent.find(class_='rs small').text
        instance.visitors = int(visitors)
    except AttributeError:
        pass


def get_interface(instance):
    try:
        interface = int(re.findall('interface=:(\d+):', instance.get_bs
                                   .find(href=re.compile('interface=:\d+:')).attrs['href'])[0])
        instance.interface = interface + 1
    except (IndexError, AttributeError):
        pass
    return instance.interface


def get_money_new_floor(instance):
    if not _in_main_page(instance):
        return
    try:

        money = int(instance.get_bs.find(text='Построить за ').
                    parent.parent.find('span').next.next.next.span.text.replace("'", ''))
        if instance.get_bs.find('a', href=re.compile('buyNewFloorPanel:buyNewFloorIronLink:link::ILinkListener::')):
            instance.new_floor = 'money'
        else:
            instance.new_floor = 'dollar'
        instance.cost_new_floor = money
    except AttributeError:
        pass


def _in_main_page(instance):
    if 'Небоскребы: онлайн игра' not in instance.get_bs.title:
        return False
    return True


def is_need_to_set_to_work_floors(instance):
    if not _in_main_page(instance):
        return
    if instance.get_bs.find('a', href='floors/0/6'):
        instance.exists_set_to_work_floors = True


def count_human_in_hotel(instance):
    if not _in_main_page(instance):
        return
    hotel_element = instance.get_bs.find('span', text='1. Гостиница')
    hotel_element = hotel_element.parent.find_all('span')
    hotel_size, now_humans_in = int(hotel_element[-2].text), int(hotel_element[-1].text)
    instance.hotel_size = hotel_size
    instance.now_humans_in_hotel = now_humans_in


def small_check_values(instance):
    if _in_main_page(instance):
        if instance.get_bs.find('a', text='Начать строительство'):
            instance.exists_empty_build_floor = True
