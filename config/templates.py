from message import Message


IMAGES = {
    "Logo": {"te": "AgACAgIAAxkBAAIIY2OI3EnKRUvpoRdM4-kIiAh9pS3eAAJuwzEbGrpASFC9Xo-DiB8tAQADAgADbQADKwQ",
             "vk": "photo-217283041_457239018"},
    "B1F1": {"te": "AgACAgIAAxkBAAIJ12OQktoqYFhwVYk8N5BDT9stZ7e_AALhwzEbx7qISH4t_AToVkAVAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239020"},
    "B1F2": {"te": "AgACAgIAAxkBAAIJ12OQktoqYFhwVYk8N5BDT9stZ7e_AALhwzEbx7qISH4t_AToVkAVAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239020"},
    "B2F1": {"te": "AgACAgIAAxkBAAILBWOUf1lWVTHtZyyeIfSn_8bs7pXsAAJkwzEbKjagSAh2_iPn-jIDAQADAgADeQADKwQ",
             "vk": "photo-217283041_457239021"},
    "B2F2": {"te": "AgACAgIAAxkBAAILB2OUf5EsoDR0QRjAsQT76_BjHPU-AAJlwzEbKjagSMyYGkNtxEXcAQADAgADeQADKwQ",
             "vk": "photo-217283041_457239022"},
    "B2F3": {"te": "AgACAgIAAxkBAAILvmOVpd__IiKh1I2-rYG3WHuAzOuHAAKUwzEbRAGxSEiz81pQRWhrAQADAgADeQADKwQ",
             "vk": "photo-217283041_457239023"},
    "B2F4": {"te": "AgACAgIAAxkBAAILwGOVpeSk5ruGWpuZZAPueLKmWDMCAAKVwzEbRAGxSO9jZ52123TeAQADAgADeAADKwQ",
             "vk": "photo-217283041_457239024"},
    "B2F5": {"te": "AgACAgIAAxkBAAILwmOVpem1NS9DbM0U2lnIYDaB7CprAAKWwzEbRAGxSKyLc9Y-sgNlAQADAgADeAADKwQ",
             "vk": "photo-217283041_457239025"},
    "B3F1": {"te": "AgACAgIAAxkBAAIL2mOW763e53o9VHBLoYdaHLSb4rs_AAKvvzEbRAG5SFISWhncHZRpAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239027"},
    "B3F2": {"te": "AgACAgIAAxkBAAIL3GOW78opeJ0HQIuq53t1XXaN0JWnAAKxvzEbRAG5SAaQFFJL4AwCAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239028"},
    "B3F3": {"te": "AgACAgIAAxkBAAIJ12OQktoqYFhwVYk8N5BDT9stZ7e_AALhwzEbx7qISH4t_AToVkAVAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239020"},
    "B4F1": {"te": "AgACAgIAAxkBAAIJ12OQktoqYFhwVYk8N5BDT9stZ7e_AALhwzEbx7qISH4t_AToVkAVAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239020"},
    "B4F2": {"te": "AgACAgIAAxkBAAIJ12OQktoqYFhwVYk8N5BDT9stZ7e_AALhwzEbx7qISH4t_AToVkAVAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239020"},
    "B4F3": {"te": "AgACAgIAAxkBAAIJ12OQktoqYFhwVYk8N5BDT9stZ7e_AALhwzEbx7qISH4t_AToVkAVAQADAgADdwADKwQ",
             "vk": "photo-217283041_457239020"}
}

ADDRESSES = {
    "Столовые": "Список адресов столовых",
    "Корпуса": "Список адресов корпусов"
}

GREETING = 'Приветствую!\n' \
               'Это телеграмм бот для студентов НТГМК.\n' \
               'Все команды доступны вам с этого момента.\n' \
               'Чтобы узнать о доступных возможностях нажмите /help.'

INCORRECT_COMMAND = "Нет такой команды\n" \
                    "(помощь - /help)"

NO_COMMAND = "Команда не введена.\n" \
             "Нужно ввети команду\n" \
             "(помощь - /help)"

COMMAND_SYNTAX_ERROR = Message(
    "Ошибка в синтаксисе команды.\n"
    "Помощь /help [имя команды]",
    buttons=("Помощь")
)

WRONG_DATE_FORMAT = 'Неверный формат даты'

ENTER_GROUP = Message("Введите номер группы (без пробелов).")

FOR_WHO = 'Это справка для вас - 0\n' \
              'или для другого - 1'

NEED_0_OR_1 = 'Нужно ввести 0 или 1'

ENTER_PERIOD = "Введите период получения доходов\n" \
                   "Например: 2022 год"

ENTER_DOCUMENT_NAME = "Введите примерное название документа"

NEED_NUMBER_IN_INTERVAL = "Нужно ввести число от 1 до 8, соответсвующее номеру документа"

ENTER_FIO = "Введите Фамилию Имя Отчество"

ENTER_PHONE = "Введите номер телефона"

ENTER_EMAIL = "Введите Email"

ENTERSAGE = "Введите сообщение\n" \
            "(Дополнительные пожелания)\n" \
            "или отправьте любое сообщение."

SUCCESS_ORDER = 'Заявка оформлена.\n' \
                'Забрать справку можно спустя 3 рабочих дня после оформления заявки в главном корпусе.\n' \
                '/help'

ERROR_ORDER = 'Произошла ошибка.\n' \
                  'Возможно введены неверные данные, попробуйте еше раз.'

ENTER_SUPPORT = 'Введите сообщение для техподдержки.\n' \
                    'Ваша жалоба будет рассмотрена разработчиками.'

SUCCESS_SEND = 'Ваше сообщение отправлено. Ожидайте ответ в этом чате.'

YOU_IS_SUBSCRIBE = 'Вы уже подписаны, хотите отписаться?\n' \
                       '(1 - Да, 0 - Нет)'

SUCCESS_SUBSCRIBE = 'Подписка на расписание оформлена.\n' \
                    'Вы будете получать расписание при каждом его обновлении на сайте.'

SUBSCRIBE_SAVED = 'Подписка сохранена'

SUBSCRIBE_CANCELED = 'Подписка отменена'

CONFIRM_CLEAR = 'Вы уверены, что хотите очистить свои данные?\n' \
                    '(1 - Да, 0 - Нет)'

DATA_IS_SAVED = 'Данные сохранены'

DATA_CLEARED = 'Данные очищены. Чтобы вновь их заполнить запросите расписание или справку.'