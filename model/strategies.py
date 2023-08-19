class strategies(Enum):
    UP = lambda x: x+0.1 #min(2, x+0.1)
    STILL = lambda x: x 
    DOWN = lambda x: max(1, x-0.1)   
