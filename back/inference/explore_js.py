import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

prices = []
dates = []

group_model = {"DH1":(2321,2214)}
groups = {}

for years in [2018, 2019, 2020, 2021]:
    with open("inference/data/pp-{}.csv".format(years)) as r:
        lines = [l for l in r.readlines()]
        np.random.shuffle(lines)
        for line in lines[:20000]:
            spl = line.split(",")
            prices.append(float(spl[1][1:-1]))
            dates.append(datetime.strptime(spl[2][1:-1], "%Y-%m-%d %H:%M"))
            postcode = spl[3][1:-1]

            if postcode != "":
                firsthalf = postcode.split(" ")[0]
                if firsthalf not in groups:
                    groups[firsthalf] = []
                groups[firsthalf].append(prices[-1])

for key in groups:
    group_model[key] = (np.mean(groups[key]), np.std(groups[key]))

print(group_model)