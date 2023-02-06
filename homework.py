from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info: list[str, float] = ('Тип тренировки: {training_type};'
                              ' Длительность: {duration:.3f} ч.;'
                              ' Дистанция: {distance:.3f} км;'
                              ' Ср. скорость: {speed:.3f} км/ч;'
                              ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить результат в виде сообщения.

        Args:
            self (__class__): Собственный класс.

            info (list[str, float]): Описание и результаты
            пройденных тренировок.

        Returns:
            str: Распакованный словарь с результатами тренировок.
            """
        return self.info.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM: int = 1000
    H_IN_M: int = 60
    SM_IN_M: int = 100
    LEN_STEP: ClassVar[float] = 0.65

    def get_distance(self) -> float:
        """Возвращает пройденную дистанцию в километрах.

        Args:
            self (__class__): Собственный класс.

            action (int): Расстояние, пройденное за тренировку.

            duration (float): Время тренировки.

            weight (float): Вес человека.

            LEN_STEP (float): Длина шага человека.

        Returns:
            float: Пройденная дистанция в километрах.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.

        Args:
            self (__class__): Собственный класс.

            get_distance() (float): Дистанция, пройденная за тренировку.

            duration (float): Время тренировки.

        Returns:
            float: Средняя скорость движения в км/ч.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Функция для дочерних классов.

        """
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке.

        Args:
            self (__class__): Собственный класс.

            type(self).__name__ (__class__): Имя класса.

            duration (float): Время тренировки.

            get_distance() (float): Дистанция, пройденная за тренировку.

            get_mean_speed() (float): Средняя скорость в км/ч.

            get_spent_calories() (float): Затраченные калории за тренировку.

        Returns:
            __class__: Возвращает класс InfoMessage.
        """
        return InfoMessage(type(self).__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Args:
            self (__class__): Собственный класс.

            CALORIES_MEAN_SPEED_MULTIPLIER (float):
            Множитель средней скорости калорий.

            CALORIES_MEAN_SPEED_SHIFT (float):
            Средняя скорость переменещения калорий.

            weight (float): Вес человека.

            get_mean_speed() (float): Средняя скорость в км/ч.

            duration (float): Время тренировки в часах.

            H_IN_M (int): Колчество минут в одном часе.

            M_IN_KM (int): Количество метров в километре.

        Returns:
            float: Колличество затраченных калорий при беге.
            """
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_M))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    KM_IN_MS: float = 0.278
    SM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action,
                         duration,
                         weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Args:
            self (__class__): Собственный класс.

            CALORIES_MEAN_SPEED_MULTIPLIER (float):
            Множитель средней скорости калорий.

            CALORIES_MEAN_SPEED_SHIFT (float):
            Средняя скорость переменещения калорий.

            weight (float): Вес человека.

            get_mean_speed() (float): Средняя скорость в км/ч.

            KM_IN_MS (float): Колличество км/ч в м/с.

            height (float): Рост человека в сантиметрах.

            duration (float): Время тренировки в часах.

            H_IN_M (int): Колчество минут в одном часе.

            SM_IN_M (int): Количество сантиметров в метре.

        Returns:
            float: Количество затраченных калорий при ходьбе.
        """
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight
                + (self.get_mean_speed() * self.KM_IN_MS)
                ** 2
                / (self.height / self.SM_IN_M)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * (self.duration * self.H_IN_M))


class Swimming(Training):
    """Тренировка: плавание."""
    WEIGHT_CALORIES_MULTIPLIER: float = 1.1
    WEIGHT_CALORIES_SHIFT: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_distance(self) -> float:
        """Получить расстояние в КМ.

         Args:
            self (__class__): Собственный класс.

            action (int): Расстояние, пройденное за тренировку.

            LEN_STEP (float): Длина одного гребка человека.

            M_IN_KM (int): Количество метров в километре.

        Returns:
            float: Дистанция заплыва в километрах.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.

        Args:
            self (__class__): Собственный класс.

            length_pool (float): Длина бассейна в метрах.

            count_pool (int): Cколько раз пользователь переплыл бассейн.

            duration (float): Время тренировки в часах.

            M_IN_KM (int): Количество метров в километре.

        Returns:
            float: Средняя скорость заплыва в километрах.
            """
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Args:
            self (__class__): Собственный класс.

            WEIGHT_CALORIES_MULTIPLIER (float):
            Множитель веса калорий.

            WEIGHT_CALORIES_SHIFT (float):
            Смещение калорий.

            weight (float): Вес человека.

            get_mean_speed() (float): Средняя скорость в км/ч.

            duration (float): Время тренировки в часах.

        Returns:
            float: Количество затраченных калорий при плавании.
            """
        return ((self.get_mean_speed() + self.WEIGHT_CALORIES_MULTIPLIER)
                * self.WEIGHT_CALORIES_SHIFT
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.
    Проверяет в словаре тип тренировки и если он
    там существует, создает экземпляр класса и
    принимает туда параметры data (list).

    Args:
        workout_type (str): Тип тренировки.

        data (list): Параметры типа тренировки.

    Returns:
        __class__: Возвращает класс Training.
        """
    training_mode: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type not in training_mode:
        raise ValueError('Не существует такого типа тренировки')
    return training_mode[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция.

    Args:
        training (Training): Принимает на вход класс Training
        c полученными данными в результате тренировки.

    Returns:
        str: Печатает результат пройденной тренировки.
        """
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [16000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
