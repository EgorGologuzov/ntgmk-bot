import sqlite3
from source import lists


class Database:
    def __init__(self):
        self.__conn = sqlite3.connect("source/users.db", check_same_thread=False)
        self.__cursor = self.__conn.cursor()

    def get_user_target(self, key: tuple[str, str]):
        return self.__cursor.execute("SELECT Target FROM `Users` WHERE Id = ? AND Service = ?", key).fetchone()[0]

    def add_user_if_not_in(self, key: tuple[str, str]):
        if self.__cursor.execute("SELECT * FROM `Users` WHERE Id = ? AND Service = ?", key).fetchone() is None:
            self.__cursor.execute("INSERT INTO `Users` (Id, Service) VALUES (?, ?)", key)
            self.__conn.commit()

    def update_user_target(self, key: tuple[str, str], new_target: str):
        self.__cursor.execute("UPDATE `Users` SET Target = ? WHERE Id = ? AND Service = ?", (new_target, key[0], key[1]))
        self.__conn.commit()

    def update_target_if_it_is_none(self, key: tuple[str, str], new_target):
        if not self.get_user_target(key):
            self.update_user_target(key, new_target)

    def write_complaint(self, key, text: str):
        self.__cursor.execute("INSERT INTO `Complaints` (Id, Service, Text) VALUES (?, ?, ?)", (key[0], key[1], text))
        self.__conn.commit()

    def user_is_subscribe(self, key):
        return self.__cursor.execute("SELECT Subscribe FROM `Users` WHERE Id = ? AND Service = ?", key).fetchone()[0]

    def update_user_subscribe(self, key, subscribe: bool):
        self.__cursor.execute("UPDATE `Users` SET Subscribe = ? WHERE Id = ? AND Service = ?", (subscribe, key[0], key[1]))
        self.__conn.commit()

    def add_new_student_if_not_in(self, key):
        if not self.__cursor.execute("SELECT * FROM `Students` WHERE Id = ? AND Service = ?", key).fetchall():
            self.__cursor.execute("INSERT INTO `Students` (Id, Service) VALUES (?, ?)", key)
            self.__conn.commit()

    def get_student_name_group_phone_email(self, key: tuple[str, str]):
        self.add_new_student_if_not_in(key)
        return self.__cursor.execute(
            "SELECT Name, [Group], Phone, Email FROM `Students` WHERE Id = ? AND Service = ?", key
        ).fetchall()[0]

    def write_student_data_and_order(self, key, name, group, phone, email, order, period):
        self.add_new_student_if_not_in(key)
        self.__cursor.execute(
            "UPDATE `Students` SET Name = ?, [Group] = ?, Phone = ?, Email = ? WHERE Id = ? AND Service = ?",
            (name, group, phone, email, key[0], key[1])
        )
        self.__cursor.execute("INSERT INTO `Orders` VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                              (key[0], key[1], name, group, phone, email, order, period))
        self.__conn.commit()

    def clear_all_student_data(self, key):
        self.__cursor.execute(
            "UPDATE `Students` SET Name = NULL, [Group] = NULL, Phone = NULL, Email = NULL WHERE Id = ? AND Service = ?",
            key
        )
        self.__conn.commit()

    def select_subscribed_users(self, target, service):
        return self.__cursor.execute(
            "SELECT Id FROM `Users` WHERE Target = ? AND Service = ? AND Subscribe = 1",
            (target, service)
        ).fetchall()


class TimetableDB:
    def __init__(self):
        self.__conn = sqlite3.connect("source/timetable.db", check_same_thread=False)
        self.__cursor = self.__conn.cursor()

    def create_table_if_not_exists(self, date):
        self.__cursor.execute(
            f"CREATE TABLE IF NOT EXISTS [{date}]("
            "[Group] VARCHAR(6),"
            "Lesson VARCHAR(1),"
            "Subgroup VARCHAR(1),"
            "Discipline VARCHAR(35),"
            "Teacher VARCHAR(30),"
            "Audithorium VARCHAR(5)"
            ");"
        )
        self.__conn.commit()

    def select_timetable(self, date):
        return self.__cursor.execute(f"SELECT * FROM `{date}`").fetchall()

    def select_timetable_by_target(self, target, date):
        target = target.lower()
        try:
            result = self.__cursor.execute(f'SELECT * FROM `{date}` WHERE [Group] = ? OR Teacher = ?',
                                           (target, target,)).fetchall()
        except sqlite3.OperationalError:
            return f"Расписания на {date} еще нет :("
        if not result:
            if target in lists.GROUP_LIST:
                return f"В расписании на {date} нет ничего для {lists.GROUP_LIST[target]}."
            else:
                return f"В расписании на {date} нет ничего для {lists.TEACHERS_LIST[target]}."

        if target in lists.GROUP_LIST:
            out = f"Расписание на {date} для {lists.GROUP_LIST[target]}\n"
            for r in result:
                out += f'{r[1]}. {r[3]}{"" if r[2] == " " else f" ({r[2]} пдгр.)"}{"" if r[5] == "" else f" в {r[5]}"}' + '\n'
        else:
            result.sort(key=lambda record: record[1])
            out = f'Расписание на {date} для {lists.TEACHERS_LIST[target]}\n'
            for r in result:
                out += f'{r[1]}. {r[3]} у {lists.GROUP_LIST[r[0]]}{"" if r[2] == " " else f" ({r[2]} пдгр.)"}{"" if r[5] == "" else f" в {r[5]}"}' + '\n'
        return out

    def rewrite_timetable(self, date, new_table):
        self.__cursor.execute(f"DELETE FROM `{date}`")
        for record in new_table:
            self.__cursor.execute(f"INSERT INTO `{date}` VALUES (?, ?, ?, ?, ?, ?)", record)
        self.__conn.commit()


# db = Database()
# print(db.select_subscribed_users("054", "vk"))
# print(db.get_user_target(("1010000101", "vk")))
# db = TimetableDB()
# print(db.select_timetable_by_target("054", "2022-12-02"))

