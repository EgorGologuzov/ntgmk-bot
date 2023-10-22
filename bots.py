
import time
import config.templates as template
import config.tokens as token
import config.commands as command
import message
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import sessions
from database import Database, TimetableDB
from lib import *


class TeBot:
    users = {}
    bot = Bot(token=token.TE_TOKEN)
    dispatcher = Dispatcher(bot)
    service = "te"

    def __call__(self):
        @self.dispatcher.message_handler(content_types=types.ContentTypes.PHOTO)
        async def download_photo(mes: types.Message):
            await mes.answer(mes.photo[-1].file_id)

        @self.dispatcher.message_handler(commands=["start"])
        async def start(mes: types.Message):
            await self._send_message(mes.from_user.id, message.Message(
                        text="Приветствую, я бот НТГМК. Все команды доступны вам с этого момента.",
                        buttons=("Помощь",)
                    ))

        @self.dispatcher.message_handler(commands=[*command.TIMETABLE])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.STimetable, mes.text)

        @self.dispatcher.message_handler(commands=[*command.SUPPORT])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SSupport, mes.text)

        @self.dispatcher.message_handler(commands=[*command.HELP])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SHelp, mes.text)

        @self.dispatcher.message_handler(commands=[*command.CLEAR])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SClear, mes.text)

        @self.dispatcher.message_handler(commands=[*command.ORDER])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SOrderReference, mes.text)

        @self.dispatcher.message_handler(commands=[*command.SUBSCRIBE])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SSubscribe, mes.text)

        @self.dispatcher.message_handler(commands=[*command.MAP])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SMap, mes.text)

        @self.dispatcher.message_handler(commands=[*command.INFORMATION])
        async def timetable(mes: types.Message):
            await self._init_session(mes.from_user.id, sessions.SInformation, mes.text)

        @self.dispatcher.message_handler()
        async def no_command_message(mes: types.Message):
            await self._get_answer_by_message(mes.from_user.id, mes.text)

        @self.dispatcher.callback_query_handler()
        async def query(callback: types.CallbackQuery):
            com = callback.data.split()[0]
            if com in command.LIST:
                await self._init_session(callback.from_user.id, sessions.SList, callback.data)
            elif com in command.ADDRESS:
                await self._init_session(callback.from_user.id, sessions.SAddresses, callback.data)
            elif com in command.PLANS:
                await self._init_session(callback.from_user.id, sessions.SPlans, callback.data)
            elif com in command.HELP:
                await self._init_session(callback.from_user.id, sessions.SHelp, callback.data)
            else:
                if callback.from_user.id in self.users:
                    await self._get_answer_by_message(callback.from_user.id, callback.data)
                else:
                    # await self._send_message(callback.from_user.id, message.Message("Необработанный колбек."))
                    pass
            await callback.answer()

        async def on_startup(dispatcher):
            print("Telegram NTGMKBot is Online!")

        loop = asyncio.get_event_loop()
        loop.create_task(self.mailing())
        executor.start_polling(self.dispatcher, skip_updates=False, on_startup=on_startup, loop=loop)

    async def _send_message(self, user_id, mes: message.Message):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for button in mes.buttons:
            if button[0] == "!":
                button = button[1:]
                keyboard.add(types.InlineKeyboardButton(text=button, callback_data=button))
            else:
                keyboard.insert(types.InlineKeyboardButton(text=button, callback_data=button))
        if mes.image:
            await self.bot.send_photo(
                chat_id=user_id,
                photo=template.IMAGES[mes.image]["te"],
                caption=mes.text,
                reply_markup=keyboard
            )
        else:
            await self.bot.send_message(text=mes.text, chat_id=user_id, reply_markup=keyboard)

    async def _init_session(self, user_id, session_class, mes):
        self.users[user_id] = session_class((user_id, self.service))
        await self._get_answer_by_message(user_id, mes)

    async def _get_answer_by_message(self, user_id, mes):
        try:
            Database().add_user_if_not_in((user_id, self.service))
            if user_id in self.users:
                await self._send_message(user_id, self.users[user_id].answer_message(mes))
                if self.users[user_id].is_finished:
                    self.users.pop(user_id)
                return
            await self._send_message(user_id, message.Message("Такой команды нет", buttons=("Помощь",)))
        except Exception as e:
            await self._send_message(user_id, message.Message("Что-то пошло не так, попробуйте позже"))
            print(e)

    async def mailing(self):
        while True:
            await asyncio.sleep(10)
            updated, date = read_and_clear_tmp_file()
            if updated:
                db = TimetableDB()
                user_db = Database()
                for target in updated:
                    tt = db.select_timetable_by_target(target, date)
                    users_id = user_db.select_subscribed_users(target, "te")
                    for user in users_id:
                        await self._send_message(user[0], message.Message(tt))


