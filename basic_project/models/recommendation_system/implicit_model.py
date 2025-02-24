import os
import sys
import implicit
from bson import ObjectId
import pickle

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(project_root)

from models.recommendation_system.base_algorithm import BaseAlgorithm
from models.recommendation_system.preprocess import Preprocess


class ImplicitModel(BaseAlgorithm):
    def __init__(self, **kwargs):
        self.model = implicit.als.AlternatingLeastSquares(**kwargs)
        self.dataset = None

    def fit(self, dataset: Preprocess):
        self.dataset = dataset
        sparse_matrix = self.dataset.build_sparse_matrix()
        self.model.fit(sparse_matrix)

    def update(self, new_data):
        # Currently, idk how new data is structured
        pass

    def recommend(self, user_id, n):
        if isinstance(user_id, ObjectId):
            user_ix = self.dataset.get_player_ix(user_id)
        elif isinstance(user_id, list):
            user_ix = [self.dataset.get_player_ix(uid) for uid in user_id]
        else:
            raise ValueError("user_id must be an ObjectId or a list of ObjectId")
        ids, _ = self.model.recommend(
            user_ix,
            self.dataset.get_sparse_matrix()[user_ix],
            N=10,
            filter_already_liked_items=True,
        )
        # if user_id is a single ObjectId
        if ids.ndim == 1:
            return [self.dataset.get_question_id(ix) for ix in ids]
        
        # if user_id is a batch of ObjectId
        result_dict = {}
        for i, uid in enumerate(user_id):
            result_dict[uid] = [self.dataset.get_question_id(ix) for ix in ids[i]]
        return result_dict

    def save(self, path):
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(path):
        with open(path, 'rb') as file:
            return pickle.load(file)