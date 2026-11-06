from abc import ABC, abstractmethod

# Интерфейс объектов, способных атаковать
class Attacker(ABC):
    @abstractmethod
    def attack(self, unit):
        pass

# Интерфейс объектов, способных перемещаться
class Moveable(ABC):
    @abstractmethod
    def move(self, x, y):
        pass

# Базовый класс всех игровых объектов
class GameObject:
    def __init__(self, object_id, name, x, y):
        self._id = object_id
        self._name = name
        self._x = x
        self._y = y

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_position(self):
        return self._x, self._y

    def _set_position(self, x, y):
        self._x = x
        self._y = y

# Базовый класс игровых юнитов
class Unit(GameObject):
    def __init__(self, object_id, name, x, y, hp, damage):
        super().__init__(object_id, name, x, y)
        self._hp = hp
        self._damage = damage

    def is_alive(self):
        return self._hp > 0

    def get_hp(self):
        return self._hp

    def receive_damage(self, damage):
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным")

        if not self.is_alive():
            print(f"{self.get_name()} уже выбыл из боя")
            return

        self._hp = max(0, self._hp - damage)
        print(f"{self.get_name()} получил {damage} урона")

        if not self.is_alive():
            print(f"{self.get_name()} побеждён!")

# Класс лучника
class Archer(Unit, Attacker, Moveable):
    def __init__(self, object_id, name, x, y):
        super().__init__(object_id, name, x, y, 100, 25)

    def attack(self, unit):
        if not self.is_alive():
            print(f"{self.get_name()} не может атаковать")
            return

        print(f"{self.get_name()} выпускает стрелу!")
        unit.receive_damage(self._damage)

    def move(self, x, y):
        if not self.is_alive():
            print("Побеждённый лучник не может двигаться")
            return

        self._set_position(x, y)
        print(f"{self.get_name()} переместился в точку ({x}, {y})")

# Класс воина
class Warrior(Unit, Attacker, Moveable):
    def __init__(self, object_id, name, x, y):
        super().__init__(object_id, name, x, y, 150, 35)

    def attack(self, unit):
        if not self.is_alive():
            print(f"{self.get_name()} не может атаковать")
            return

        print(f"{self.get_name()} атакует мечом!")
        unit.receive_damage(self._damage)

    def move(self, x, y):
        if not self.is_alive():
            print("Побеждённый воин не может двигаться")
            return

        self._set_position(x, y)
        print(f"{self.get_name()} переместился в точку ({x}, {y})")


# Класс здания
class Building(GameObject):
    def __init__(self, object_id, name, x, y, built=False):
        super().__init__(object_id, name, x, y)
        self._built = built

    def is_built(self):
        return self._built

    def complete_construction(self):
        if self._built:
            print(f"{self.get_name()} уже построена")
            return

        self._built = True
        print(f"{self.get_name()} успешно построена!")


# Класс крепости
class Fort(Building, Attacker):
    def __init__(self, object_id, name, x, y, built=True):
        super().__init__(object_id, name, x, y, built)
        self._damage = 40

    def attack(self, unit):
        if not self.is_built():
            print("Крепость ещё не построена и не может атаковать")
            return

        print(f"{self.get_name()} стреляет из пушек!")
        unit.receive_damage(self._damage)


# Класс передвижного дома
class MobileHouse(Building, Moveable):
    def move(self, x, y):
        self._set_position(x, y)
        print(f"{self.get_name()} переехал в точку ({x}, {y})")


# Демонстрация игрового процесса
def main():
    # Создание игровых объектов
    archer = Archer(1, "Лучник", 2, 3)
    warrior = Warrior(2, "Воин", 4, 3)
    fort = Fort(3, "Вражеская крепость", 8, 8)
    house = MobileHouse(4, "Передвижной дом", 0, 0)

    # Первый ход
    print("\n--- Ход 1 ---")
    archer.move(5, 5)
    archer.attack(warrior)

    # Второй ход
    print("\n--- Ход 2 ---")
    warrior.attack(archer)
    fort.attack(archer)

    # Третий ход
    print("\n--- Ход 3 ---")
    archer.attack(warrior)
    house.move(3, 7)

    # Состояние игры
    print("\n--- Итоги ---")
    print(f"{archer.get_name()}: {archer.get_hp()} HP")
    print(f"{warrior.get_name()}: {warrior.get_hp()} HP")
    print(f"{fort.get_name()}: построена — {fort.is_built()}")
    print(f"{house.get_name()}: позиция — {house.get_position()}")

    print("\nИгра завершена!")


if __name__ == "__main__":
    main()
