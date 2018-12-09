from enum import Enum


class Food(object):
    def __init__(self, food_type, fruit_type=None):
        if food_type is None or not isinstance(food_type, Food.FoodType):
            raise RuntimeError('Invalid food type', food_type)
        if food_type is Food.FoodType.FRUIT and (fruit_type is None or not isinstance(fruit_type, Food.FruitType)):
            raise RuntimeError('Invalid fruit type', food_type)
        self._food_type = food_type
        self._fruit_type = fruit_type

    def get_points(self):
        if self._food_type is Food.FoodType.FRUIT:
            return self._fruit_type.value
        return self._food_type.value

    def is_powerup(self):
        return self._food_type is Food.FoodType.PWRUP

    class FoodType(Enum):
        BASIC = 10
        PWRUP = 50
        FRUIT = 0

    class FruitType(Enum):
        CHRRY = 100
        STRWB = 300
        ORNGE = 500
        APPLE = 700
        MELON = 1000
        GALAX = 2000
        BELL = 3000
        KEY = 5000
