import random
from model.car import Car
from model.strategies import strategies

class Station():
    def __init__(self) -> None:
        self.cars = [Car() for _ in range(N_cars)]
        self.price = 1.7 + random.random()*0.4 - 0.2
        self.strategy = self.last_strategy = strategies.STILL
        self.last_profit = len(self.cars)
    
    def get_random_strategy(self):
        r = random.random()
        if r < 1./3.:
            return strategies.UP
        elif r < 2./3:
            return strategies.STILL
        else:
            return strategies.DOWN
        
    def _apply_strategy(self):
        self.price = self.strategy(self.price)
        
    @property
    def profit(self):
        return sum([c.tank_size * self.price for c in self.cars])
        
    def update(self):
        if self.profit < self.last_profit * 0.9:
            self.strategy = strategies.DOWN
        elif self.profit > self.last_profit * 1.1:
            self.strategy = strategies.UP
        if random.random() < 0.1:
            self.strategy = self.get_random_strategy()
        self._apply_strategy()
        self.last_strategy = self.strategy
        self.last_profit = self.profit
        
    def __len__(self):
        return len(self.cars)
    