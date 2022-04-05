from datetime import datetime, timezone


def get_ts_from_time_str(time_str):
    # STring format: '2022-04-05T11:30:56.93289351+02:00'; remove .93289351
    list = time_str.split('.')
    str = f'{list[0]}+{list[1].split("+")[1]}'
    return int(datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z').timestamp())

