from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Informational message about the workout."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info: list[str, float] = ('Workout type: {training_type};'
                              ' Duration: {duration:.3f} ч.;'
                              ' Distance: {distance:.3f} км;'
                              ' Average speed: {speed:.3f} км/ч;'
                              ' Calories burned: {calories:.3f}.')

    def get_message(self) -> str:
        """Get the result as a message.

        Args:
            self (__class__): Own class.

            info (list[str, float]): Description and results
            of completed trainings.

        Returns:
            str: Unpacked dictionary with training results.
            """
        return self.info.format(**asdict(self))


@dataclass
class Training:
    """Base training class."""
    action: int
    duration: float
    weight: float

    M_IN_KM: int = 1000
    H_IN_M: int = 60
    SM_IN_M: int = 100
    LEN_STEP: ClassVar[float] = 0.65

    def get_distance(self) -> float:
        """Returns the distance traveled in kilometers.

        Args:
            self (__class__): Own class.

            action (int): Distance traveled per workout.

            duration (float): Workout time.

            weight (float): Human weight.

            LEN_STEP (float): The length of a person's stride.

        Returns:
            float: Distance traveled in kilometers.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average moving speed.

        Args:
            self (__class__): Own class.

            get_distance() (float): Distance covered per workout.

            duration (float): Workout time.

        Returns:
            float: Average speed in km/h.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get calories burned.

        Function for child classes.

        """
        pass

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed workout.

        Args:
            self (__class__): Own class.

            type(self).__name__ (__class__): class name.

            duration (float): Workout time.

            get_distance() (float): Distance covered per workout.

            get_mean_speed() (float): Average speed in km/h.

            get_spent_calories() (float): Calories burned per workout.

        Returns:
            __class__: Returns the InfoMessage class.
        """
        return InfoMessage(type(self).__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Workout: running."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Get calories burned.

        Args:
            self (__class__): Own class.

            CALORIES_MEAN_SPEED_MULTIPLIER (float):
            Calorie average rate multiplier.

            CALORIES_MEAN_SPEED_SHIFT (float):
            Average rate of change of calories.

            weight (float): Human weight.

            get_mean_speed() (float): Average speed in km/h.

            duration (float): Training time in hours.

            H_IN_M (int): The number of minutes in one hour.

            M_IN_KM (int): The number of meters in a kilometer.

        Returns:
            float: The number of calories burned while running.
            """
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_M))


class SportsWalking(Training):
    """Workout: race walking."""
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
        """Get calories burned.

        Args:
            self (__class__): Own class.

            CALORIES_MEAN_SPEED_MULTIPLIER (float):
            Calorie average rate multiplier.

            CALORIES_MEAN_SPEED_SHIFT (float):
            Average rate of change of calories.

            weight (float): Human weight.

            get_mean_speed() (float): Average speed in km/h.

            KM_IN_MS (float): Number of km/h in m/s.

            height (float): Human height in centimeters.

            duration (float): Training time in hours.

            H_IN_M (int): Number of minutes in one hour.

            SM_IN_M (int): Number of centimeters in a meter.

        Returns:
            float: The number of calories burned while walking.
        """
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight
                + (self.get_mean_speed() * self.KM_IN_MS)
                ** 2
                / (self.height / self.SM_IN_M)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * (self.duration * self.H_IN_M))


class Swimming(Training):
    """Workout: swimming."""
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
        """Get distance in km.

         Args:
            self (__class__): Own class.

            action (int): Distance traveled per workout.

            LEN_STEP (float): The length of one stroke of a person.

            M_IN_KM (int): The number of meters in a kilometer.

        Returns:
            float: Swimming distance in kilometers.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average moving speed.

        Args:
            self (__class__): Own class.

            length_pool (float): Pool length in meters.

            count_pool (int): How many times the user swam across the pool.

            duration (float): Training time in hours.

            M_IN_KM (int): The number of meters in a kilometer.

        Returns:
            float: Average swimming speed in kilometers.
            """
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Get calories burned.

        Args:
            self (__class__): Own class.

            WEIGHT_CALORIES_MULTIPLIER (float):
            Calorie weight multiplier.

            WEIGHT_CALORIES_SHIFT (float):
            Calorie offset.

            weight (float): Human weight.

            get_mean_speed() (float): Average speed in km/h.

            duration (float): Training time in hours.

        Returns:
            float: Number of calories burned while swimming.
            """
        return ((self.get_mean_speed() + self.WEIGHT_CALORIES_MULTIPLIER)
                * self.WEIGHT_CALORIES_SHIFT
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read the data received from the sensors.
    Checks the type of training in the dictionary and if it is
    exists there, creates an instance of the class, and
    accepts data (list) parameters there.

    Args:
        workout_type (str): Workout type.

        data (list): Workout Type Options.

    Returns:
        __class__: Returns the Training class.
        """
    training_mode: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type not in training_mode:
        raise ValueError('There is no such type of training')
    return training_mode[workout_type](*data)


def main(training: Training) -> None:
    """Main function.

    Args:
        training (Training): Takes the Training class as input
        with the data obtained as a result of training.

    Returns:
        str: Prints the result of the completed workout.
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
