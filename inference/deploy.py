import pickle

class Valuator:
    def __init__(self, model_type="linear"):
        # TODO: Implement more model types
        if model_type == "linear":
            with open("inference/models/linear.bin", "rb") as file:
                self.linear_model = pickle.load(file)
    
    def valuate(self, property_data):
        return 200000 # best estimate

valuator = Valuator()

print(valuator.valuate(None))
