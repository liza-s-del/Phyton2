"""
Классы для публикаций в социальной сети.
Post - базовый класс. Текст, изображение - дочерние классы.
"""

class Post:
    """
    Базовый класс для всех публикаций.
    """

    def __init__(self, author: str, content: str):
        """
        Инициализация поста.

        : param author: Автор поста
        : param content: Содержание поста
        """
        self._author = author
        self._content = content
        self._likes = 0
        self._comments = []

    @property
    def author(self) -> str:
        """Автор поста."""
        return self._author

    @property
    def likes(self) -> int:
        """Количество лайков."""
        return self._likes

    def like(self) -> None:
        """Поставить лайк."""
        self._likes += 1
        print(f"Пользователю понравился ваш пост. Всего лайков: {self._likes}")

    def comment(self, text: str) -> None:
        """
        Добавить комментарий.

        : param text: Текст комментария
        """
        self._comments.append(text)
        print(f"Добавлен комментарий: {text}")

    def show_comments(self) -> None:
        """Показать все комментарии."""
        if not self._comments:
            print("Комментариев нет")
        else:
            print("Комментарии:")
            for i, comment in enumerate(self._comments, 1):
                print(f"  {i}. {comment}")

    def display(self) -> None:
        """Базовый метод отображения поста."""
        print(f"\nПост от {self._author}")
        print(self._content)
        print(f"Лайков: {self._likes}")

    def __str__(self) -> str:
        """Строковое представление поста."""
        return (f"Пост от {self._author}\n"
                f"Лайков: {self._likes}\n"
                f"Комментариев: {len(self._comments)}")

    def __repr__(self) -> str:
        """Техническое представление."""
        return f"Post(author='{self._author}')"


class TextPost(Post):
    """
    Текстовый пост.
    """

    def __init__(self, author: str, content: str):
        """
        Инициализация текстового поста.

        :param author: Автор
        :param content: Текст поста
        """
        super().__init__(author, content)
        self._hashtags = self._extract_hashtags(content)

    def _extract_hashtags(self, text: str) -> list:
        """Извлечение хештегов из текста."""
        words = text.split()
        hashtags = [word for word in words if word.startswith('#')]
        return hashtags

    @property
    def hashtags(self) -> list:
        """Список хештегов."""
        return self._hashtags

    def display(self) -> None:
        """
        Перегруженный метод отображения.

        Текстовый пост показывает еще и хештеги.
        """
        super().display()
        if self._hashtags:
            print(f"Теги: {' '.join(self._hashtags)}")

    def __str__(self) -> str:
        """
        Перегруженный строковой метод.

        Меняется тип поста.
        """
        base = super().__str__()
        return f"{base}\nТекст: {self._content[:50]}..."


class ImagePost(Post):
    """
    Пост с изображением.
    """

    def __init__(self, author: str, image_url: str, content: str = ""):
        """
        Инициализация поста с изображением.

        : param author: Автор
        : param image_url: Ссылка на изображение
        : param description: Описание
        """
        super().__init__(author, content)
        self._image_url = image_url
        self._filters = []

    @property
    def image_url(self) -> str:
        """Ссылка на изображение."""
        return self._image_url

    def add_filter(self, filter_name: str) -> None:
        """Добавить фильтр к изображению."""
        self._filters.append(filter_name)
        print(f"Применен фильтр: {filter_name}")

    def display(self) -> None:
        """
        Перегруженный метод отображения.

        Причина перегрузки: пост с картинкой показывается иначе.
        """
        print(f"\nПост от {self._author}")
        print(f"Изображение: {self._image_url}")
        if self._content:
            print(f"Описание: {self._content}")
        if self._filters:
            print(f"Фильтры: {', '.join(self._filters)}")
        print(f"Лайков: {self._likes}")

    def __str__(self) -> str:
        """
        Перегруженный строковой метод.

        Меняется тип поста.
        """
        base = super().__str__()
        return f"{base}\nИзображение: {self._image_url}"


if __name__ == "__main__":
    # Пример

    # Создание постов
    text = TextPost("Марина", "Сегодня отличная погода! #весна #солнце")
    image = ImagePost("Константин", "https://foto.ru/travel.jpg", "Прилетели в замечательный город.")

    # __str__
    print("\n__str__:")
    print("-" * 30)
    print("\nТекстовый пост:")
    print(text)
    print("\nПост с фото:")
    print(image)

    # __repr__
    print("\n__repr__:")
    print("-" * 30)
    print(f"repr(text): {repr(text)}")
    print(f"repr(image): {repr(image)}")

    # display
    print("\nОтображение постов:")
    print("-" * 30)
    text.display()
    image.display()

    # Реализация методов
    print("\nМетоды:")
    print("-" * 30)

    print("\nТекстовый пост:")
    text.like()
    text.like()
    text.comment("Класс!")
    text.show_comments()
    print(f"Хештеги: {text.hashtags}")

    print("\nПост с фото:")
    image.add_filter("sepia")
    image.like()

pass
