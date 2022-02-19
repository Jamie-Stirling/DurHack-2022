import pickle
import numpy as np

def remove_numeric(s):
    return "".join([c for c in s if c not in "0123456789"])

class Valuator:
    def __init__(self, model_type="linear"):
        self.model_type = model_type
        # TODO: Implement more model types
        if model_type == "linear":
            with open("inference/models/linear.bin", "rb") as file:
                self.linear_model = pickle.load(file)
        if model_type == "postcode":
            with open("inference/models/group.bin", "rb") as file:
                self.group_model = pickle.load(file)
    
    def valuate(self, property_data):
        if self.model_type == "group":
            if property_data["district"] not in self.group_model:
                mean, std = self.group_model[remove_numeric(property_data["district"])]
            else:
                mean, std = self.group_model[property_data["district"]]
                return (np.exp(mean - std), np.exp(mean + std))

valuator = Valuator()

print(valuator.valuate(None))
