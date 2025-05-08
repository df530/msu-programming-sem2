# Исходный код будет выполняться неправильно, т.к. в методе take_ticket могла случится гонка данных
# Конкретно, оба потока могли проверить, что билеты ещё остались, и только потом они оба уменьшили бы количество
# билетов и оба сказали бы, что билет выдан
# Также была print-ы разных потоков могли перемешаться и было бы непонятно, на чей запрос получен ответ
#
# В новой реализации используется блокировка, что гарантирует, что только один поток может выполнять take_ticket одновременно
# Билеты выдадутся корректно, print-ы не перепутаются -- сначала будет вывод для одного потока, потом для другого

import threading
from threading import Thread, current_thread

class RideQueue:
    def __init__(self, tickets_available):
        self.tickets_available = tickets_available
        self.lock = threading.Lock()
    def take_ticket(self, tickets_requested):
        with self.lock:
            print(f"{self.tickets_available} ticket(s) available before request.")
            name = current_thread().name
            if tickets_requested <= self.tickets_available:
                self.tickets_available -= tickets_requested
                print(f"{tickets_requested} ticket(s) assigned to {name}. Enjoy the ride!")
            else:
                print(f"Sorry {name}, not enough tickets available.")

ride = RideQueue(1)
visitor1 = Thread(target=ride.take_ticket, kwargs={"tickets_requested": 1}, name="Alice")
visitor2 = Thread(target=ride.take_ticket, kwargs={"tickets_requested": 1}, name="Bob")
visitor1.start()
visitor2.start()