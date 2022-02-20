import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime

from deploy import remove_numeric

dummy_x = [ [6, 1],
            [5, 0],
            [3, 0],
            [5, 1],
            [2, 0]]

dummy_y = [1350000, 650000, 200000, 400000, 350000]

def prepare_xy(lines):
    x = []
    y = []
    keyword_map = {}
    for line in lines:
        spl = line.split(",")
        price = int(spl[0])
        rooms = int(spl[0])
        x.append([rooms])
        y.append(price)

def train_linear():
    model = LinearRegression()

    model.fit(dummy_x, np.log(dummy_y))

    # TODO: Validate/test, save testing metadata for confidence intervals
    with open("inference/models/linear.bin", "wb") as file:
        pickle.dump(model, file)


def train_groups():
    
    prices = []
    dates = []

    group_model = {}
    groups = {}

    for years in [2018, 2019, 2020, 2021]:
        with open("inference/data/pp-{}.csv".format(years)) as r:
            lines = [l for l in r.readlines()]
            np.random.shuffle(lines)
            for line in lines[:]:
                spl = line.split(",")
                prices.append(float(spl[1][1:-1]))
                dates.append(datetime.strptime(spl[2][1:-1], "%Y-%m-%d %H:%M"))
                postcode = spl[3][1:-1]

                if postcode != "":
                    district = postcode.split(" ")[0]
                    if district not in groups:
                        groups[district] = []
                    groups[district].append(np.log(prices[-1]))
                    superdistrict = remove_numeric(district)

                    if superdistrict not in groups:
                        groups[superdistrict] = []
                    groups[superdistrict].append(np.log(prices[-1]))


    for key in groups:
        if len(groups[key]) >= 2:
            group_model[key] = (np.mean(groups[key]), np.std(groups[key]))

    plt.hist([len(groups[key]) for key in group_model], bins=32)
    plt.show()
    print(group_model)
    prices = np.array(prices)    

    with open("inference/models/group.bin", "wb") as file:
            pickle.dump(group_model, file)

if __name__ == "__main__":
    train_linear()
    train_groups()
