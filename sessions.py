import time
import config.templates as answer
import config.commands as command
from message import Message
from database import Database, TimetableDB
from lib import *
from source import lists


class Session:
    def __init__(self, user_id: tuple[str, str]):
        self._user_id: tuple[str, str] = user_id
        self._past_call_time = time.time()
        self._dialog = self._dialog_generator()
        self._past_message: str = ""
        self.is_finished = False

    def _dialog_generator(self):
        pass

    def answer_message(self, message):
        self._past_message = message
        self._past_call_time = time.time()
        return self._dialog.__next__()


class STimetable(Session):
    def _dialog_generator(self):
        db_users = Database()
        message_split = self._past_message.split()[1::]
        target, date = None, None
        if len(message_split) == 2:
            target = find_target(message_split[0])
            date = isoformat_date(message_split[1])
            if target is None:
                self.is_finished = True
                yield Message("Не найдена заданная группа или преподавтель. Проверьте правильность введения данных.",
                              buttons=("!Список груп", "!Список преподавателей"))
            if date is None:
                self.is_finished = True
                yield Message("Неверный формат даты", buttons=("Помощь timetable",))

        elif len(message_split) == 1:
            target = find_target(message_split[0])
            date = next_day()
            if target is None:
                self.is_finished = True
                yield Message("Не найдена заданная группа или преподавтель. Проверьте правильность введения данных.",
                              buttons=("!Список груп", "!Список преподавателей"))

        elif len(message_split) == 0:
            target = db_users.get_user_target(self._user_id)
            date = next_day()
            if target is None:
                yield Message("Введите номер групы или фамилию преподавателя.")
                target = find_target(self._past_message)
                while target is None:
                    yield Message("Не найдена заданная группа или преподавтель. Попробуйте еще раз.",
                                  buttons=("!Список груп", "!Список преподавателей"))
                    target = find_target(self._past_message)
                db_users.update_target_if_it_is_none(self._user_id, target)
        else:
            self.is_finished = True
            yield Message("Ошибка: Команда timetable принимает максимум 2 аргумента.",
                          buttons=("Помощь timetable",))

        db_users.update_target_if_it_is_none(self._user_id, target)

        self.is_finished = True
        db = TimetableDB()
        yield Message(db.select_timetable_by_target(target, date))


class SOrderReference(Session):
    def _dialog_generator(self):
        user_db = Database()
        name, group, phone, email = user_db.get_student_name_group_phone_email(self._user_id)
        if name is not None:
            yield Message(f"Эта справка для {name}?", buttons=("Да", "Нет"))
            while True:
                if self._past_message == "Да":
                    break
                elif self._past_message == "Нет":
                    name, group, phone, email = None, None, None, None
                    break
        if name is None:
            yield Message("Введите свое ФИО")
            while name is None:
                name = self._past_message
                if name.count(" ") != 2:
                    name = None
                    yield Message("ФИО должно состоять из 3 слов")
        if group is None:
            yield Message("Введите свою группу")
            while True:
                group = self._past_message
                if not group_in_list(group):
                    yield Message("Вашей группы нет в списке. Попробуйет еще раз.", buttons=("Список груп",))
                else:
                    break
        if phone is None:
            yield Message("Введите свой телефон")
            phone = self._past_message
        if email is None:
            yield Message("Введите свой EMail")
            email = self._past_message
        yield Message("Выберите тип справки.\n"
                      "1.Справка с места учебы на текущий учебный год\n"
                      "2.Справка с места учебы за весь период обучения\n"
                      "3.Справка для военкомата\n"
                      "4.Справка о доходах студента\n"
                      "5.Справка об обучении (для отчисленных с оценками)\n"
                      "6.Справка о периоде обучения (для обучающихся с оценками)\n"
                      "7.Справка для участия в ЕГЭ (для студентов выпускных груп)\n"
                      "8.Другое",
                      buttons=("1", "2", "3", "4", "!5", "6", "7", "8")
                      )
        order, period = "", None
        while True:
            if self._past_message in "123567":
                order = self._past_message
                break
            elif self._past_message == "4":
                order = self._past_message
                yield Message("Введите период получения доходов (например '2022 год')")
                period = self._past_message
                break
            elif self._past_message == "8":
                yield Message("Введите примерное название документа")
                order = self._past_message
                break
            else:
                yield Message("Бот ожидает нажатия кнопки")
        user_db.write_student_data_and_order(self._user_id, name, group, phone, email, order, period)
        self.is_finished = True
        yield Message("Заявка оформлена. Ее можно забрать спустя 3 рабочих дня в главном корпусе.")


