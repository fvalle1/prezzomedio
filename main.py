import random
import math
from statistics import median
from plotly.subplots import make_subplots
from model.policies import policies
from model.road import Road


def update_cars(policy=policies.AVERAGE):
    alpha = 5000
    def get_neigh(i):
        if i == 0:
            return 1
        if i == len(road)-1:
            return i - 2
        if random.random() < 0.5:
            return i-1
        else:
            return i+1
    avg_price = road.avg_price
    for i, s in enumerate(road):
        tomove = []
        for ic, car in enumerate(s.cars):
            neigh = get_neigh(i)
            if policy == policies.LEGACY:
                diff = (s.price - road[neigh].price)/s.price
            if policy == policies.AVERAGE:
                diff = (avg_price - road[neigh].price) / s.price
            if diff > 0:
                tomove.append((ic, neigh))
                continue
            elif random.random() < math.exp(alpha * diff):
                tomove.append((ic, neigh))
                continue
                
        _removed = 0
        for _car in tomove:
            car = s.cars[_car[0]-_removed]
            road[_car[1]].cars.append(car)
            s.cars.pop(_car[0]-_removed)
            _removed +=1

def update_stations():
    road.update()

def run(policy=policies.LEGACY):
    global road
    global N_cars
    global N_Stations
    global T
    
    N_Stations = 100
    N_cars = 1000
    T = range(60)
    observables = {}
    observables["prices"]=[]
    observables["avg_price"]=[]
    road = Road(N_Stations)

    print([round(s.price,2) for s in road])
    print([len(s) for s in road])

    for t in T:
        update_cars(policy=policy)
        update_stations()
        observables["prices"].append(road.prices)
        
    print([round(s.price,2) for s in road])
    print([len(s) for s in road])

    observables["road"] = road

    return observables


observables = run(policy=policies.AVERAGE)
observables_legacy = run(policy=policies.LEGACY)

fig = make_subplots(1, 2)

#price vs T

stat_f = median
stat_dev = lambda x: (max(x)-min(x))/2

fig.add_scatter(x=list(T), y=[stat_f(p)for p in observables["prices"]],
                #error_y={"type": "data", "array": [
                #    stat_dev(p) for p in observables["prices"]]},
                line={"color": "red"},
                row=1, col=1, name="average_new_policy")

fig.add_scatter(x=list(T), y=[stat_f(p)for p in observables_legacy["prices"]],
                #error_y={"type": "data", "array": [
                #    stat_dev(p) for p in observables_legacy["prices"]]},
                line={"color":"blue"},
                row=1, col=1, name="average")


for i in range(len(road)):
    fig.add_scatter(x=list(T), y=[p[i] for p in observables["prices"]], opacity=0.1, line_color="gray", mode="lines", row=1, col=1)


fig.update_xaxes(title="Time", row=1, col=1)
fig.update_yaxes(title="price", row=1, col=1)

fig.update_xaxes(title="price", row=1, col=2)
fig.update_yaxes(title="number of cars", row=1, col=2)


#cars vs T
fig.add_scatter(
            x=[s.price for s in observables["road"]],
            y=[len(s) for s in observables["road"]], 
            marker={"color": "red"},
            mode="markers",
            row=1, col=2)

fig.add_scatter(
    x=[s.price for s in observables_legacy["road"]],
    y=[len(s) for s in observables_legacy["road"]],
    mode="markers",
    marker={"color":"blue"},
    row=1, col=2)
    
fig.show()

