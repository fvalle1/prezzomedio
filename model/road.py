from math import mean
from model.station import Station


class Road():
    def __init__(self, N_Stations) -> None:
        self.stations = [Station() for _ in range(N_Stations)]

    @property
    def prices(self)->list:
        return [s.price for s in self.stations]
    
    @property
    def avg_price(self)->float:
        return mean(self.prices)
    
    def update(self):
        for s in self.stations:
            s.update()

    def __getitem__(self, i:int):
        return self.stations[i]

    def __len__(self):
        return len(self.stations)