class SHelp(Session):
    def _dialog_generator(self):
        split = self._past_message.split()
        if len(split) == 2:
            com = split[1]
            self.is_finished = True
            if com in command.HELP:
                yield Message(read_all_file("source/help/help.txt"))
            elif com in command.CLEAR:
                yield Message(read_all_file("source/help/clear.txt"))
            elif com in command.ORDER:
                yield Message(read_all_file("source/help/order.txt"))
            elif com in command.SUBSCRIBE:
                yield Message(read_all_file("source/help/subscribe.txt"))
            elif com in command.SUPPORT:
                yield Message(read_all_file("source/help/support.txt"))
            elif com in command.TIMETABLE:
                yield Message(read_all_file("source/help/timetable.txt"))
            elif com in command.MAP:
                yield Message(read_all_file("source/help/map.txt"))
            else:
                yield Message("Такой команды нет", buttons=("Помощь",))
        else:
            self.is_finished = True
            yield Message(read_all_file("source/help/base.txt"))


class SSupport(Session):
    def _dialog_generator(self):
        yield Message("Введите сообщение для техподдержки.", buttons=("Отмена",))
        if self._past_message == "Отмена":
            self.is_finished = True
            yield Message("Действие отменено.")
        while len(self._past_message) > 1500:
            if self._past_message == "Отмена":
                self.is_finished = True
                yield Message("Действие отменено.")
            yield Message("Пожалуйста опишите проблему короче, не более 1500 символов.", buttons=("Отмена",))
        self.is_finished = True
        Database().write_complaint(self._user_id, self._past_message)
        yield Message("Заявка отправлена. Вы получите ответ на неё в этом чате.")


class SSubscribe(Session):
    def _dialog_generator(self):
        db_user = Database()
        if db_user.user_is_subscribe(self._user_id):
            yield Message(f"Вы уже подписаны на {upcase_target(db_user.get_user_target(self._user_id))}.",
                          buttons=("!Отписаться", "!Изменить объект подписки", "!Отмена"))
            while True:
                if self._past_message == "Отписаться":
                    db_user.update_user_subscribe(self._user_id, False)
                    self.is_finished = True
                    yield Message("Подписка отменена")
                elif self._past_message == "Изменить объект подписки":
                    yield Message("Введите номер группы или фамилию преподавателя")
                    target = find_target(self._past_message)
                    while target is None:
                        yield Message("Не найдена заданная группа или преподавтель. Проверьте правильность введения данных.",
                                      buttons=("!Список груп", "!Список преподавателей"))
                        target = find_target(self._past_message)
                    self.is_finished = True
                    db_user.update_user_target(self._user_id, target)
                    yield Message(f"Объект подписки изменен на {upcase_target(target)}")
                elif self._past_message == "Отмена":
                    self.is_finished = True
                    yield Message("Действие отменено")
                else:
                    yield Message("Сделайте выбор нажав кнопку")
        else:
            target = db_user.get_user_target(self._user_id)
            if target is None:
                yield Message("Введите номер группы или фамилию преподавателя")
                target = find_target(self._past_message)
                while target is None:
                    yield Message("Не найдена заданная группа или преподавтель. Попробуйте еще раз.",
                                  buttons=("!Список груп", "!Список преподавателей"))
                    target = find_target(self._past_message)
                db_user.update_user_target(self._user_id, target)
            else:
                yield Message(f"Подписаться на расписание для {upcase_target(target)}?",
                              buttons=("Да", "Изменить объект"))
                if self._past_message == "Изменить объект":
                    yield Message("Введите номер группы или фамилию преподавателя")
                    target = find_target(self._past_message)
                    while target is None:
                        yield Message("Не найдена заданная группа или преподавтель. Попробуйте еще раз.",
                                      buttons=("!Список груп", "!Список преподавателей"))
                        target = find_target(self._past_message)
                    db_user.update_user_target(self._user_id, target)
            db_user.update_user_subscribe(self._user_id, True)
            self.is_finished = True
            yield Message(f"Подписка на {upcase_target(target)} оформлена")


