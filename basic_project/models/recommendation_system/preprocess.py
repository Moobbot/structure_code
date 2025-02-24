import os
import sys
import numpy as np
import pandas as pd
import scipy.sparse as sparse
from bson import ObjectId

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(project_root)
from recommendation_system.base_preprocessing import BasePreprocessing
from recommendation_system.helper import (
    calculate_performance,
    calculate_sim_major_category,
    calculate_sim_rank_difficulty,
    map_id_ix,
    tfidf_transform,
)

class Preprocess(BasePreprocessing): 
    # def __init__(self,
    #              question_id_to_ix: dict[ObjectId, int],
    #              ix_to_question_id: dict[int, ObjectId],
    #              player_id_to_ix: dict[ObjectId, int],
    #              ix_to_player_id: dict[int, ObjectId],
    #              observation_players: np.ndarray,
    #              observation_questions: np.ndarray,
    #              observations: np.ndarray):
    #     self.question_id_to_ix = question_id_to_ix
    #     self.ix_to_question_id = ix_to_question_id
    #     self.player_id_to_ix = player_id_to_ix
    #     self.ix_to_player_id = ix_to_player_id
    #     self.observation_players = observation_players
    #     self.observation_questions = observation_questions
    #     self.observations = observations
    #     self.sparse_matrix = None
    
    def __init__(self):
        self.question_id_to_ix = None
        self.ix_to_question_id = None
        self.player_id_to_ix = None
        self.ix_to_player_id = None
        self.observation_players = None
        self.observation_questions = None
        self.observations = None
        self.sparse_matrix = None

    def n_users(self):
        return len(self.player_id_to_ix)

    def n_items(self):
        return len(self.question_id_to_ix)

    def get_player_id(self, ix):
        return self.ix_to_player_id[ix]

    def get_question_id(self, ix):
        return self.ix_to_question_id[ix]

    def get_player_ix(self, id):
        return self.player_id_to_ix[id]

    def get_question_ix(self, id):
        return self.question_id_to_ix[id]
    
    def preprocess(self, player_data, question_data, interaction_data):
        player_ids = interaction_data['player_id'].unique().tolist()
        self.player_id_to_ix, self.ix_to_player_id = map_id_ix(player_ids)

        question_ids = interaction_data['question_id'].unique().tolist()
        self.question_id_to_ix, self.ix_to_question_id = map_id_ix(question_ids)

        major_tfidf, major_cols = tfidf_transform(
            player_data['major'], 'player_')
        category_tfidf, category_cols = tfidf_transform(
            question_data['category'], 'question_')
        
        player_data = pd.concat([player_data, major_tfidf], axis=1)
        player_data.drop('major', axis=1, inplace=True)

        question_data = pd.concat([question_data, category_tfidf], axis=1)
        question_data.drop('category', axis=1, inplace=True)

        # Merge player_data with interaction_data on _id and player_id
        merged_data = pd.merge(player_data, interaction_data,
                               left_on='_id', right_on='player_id')
        # Merge with question_data on question_id
        merged_data = pd.merge(merged_data, question_data,
                               left_on='question_id', right_on='_id')
        # Drop redundant columns
        merged_data.drop(['_id_x', '_id_y'], axis=1, inplace=True)

        del interaction_data, player_data, question_data, major_tfidf, category_tfidf

        return merged_data, major_cols, category_cols

    def fit(self, player_data, question_data, interaction_data):
        merged_data, major_cols, category_cols = self.preprocess(player_data, question_data, interaction_data)
        rating = self.__calculate_rating(merged_data, major_cols, category_cols)
        self.observation_players=merged_data['player_id'].map(
            self.player_id_to_ix).to_list(),
        self.observation_questions=merged_data['question_id'].map(
            self.question_id_to_ix).to_list(),
        self.observations=rating.tolist()
        self.sparse_matrix=self.__build_sparse_matrix()
        
    def get_sparse_matrix(self):
        return self.sparse_matrix

    def __build_sparse_matrix(self):
        return sparse.csr_matrix(
            (
                self.observations,
                (self.observation_players,
                 self.observation_questions),
            )
        )
    
    def __calculate_rating(self, data, major_cols, category_cols):
        rating = 0.2 * calculate_performance(data['time'].to_numpy(),
                                             data['difficulty'].to_numpy(
        ),
            data['outcome'].to_numpy()) \
            + 0.3 * calculate_sim_rank_difficulty(data['rank'].to_numpy(),
                                                  data['difficulty'].to_numpy()) \
            + 0.5 * calculate_sim_major_category(data[major_cols].to_numpy(),
                                                 data[category_cols].to_numpy())
        
        return rating