import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

def remove_numeric(s):
    new = ""

    for c in s:
        if c not in "0123456789":
            new += c
        else:
            break
    return "".join(new)


class Valuator:
    def __init__(self, model_type="linear"):
        self.model_type = model_type
        # TODO: Implement more model types
        with open("back/inference/models/linear.bin", "rb") as file:
            self.linear_model = pickle.load(file)
            #print(self.linear_model)
            #print(self.linear_model)
        with open("back/inference/models/group.bin", "rb") as file:
            self.group_model = pickle.load(file)
            #print(self.group_model)
        # added confidence interval model
        with open("back/inference/models/confidence_intervals.bin", "rb") as file:
            self.confidence_intervals_model = pickle.load(file)
            print(self.confidence_intervals_model)
    
    def valuate(self, property_data):
        if property_data["district"] not in self.group_model:
            group_mean, group_std = self.group_model[remove_numeric(property_data["district"])]
        else:
            group_mean, group_std = self.group_model[property_data["district"]]
        
        linear_estimate = self.linear_model.predict([property_data["x"]])[0]

        mean =  (group_mean / group_std + linear_estimate / 0.683409027789194) / (1/group_std+1/0.683409027789194)

        std = 1/(1/group_std + 1/0.6306725040115735) 
        print(mean, std)

        #combine estimates

        lower = np.exp(mean - std)
        upper = np.exp(mean + std)

        #if lower > self.confidence_intervals_model(property_data)
        # wanted to compare the confidence intervals to the upper and lower bounds of the price, but I kept getting the error that;
        # "linear_estimate = self.linear_model.predict([property_data["x"]])[0], KeyError: 'x'"

        return np.exp(mean - std), np.exp(mean + std)




