import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

dummy_x = [ [6, 1],
            [5, 0],
            [3, 0],
            [5, 1],
            [2, 0]]

dummy_y = [1350000, 650000, 200000, 400000, 350000]

def train_linear():
    model = LinearRegression()

    model.fit(dummy_x, np.log(dummy_y))

    # TODO: Validate/test, save testing metadata for confidence intervals
    with open("inference/models/linear.bin", "wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    train_linear()