class VkBot:
    users = {}
    bot = VkApi(token=token.VK_TOKEN)
    longpoll = VkBotLongPoll(bot, token.GROUP_ID)
    service = "vk"

    def __call__(self):
        print("VK NTGMKBot is Online!")
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.obj.message["text"]
                user_id = event.obj.message["from_id"]
                if text == "Начать":
                    self._send_message(user_id, message.Message(
                        text="Приветствую, я бот НТГМК. Все команды доступны вам с этого момента.",
                        buttons=("Помощь",)
                    ))
                    continue
                if text[0] != "/":
                    self._get_answer_by_message(user_id, text)
                    continue
                com = text[1:].split()[0]
                if com in command.TIMETABLE:
                    self._init_session(user_id, sessions.STimetable, text)
                elif com in command.MAP:
                    self._init_session(user_id, sessions.SMap, text)
                elif com in command.INFORMATION:
                    self._init_session(user_id, sessions.SInformation, text)
                elif com in command.CLEAR:
                    self._init_session(user_id, sessions.SClear, text)
                elif com in command.ORDER:
                    self._init_session(user_id, sessions.SOrderReference, text)
                elif com in command.SUBSCRIBE:
                    self._init_session(user_id, sessions.SSubscribe, text)
                elif com in command.HELP:
                    self._init_session(user_id, sessions.SHelp, text)
                elif com in command.SUPPORT:
                    self._init_session(user_id, sessions.SSupport, text)
                else:
                    self._send_message(user_id, message.Message("Такой команды нет", buttons=("Помощь",)))

            elif event.type == VkBotEventType.MESSAGE_EVENT:
                text = event.object.payload.get("type")
                com = text.split()[0]
                if com in command.LIST:
                    self._init_session(event.object.user_id, sessions.SList, text)
                elif com in command.ADDRESS:
                    self._init_session(event.object.user_id, sessions.SAddresses, text)
                elif com in command.PLANS:
                    self._init_session(event.object.user_id, sessions.SPlans, text)
                elif com in command.HELP:
                    self._init_session(event.object.user_id, sessions.SHelp, text)
                else:
                    if event.object.user_id in self.users:
                        self._get_answer_by_message(event.object.user_id, text)
                    else:
                        # self._send_message(event.object.user_id, message.Message("Необработанный колбек."))
                        pass
                # self._send_message(event.object.user_id, message.Message(event_type))
                self.bot.method(
                    method="messages.sendMessageEventAnswer",
                    values={
                        "event_id": event.object.event_id,
                        "user_id": event.object.user_id,
                        "peer_id": event.object.peer_id
                    }
                )

    def _send_message(self, user_id, mes):
        keyboard, attachment = "", ""
        if mes.buttons:
            keyboard = VkKeyboard(one_time=False, inline=True)
            for button in mes.buttons:
                if button[0] == "!":
                    if button != mes.buttons[0]:
                        keyboard.add_line()
                    button = button[1:]
                    keyboard.add_callback_button(
                        label=button,
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": button}
                    )
                else:
                    keyboard.add_callback_button(
                        label=button,
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": button}
                    )
            keyboard = keyboard.get_keyboard()
        if mes.image:
            attachment = template.IMAGES[mes.image]["vk"]
        self.bot.method(
            method="messages.send",
            values={
                "user_id": user_id,
                "random_id": get_random_id(),
                "message": mes.text,
                "attachment": attachment,
                "keyboard": keyboard
            }
        )

    def _init_session(self, user_id, session_class, mes):
        self.users[user_id] = session_class((user_id, self.service))
        self._get_answer_by_message(user_id, mes)

    def _get_answer_by_message(self, user_id, mes):
        try:
            Database().add_user_if_not_in((user_id, self.service))
            if user_id in self.users:
                self._send_message(user_id, self.users[user_id].answer_message(mes))
                if self.users[user_id].is_finished:
                    self.users.pop(user_id)
                return
            self._send_message(user_id, message.Message("Такой команды нет", buttons=("Помощь",)))
        except Exception as e:
            self._send_message(user_id, message.Message("Что-то пошло не так попробуйте позже"))
            print(e)

    def mailing(self, targets, date):
        db = TimetableDB()
        user_db = Database()
        for target in targets:
            tt = db.select_timetable_by_target(target, date)
            users_id = user_db.select_subscribed_users(target, "vk")
            for user in users_id:
                self._send_message(user[0], message.Message(tt))


vk_bot = VkBot()
te_bot = TeBot()

