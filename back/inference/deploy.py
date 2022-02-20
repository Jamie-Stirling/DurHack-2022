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
        with open("back/inference/models/group.bin", "rb") as file:
            self.group_model = pickle.load(file)
    
    def valuate(self, property_data):
        if property_data["district"] not in self.group_model:
            group_mean, group_std = self.group_model[remove_numeric(property_data["district"])]
        else:
            group_mean, group_std = self.group_model[property_data["district"]]
        
        linear_estimate = self.linear_model.predict([property_data["x"]])[0]
        print(property_data["x"])

        mean =  (group_mean / group_std + linear_estimate / 0.683409027789194) / (1/group_std+1/0.683409027789194)

        std = 1/(1/group_std + 1/0.683409027789194) 
        print(mean, std)

        #combine estimates
        return np.exp(mean - std), np.exp(mean + std)




