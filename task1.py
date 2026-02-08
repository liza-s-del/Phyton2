import doctest
from typing import List

class Playlist:
    """
    Класс, представляющий музыкальный плейлист.
    """
    def __init__(self, name: str, songs: List[str]):
        """
        Создание и подготовка к работе объекта Playlist.

        :param name: Название плейлиста
        :param songs: Список песен

        Примеры:
        >>> playlist = Playlist("Test", ["Song1", "Song2"])
        """
        if not isinstance(name, str):
            raise TypeError("Название плейлиста должно быть строкой")
        if not name.strip():
            raise ValueError("Название плейлиста не может быть пустым")
        self.name = name

        if not isinstance(songs, list):
            raise TypeError("Список песен должен быть списком")
        if not all(isinstance(song, str) for song in songs):
            raise TypeError("Все песни в списке должны быть строками")
        self.songs = songs

    def add_song(self, song_name: str) -> None:
        """
        Добавить песню в плейлист.

        :param song_name: Название добавляемой песни
        :raise ValueError: Если песня уже есть в плейлисте

        Примеры:
        >>> playlist = Playlist("Test", ["Song1"])
        >>> playlist.add_song("Song2")
        """
        if not isinstance(song_name, str):
            raise TypeError("Название песни должно быть строкой")
        if not song_name.strip():
            raise ValueError("Название песни не может быть пустым")

        if song_name in self.songs:
            raise ValueError(f"Песня '{song_name}' уже есть в плейлисте")

        self.songs.append(song_name)

    def remove_song(self, song_name: str) -> bool:
        """
        Удалить песню из плейлиста по названию.

        :param song_name: Название песни для удаления
        :return: True если песня была удалена, False если песни не было в плейлисте

        Примеры:
        >>> playlist = Playlist("Test", ["Song1", "Song2", "Song3"])
        >>> playlist.remove_song("Song2")
        True
        >>> playlist.remove_song("Song")
        False
        """
        if not isinstance(song_name, str):
            raise TypeError("Название песни должно быть строкой")

        if song_name in self.songs:
            self.songs.remove(song_name)
            return True
        return False

    def get_song_count(self) -> int:
        """
        Получить количество песен в плейлисте.

        :return: Количество песен

        Примеры:
        >>> playlist = Playlist("Test", ["Song1", "Song2", "Song3"])
        >>> playlist.get_song_count()
        3
        """
        return len(self.songs)

if __name__ == "__main__":
    doctest.testmod()


import doctest
from typing import List, Dict

class FloorPlan:
    """
    Класс, представляющий планировку помещения.

    :param total_area (float): Общая площадь помещения в м2
    :param rooms (List[Dict]): Список комнат
    """

    def __init__(self, total_area: float, rooms: List[Dict]):
        """
        Создание и подготовка к работе объекта FloorPlan.

        Пример:
        >>> plan = FloorPlan(85.5, [{"name": "гостиная", "area": 25.5}])
        """
        if not isinstance(total_area, (int, float)):
            raise TypeError("Общая площадь должна быть числом (int или float)")
        if total_area <= 0:
            raise ValueError("Общая площадь должна быть положительным числом")
        self.total_area = float(total_area)

        validated_rooms, total_rooms_area = self.validate_rooms(rooms)

        # Проверка, что сумма площадей комнат не превышает общую площадь
        if total_rooms_area > self.total_area:
            raise ValueError(
                f"Суммарная площадь комнат ({total_rooms_area:.2f} м2) "
                f"превышает общую площадь ({self.total_area:.2f} м2)"
            )

        self.rooms = validated_rooms

    def validate_rooms(self, rooms: List[Dict]) -> tuple[List[Dict], float]:
        """
        Проверка списка комнат.

        :param rooms: Список комнат для проверки
        :return: Кортеж из (проверенные_комнаты, суммарная_площадь)
        :raise TypeError: Если комнаты имеют неверный тип
        :raise ValueError: Если комнаты содержат некорректные данные
        """
        if not isinstance(rooms, list):
            raise TypeError("Список комнат должен быть списком")

        validated_rooms = []
        total_rooms_area = 0.0

        for i, room in enumerate(rooms):
            if not isinstance(room, dict):
                raise TypeError(f"Комната №{i + 1} должна быть словарём")

            if "name" not in room or "area" not in room:
                raise ValueError(f"Комната №{i + 1} должна содержать ключи 'name' и 'area'")

            if not isinstance(room["name"], str):
                raise TypeError(f"Название комнаты №{i + 1} должно быть строкой")

            if not isinstance(room["area"], (int, float)):
                raise TypeError(f"Площадь комнаты №{i + 1} должна быть числом")

            if room["area"] <= 0:
                raise ValueError(f"Площадь комнаты №{i + 1} должна быть положительной")

            total_rooms_area += float(room["area"])
            validated_rooms.append({
                "name": room["name"].strip(),
                "area": float(room["area"])
            })

        return validated_rooms, total_rooms_area

    def add_room(self, room_name: str, area: float) -> None:
        """
        Добавить комнату в планировку.

        :param room_name: Название комнаты
        :param area: Площадь комнаты в м2
        :raise ValueError: Если комната с таким названием уже существует или сумма площадей превысит общую площадь

        Примеры:
        >>> plan = FloorPlan(100.0, [{"name": "кухня", "area": 15.0}])
        >>> plan.add_room("гостиная", 25.0)
        """
        if not isinstance(room_name, str):
            raise TypeError("Название комнаты должно быть строкой")

        room_name = room_name.strip()
        if not room_name:
            raise ValueError("Название комнаты не может быть пустым")

        if not isinstance(area, (int, float)):
            raise TypeError("Площадь комнаты должна быть числом")

        if area <= 0:
            raise ValueError("Площадь комнаты должна быть положительной")

        # Проверка на дубликат названия
        if any(room["name"].lower() == room_name.lower() for room in self.rooms):
            raise ValueError(f"Комната с названием '{room_name}' уже существует")

        # Проверка, что новая комната поместится
        current_total = self.get_total_rooms_area()
        if current_total + area > self.total_area:
            available = self.total_area - current_total
            raise ValueError(
                f"Недостаточно площади. Доступно: {available:.2f} м2, "
                f"требуется: {area:.2f} м2"
            )

        self.rooms.append({
            "name": room_name,
            "area": float(area)
        })

    def remove_room(self, room_name: str) -> bool:
        """
        Удалить комнату из планировки по названию.

        :param room_name: Название комнаты для удаления
        :return: True если комната была удалена, False если комнаты не было в планировке

        Примеры:
        >>> plan = FloorPlan(100.0, [{"name": "кухня", "area": 15.0}, {"name": "гостиная", "area": 25.0}])
        >>> plan.remove_room("кухня")
        True
        >>> plan.remove_room("спальня")
        False
        """
        if not isinstance(room_name, str):
            raise TypeError("Название комнаты должно быть строкой")

        room_name = room_name.strip()

        for i, room in enumerate(self.rooms):
            if room["name"].lower() == room_name.lower():
                self.rooms.pop(i)
                return True

        return False

    def get_total_rooms_area(self) -> float:
        """
        Получить суммарную площадь всех комнат.

        :return: Суммарная площадь комнат в м2

        Примеры:
        >>> plan = FloorPlan(100.0, [{"name": "кухня", "area": 15.0}, {"name": "гостиная", "area": 25.0}])
        >>> plan.get_total_rooms_area()
        40.0
        """
        return sum(room["area"] for room in self.rooms)

