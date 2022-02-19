import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

prices = []
dates = []

with open("inference/data/pp-2018.csv") as r:
    for line in r.readlines():
        spl = line.split(",")
        prices.append(float(spl[1][1:-1]))
        dates.append(datetime.strptime(spl[2][1:-1], "%Y-%m-%d %H:%M"))
prices = np.array(prices)

plt.hist(np.log(prices), bins=64)
plt.show()