class SClear(Session):
    def _dialog_generator(self):
        yield Message("Вы уверены что хотите очистить свои данные?", buttons=("Да", "Нет"))
        while True:
            if self._past_message == "Да":
                self.is_finished = True
                Database().clear_all_student_data(self._user_id)
                yield Message("Все данные очищены")
            elif self._past_message == "Нет":
                self.is_finished = True
                yield Message("Действие отменено")
            else:
                yield Message("Бот ожидает нажатия кнопки")


class SMap(Session):
    def _dialog_generator(self):
        yield Message("Что вы хотите узнать?",
                      buttons=("!Адреса корпусов", "!Адреса столовых", "!Схемы корпусов"))


class SInformation(Session):
    def _dialog_generator(self):
        pass


class SList(Session):
    def _dialog_generator(self):
        target = self._past_message.split()[1]
        if target == "преподавателей":
            self.is_finished = True
            yield Message(lists.TEXT_TEACHERS_LIST)
        else:
            self.is_finished = True
            yield Message(lists.TEXT_GROUP_LIST)


class SAddresses(Session):
    def _dialog_generator(self):
        target = self._past_message.split()[1]
        if target == "корпусов":
            self.is_finished = True
            yield Message(answer.ADDRESSES["Корпуса"])
        else:
            self.is_finished = True
            yield Message(answer.ADDRESSES["Столовые"])


class SPlans(Session):
    def _dialog_generator(self):
        yield Message("О каком корпусе речь?", buttons=("1й", "2й", "3й", "4й"))
        while True:
            if self._past_message == "1й":
                yield Message("А этаж?", buttons=("1", "2"))
                while True:
                    if self._past_message == "1":
                        self.is_finished = True
                        yield Message("Схема 1 этажа 1 корпуса", image="B1F1")
                    elif self._past_message == "2":
                        self.is_finished = True
                        yield Message("Схема 2 этажа 1 корпуса", image="B1F2")
                    else:
                        yield Message("Я жду пока вы нажмете кнопку...")
            elif self._past_message == "2й":
                yield Message("А этаж?", buttons=("1", "2", "3", "4", "5"))
                while True:
                    if self._past_message == "1":
                        self.is_finished = True
                        yield Message("Схема 1 этажа 2 корпуса", image="B2F1")
                    elif self._past_message == "2":
                        self.is_finished = True
                        yield Message("Схема 2 этажа 2 корпуса", image="B2F2")
                    elif self._past_message == "3":
                        self.is_finished = True
                        yield Message("Схема 3 этажа 2 корпуса", image="B2F3")
                    elif self._past_message == "4":
                        self.is_finished = True
                        yield Message("Схема 4 этажа 2 корпуса", image="B2F4")
                    elif self._past_message == "5":
                        self.is_finished = True
                        yield Message("Схема 5 этажа 2 корпуса", image="B2F5")
                    else:
                        yield Message("Я жду пока вы нажмете кнопку...")
            elif self._past_message == "3й":
                yield Message("А этаж?", buttons=("1", "2", "3"))
                while True:
                    if self._past_message == "1":
                        self.is_finished = True
                        yield Message("Схема 1 этажа 3 корпуса", image="B3F1")
                    elif self._past_message == "2":
                        self.is_finished = True
                        yield Message("Схема 2 этажа 3 корпуса", image="B3F2")
                    elif self._past_message == "3":
                        self.is_finished = True
                        yield Message("Схема 3 этажа 3 корпуса", image="B3F3")
                    else:
                        yield Message("Я жду пока вы нажмете кнопку...")
            elif self._past_message == "4й":
                yield Message("А этаж?", buttons=("1", "2", "3"))
                while True:
                    if self._past_message == "1":
                        self.is_finished = True
                        yield Message("Схема 1 этажа 4 корпуса", image="B4F1")
                    elif self._past_message == "2":
                        self.is_finished = True
                        yield Message("Схема 2 этажа 4 корпуса", image="B4F2")
                    elif self._past_message == "3":
                        self.is_finished = True
                        yield Message("Схема 3 этажа 4 корпуса", image="B4F3")
                    else:
                        yield Message("Я жду пока вы нажмете кнопку...")
            else:
                yield Message("Я жду пока вы нажмете кнопку...")

