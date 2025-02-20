import pickle

def load_model(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)