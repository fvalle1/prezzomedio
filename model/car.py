import random

class Car():
    def __init__(self) -> None:
        self.tank_size = 1 + random.random()*2
        