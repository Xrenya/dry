import pickle

def save_obj(obj, filename):
  with open(f"{filename}.pkl", "wb") as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
  with open(f"{name}.pkl", "rb") as f:
    return pickle.load(f)
