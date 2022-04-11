from datetime import datetime


def get_ts_from_time_str(time_str: str):
    # STring format: '2022-04-05T11:30:56.93289351+02:00'; remove .93289351
    _list = time_str.split('.')
    _time_str = f'{_list[0]}+{_list[1].split("+")[1]}'
    return int(datetime.strptime(_time_str, '%Y-%m-%dT%H:%M:%S%z').timestamp())


def format_list_to_str(_list: list):
    # TODO check if '-character needs to be removed from string:
    # "['hello', 'world']" or "[hello, world]"
    return str(_list).replace('\'', '')
