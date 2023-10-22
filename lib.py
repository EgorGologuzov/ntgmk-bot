import datetime
from source import lists


def read_all_file(path: str):
    with open(path, "r") as f:
        text = f.read()
        f.close()
        return text


def group_in_list(group: str):
    group = group.lower()
    for g in lists.GROUP_LIST:
        if group in g:
            return True
    return False


def find_target(target: str):
    target = target.lower()
    for group in lists.GROUP_LIST:
        if target in group:
            return group
    for teacher in lists.TEACHERS_LIST:
        if target in teacher:
            return teacher
    return None


def upcase_target(target):
    if target in lists.GROUP_LIST:
        return lists.GROUP_LIST[target]
    else:
        return lists.TEACHERS_LIST[target]


def today():
    return datetime.date.today().isoformat()


def next_day():
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    week_day = tomorrow.isoweekday()
    if week_day == 7:
        tomorrow += datetime.timedelta(1)
    elif week_day == 6:
        tomorrow += datetime.timedelta(2)
    return tomorrow.isoformat()


def isoformat_date(date: str):
    if date in ("n", "с"):
        return datetime.date.today().isoformat()
    elif date in ("t", "з"):
        return (datetime.date.today() + datetime.timedelta(1)).isoformat()
    try:
        today = datetime.datetime.today()
        date = date.split(".")
        day = int(date[0])
        month = int(date[1] if len(date) > 1 else today.month)
        year = int(date[2] if len(date) > 2 else today.year)
        return datetime.date(year, month, day).isoformat()
    except ValueError:
        return None


def write_list_and_date_in_file(updated, date):
    with open("config/tmp.txt", "w") as f:
        f.writelines(("|".join(updated), "\n", date))
        f.close()


def read_and_clear_tmp_file():
    f = open("config/tmp.txt", "r")
    updated = f.readline()[:-1]
    date = f.readline()
    if not updated:
        return None, None
    updated = updated.split("|")
    open("config/tmp.txt", "w").close()
    return updated, date


