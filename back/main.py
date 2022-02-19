from ..inference.deploy import predict_price_given_rooms

def process_request(data):
    # process the data
    # return the prediction
    return predict_price_given_rooms(data.rooms)