from typing import Dict

import requests


class SWToolz:
    """
    Класс для удобного получения данных и управления оборудованием через сервис SWToolz-Core_.

    Пример использования::

        swt = SWToolz(swtoolz_url, swtoolz_user, swtoolz_community_number, swtoolz_port)
        swt.change_port_admin_state(device_ip, port_num, 'enabled')

    .. _SWToolz-Core: http://wiki.powernet.com.ru/services/swtoolz-core?s[]=swtoolz
    """

    def __init__(self, url: str, user: str, community_number: int, port: int = 7377, timeout: float = 2.0):
        """
        Начальная инициализация - установка основных полей, формирование шаблона URL для выполнения запросов.

        :param str url: url сервиса SWToolz-Core
        :param str user: логин пользователя в сервисе
        :param int community_number: номер комьюнити для выполнения команд
        :param int port: порт, на котором слушает сервис (по-умолчанию 7377)
        :param float timeout: таймаут для выполнения всех операций
        """

        self.server_url = url
        self.user = user
        self.community_number = community_number
        self.service_port = port
        self.timeout = timeout

        # Т.к. SWToolz-Core принимает параметры запроса не как GET-параметры, а парсит URL, то для удобства
        # использования используем шаблон для формирования конечного URL, куда впоследствии будут подставляться
        # ip-адрес устройства и команда.
        self.request_url_template = f'{self.server_url}:{self.service_port}/{self.user}/{{device_ip}}/' \
            f'{self.community_number}/{{command}}'

    # TODO: сделать какой-то wrapper для запросов к SWToolz-Core, что бы нормально распозновать ошибки
    def change_port_admin_state(self, device_ip: str, port_num: int, target_state: str) -> bool:
        """
        Изменяет административное состояние порта, т.е. включает его или выключает в зависимости от переданного
        `target_state`.

        :param str device_ip: ip-адрес коммутатора
        :param int port_num: номер порта коммутатора
        :param str target_state: целевое состояние порта включен/выключен (принимает строки 'enabled' и 'disabled')
        :rtype: bool
        :return: успешность выполнения команды
        """

        # К сожалению, API SWToolz-Core не очень удобен. Поэтому чтобы понять какой числовой код нужно слать сервису
        # чтобы включить или выключить порт нужно сначала спросить "словарь соответствия" AdminStatus. Сделано это так,
        # потому что на всех устройствах разные SNMP индексы для состояний.
        admin_status_dict: Dict = {}  # словарь соответсвия административных состояний и их кодов
        # подставляем в шаблон URL команду и ip-адрес устройства
        admin_status_url = self.request_url_template.format(device_ip=device_ip, command='AdminStatus')
        admin_status_response = requests.get(admin_status_url, timeout=self.timeout)
        if admin_status_response.status_code == requests.codes.ok:
            # заполняем словарь соответсвия (меняем ключ и значение местами)
            for code, name in admin_status_response.json()['response']['data']['AdminStatus'].items():
                admin_status_dict[name] = code
        else:
            return False

        # Для того, что бы включить/выключить порт нужно послать SWToolz-Core команду
        # set_AdminStatus/{номер порта}/{код нужного административного состояния}
        try:
            command_url_part = f'set_AdminStatus/{port_num}/{admin_status_dict[target_state]}'
        except KeyError:
            # неправильно передан target_state
            return False
        # подставляем в шаблон URL команду и ip-адрес устройства
        change_state_url = self.request_url_template.format(device_ip=device_ip, command=command_url_part)
        change_state_response = requests.get(change_state_url, timeout=self.timeout)
        if change_state_response.status_code == requests.codes.ok:
            # проверяем выполнилась ли команда
            # такое может произойти если, например, неправильно указан индекс SNMP community, ответ придет с нормальным
            # HTTP-кодом, а команда выполнена не будет
            if change_state_response.json()['response']['data']['set_AdminStatus'] == 1:
                return True

        return False

    def get_port_admin_state(self, device_ip: str, port_num: int, media: str = 'copper') -> str:
        """
        Возвращает административное состояние порта.

        :param str device_ip: ip-адрес коммутатора
        :param int port_num: номер порта коммутатора
        :param str media: тип среды ('copper'/'fiber'), по-умолчанию - "медь"
        :rtype str:
        :return: административное состояние ('enabled'/'disabled')
        """

        # TODO: убрать повторение запроса словаря с административным статусом
        # К сожалению, API SWToolz-Core не очень удобен. Поэтому чтобы понять какой числовой код какому типу среды или
        # административному состоянию соответствует, нужно сначала спросить "словари соответствия" AdminStatus и
        # MediumType. Сделано это так, потому что на всех устройствах разные SNMP индексы для состояний.
        admin_status_dict: Dict = {}  # словарь соответсвия административных состояний и их кодов
        medium_type_dict: Dict = {}  # словарь соответсвтия типов среды
        # подставляем в шаблон URL команду и ip-адрес устройства
        dicts_url = self.request_url_template.format(device_ip=device_ip, command='AdminStatus+/MediumType')
        dicts_response = requests.get(dicts_url, timeout=self.timeout)
        if dicts_response.status_code == requests.codes.ok:
            # заполняем словари соответсвия (меняем ключ и значение местами)
            admin_status_dict = dicts_response.json()['response']['data']['AdminStatus']
            for code, name in dicts_response.json()['response']['data']['MediumType'].items():
                medium_type_dict[name] = code
        else:
            return ''

        # Для того, что бы узнасть администартивное состояние порта нужно послать SWToolz-Core команду
        # get_SinglePort/{номер порта}, тем самым узнав всю информацию об этом порту. А потом уже оттуда выбрать, то
        # что нужно.
        command_url_part = f'get_SinglePort/{port_num}'
        # подставляем в шаблон URL команду и ip-адрес устройства
        get_admin_state_url = self.request_url_template.format(device_ip=device_ip, command=command_url_part)
        get_admin_state_response = requests.get(get_admin_state_url, timeout=self.timeout)
        if get_admin_state_response.status_code == requests.codes.ok:
            try:
                status_code = get_admin_state_response.json()['response']['data']['AdminStatus'][
                    f'{port_num}.{medium_type_dict[media]}']
                return admin_status_dict[status_code]
            except IndexError:
                return ''
