

class Message:
    def __init__(self, text="...", image="", buttons=(), del_buttons=False):
        self.text = text
        self.image = image
        self.buttons = buttons
        self.delete_buttons = del_buttons


MESSAGE_1 = Message(
    text="Многострочный текст.\nВторая строка"
)
MESSAGE_2 = Message(
    image="Logo"
)
MESSAGE_3 = Message(
    text="Подтвердите...",
    buttons=("Да", "Нет")
)
MESSAGE_4 = Message(
    text="Подтвердите...",
    image="Logo",
    buttons=("!1111111111111111111111111111111111111111",
             "!2222222222222222222222222222222222222222",
             "!3333333333333333333333333333333333333333")
)

