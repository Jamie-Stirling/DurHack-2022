import pickle
import numpy as np
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
from datetime import datetime

try:
    from inference.deploy import remove_numeric
except:
    from deploy import remove_numeric


def encode_x(bedrooms, keywords, keyword_map):
    arr = [0] * len(keyword_map)
    for keyword in keywords:
        keyword = keyword.lower()
        if keyword in keyword_map:
            arr[keyword_map[keyword]] = 1
    return np.array([(float(bedrooms) * 0.2 + 3.2 * 0.8)] + arr)

def prepare_xy(lines):
    x = []
    y = []
    keyword_map = {}
    lines = [line for line in lines]
    for line in lines:
        spl = line.split(",")
        price = int(spl[0])
        rooms = int(spl[1])
        keywords = spl[2:]
        for keyword in keywords:
            keyword = keyword.lower()
            if keyword not in keyword_map:
                keyword_map[keyword] = len(keyword_map)
        # encode binary features
    for line in lines:
        spl = line.split(",")
        keywords = spl[2:]
        x.append(encode_x(rooms, keywords, keyword_map))
        
        price = int(spl[0])
        y.append(price)
    # dump keyword map
    with open("back/inference/models/keywords.bin", "wb") as file:
        pickle.dump(keyword_map, file)
    return np.array(x), np.array(y)

def train_linear():
    model = MLPRegressor((15), max_iter=1000)
    with open("data.csv") as r:
        x,y = prepare_xy(r.readlines())
    val_split = int(len(x) * 0.8)
    x_train, y_train = x[:val_split], y[:val_split]
    
    x_val, y_val = x[val_split:], y[val_split:]

    
    model.fit(x_train, np.log(y_train), )
    val_error = np.sqrt(np.mean((np.log(y_val) - model.predict(x_val)) ** 2))
    print(val_error)

    # TODO: Validate/test, save testing metadata for confidence intervals
    with open("back/inference/models/linear.bin", "wb") as file:
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
    print("trained")
