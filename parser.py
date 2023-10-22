import datetime
import time
from source import lists
from database import TimetableDB
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bots import vk_bot, te_bot
from lib import *


class ParserBot:
    def __call__(self):
        options = Options()
        service = Service(executable_path="source/chromedriver.exe")
        options.headless = True
        options.add_argument('--ignore-certificate-errors')
        browser = Chrome(options=options, service=service)
        db = TimetableDB()

        while True:
            for i in range(3):
                t1 = time.time()
                date = datetime.date.today() + datetime.timedelta(days=i)
                date = date.isoformat()
                browser.get(f"http://ntgmk.ru/program/r_student.php?dt1={date}&dt2={date}")
                time.sleep(5)

                # парсинг новой таблицы
                new_table = []
                rows = browser.find_elements(By.TAG_NAME, 'tr')
                if len(rows) < 3:
                    print(f"Расписание на {date} отсутствует.")
                    continue
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    if len(cells) < 6 or cells[0].text == "Группа":
                        continue
                    new_table.append((
                        cells[0].text.lower(),
                        cells[1].text,
                        cells[2].text,
                        cells[3].text,
                        cells[4].text.lower(),
                        cells[5].text
                    ))

                # сравнение таблиц
                t2 = time.time()
                db.create_table_if_not_exists(date)
                old_table = db.select_timetable(date)
                updated = []
                for group in lists.GROUP_LIST:
                    l1 = list(filter(lambda r: (r[0] == group), old_table))
                    l2 = list(filter(lambda r: (r[0] == group), new_table))
                    if l1 != l2 and len(l2):
                        updated.append(group)
                for teacher in lists.TEACHERS_LIST:
                    l1 = list(filter(lambda r: (r[4] == teacher), old_table))
                    l2 = list(filter(lambda r: (r[4] == teacher), new_table))
                    if l1 != l2 and len(l2):
                        updated.append(teacher)

                # обновление таблицы в БД + вызов методов рассылки
                if len(updated):
                    db.rewrite_timetable(date, new_table)
                    print(f"Таблица {date} обновлена.")
                    print(updated)
                    vk_bot.mailing(updated, date)
                    write_list_and_date_in_file(updated, date)

                print(f"Парсинг таблицы {date} завершен за", int(t2 - t1), "с.")
                print(f"Обработка результата заняла {int(time.time() - t2)} с.")

            time.sleep(120)


pa_bot = ParserBot()

