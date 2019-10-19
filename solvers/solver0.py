import re
import os
import random
from string import punctuation


class Solver(object):

    def __init__(self, seed=42, data_path='data/'):
        self.is_train_task = False
        self.seed = seed
        self.init_seed()


    def init_seed(self):
        random.seed(self.seed)

    def predict(self, task):
        return None


    def fit(self, tasks):
        pass

    def load(self, path="data/models/solver4.pkl"):
        pass

    def save(self, path="data/models/solver4.pkl"):
        pass

    def predict_from_model(self, a):
        return []

