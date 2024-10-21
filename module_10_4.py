import random
from threading import Thread
from time import sleep
from queue import Queue

#  Класс Table - с атрибутами - номер стола и гость за этим столом.
class Table():
    def __init__(self, number):
        self.number = number
        self.guest = None

# Класс Guest - поток
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name # имя гостя

    def run(self):
        # sleep(random.randint(3, 10))
        pause =  random.randint(3, 10) # ожидание гостя в течение заданного времени (от 3 до 10 секунд)
        sleep(pause)

# Класс Cafe
class Cafe:
    list_thr = [] # создание списка

    def __init__(self, *tables):
        self.queue = Queue() # создание очереди (объект класса Queue)
        self.tables = list(tables) # перечень столов

    def guest_arrival(self, *guests): # метод прибытия гостя
        list_guests = list(guests)
        list_tables = self.tables
        len_list_guests = len(list_guests)
        min_guests_tables = min(len_list_guests, len(self.tables))
        for i in range(min_guests_tables): # перебор
            list_tables[i].guest = guests[i]
            thr1 = guests[i]
            thr1.start()
            Cafe.list_thr.append(thr1)
            print(f'{list_guests[i].name} сел(-а) за стол номер {list_tables[i].number}')
        if len_list_guests > min_guests_tables:
            for i in range(min_guests_tables, len_list_guests):
                self.queue.put(guests[i])
                print(f'{list_guests[i].name} в очереди')

    def discuss_guests(self): # обслуживание гостей
        while not (self.queue.empty()) or Cafe.check_table(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    thr1 = table.guest
                    thr1.start()
                    Cafe.list_thr.append(thr1)

    def check_table(self): # проверка столов на свободность
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman','Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
# cafe.guest_arrival(*guests)
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
for thr in Cafe.list_thr:
    thr.join()