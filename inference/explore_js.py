import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

prices = []
dates = []

group_model = {"DH1":(2321,2214)}

for years in [2018, 2019, 2020, 2021]:
    with open("inference/data/pp-{}.csv".format(years)) as r:
        lines = [l for l in r.readlines()]
        np.random.shuffle(lines)
        for line in lines[:2000]:
            spl = line.split(",")
            prices.append(float(spl[1][1:-1]))
            dates.append(datetime.strptime(spl[2][1:-1], "%Y-%m-%d %H:%M"))

prices = np.array(prices)