if __name__ == "__main__":
    doctest.testmod()


import doctest

class FitnessTracker:
    """
    Класс, представляющий фитнес-трекер.

    :param steps_today (int): Количество пройденных шагов за сегодня
    :param heart_rate (int): Текущий пульс в ударах в минуту
    """

    def __init__(self, steps_today: int, heart_rate: int):
        """
        Создание и подготовка к работе объекта FitnessTracker.

        Примеры:
        >>> tracker = FitnessTracker(5000, 72)
        >>> tracker.steps_today
        5000
        """
        if not isinstance(steps_today, int):
            raise TypeError("Количество шагов должно быть целым числом")
        if steps_today < 0:
            raise ValueError("Количество шагов не может быть отрицательным")
        self.steps_today = steps_today

        if not isinstance(heart_rate, int):
            raise TypeError("Пульс должен быть целым числом")
        if heart_rate < 40 or heart_rate > 200:
            raise ValueError("Пульс должен быть в диапазоне от 40 до 200 уд/мин")
        self.heart_rate = heart_rate

    def add_steps(self, steps: int) -> None:
        """
        Добавить пройденные шаги.

        :param steps: Количество добавляемых шагов
        :raise ValueError: Если количество шагов отрицательное

        Примеры:
        >>> tracker = FitnessTracker(5000, 72)
        >>> tracker.add_steps(1000)
        >>> tracker.steps_today
        6000
        """
        if not isinstance(steps, int):
            raise TypeError("Количество шагов должно быть целым числом")
        if steps < 0:
            raise ValueError("Количество добавляемых шагов не может быть отрицательным")

        self.steps_today += steps

    def update_heart_rate(self, new_heart_rate: int) -> None:
        """
        Обновить текущий пульс.

        :param new_heart_rate: Новое значение пульса
        :raise ValueError: Если пульс вне допустимого диапазона

        Примеры:
        >>> tracker = FitnessTracker(5000, 72)
        >>> tracker.update_heart_rate(75)
        >>> tracker.heart_rate
        75
        """
        if not isinstance(new_heart_rate, int):
            raise TypeError("Пульс должен быть целым числом")
        if new_heart_rate < 40 or new_heart_rate > 200:
            raise ValueError("Пульс должен быть в диапазоне от 40 до 200 уд/мин")

        self.heart_rate = new_heart_rate

    def check_heart_rate_zone(self) -> str:
        """
        Определить зону пульса.

        :return: Название зоны пульса

        Примеры:
        >>> tracker1 = FitnessTracker(5000, 60)
        >>> tracker1.check_heart_rate_zone()
        'Разминка'
        >>> tracker2 = FitnessTracker(5000, 140)
        >>> tracker2.check_heart_rate_zone()
        'Кардио'
        """
        if self.heart_rate < 100:
            return "Разминка"
        elif 100 <= self.heart_rate < 130:
            return "Жиросжигание"
        elif 130 <= self.heart_rate < 160:
            return "Кардио"
        else:
            return "Максимальная нагрузка"

    def estimate_steps_to_goal(self, daily_goal: int) -> int:
        """
        Оценить, сколько шагов осталось до достижения дневной цели.

        :param daily_goal: Дневная цель по шагам
        :return: Количество оставшихся шагов до цели

        Примеры:
        >>> tracker = FitnessTracker(5000, 72)
        >>> tracker.estimate_steps_to_goal(10000)
        5000
        >>> tracker2 = FitnessTracker(12000, 72)
        >>> tracker2.estimate_steps_to_goal(10000)
        0
        """
        if not isinstance(daily_goal, int):
            raise TypeError("Дневная цель должна быть целым числом")
        if daily_goal < 0:
            raise ValueError("Дневная цель не может быть отрицательной")

        remaining = daily_goal - self.steps_today
        return max(remaining, 0)

if __name__ == "__main__":
    doctest.testmod()