from bots import vk_bot, te_bot
from multiprocessing import Process
from parser import pa_bot


if __name__ == "__main__":
    p1 = Process(target=vk_bot)
    p2 = Process(target=te_bot)
    p3 = Process(target=pa_bot)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

