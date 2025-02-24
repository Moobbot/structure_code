import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from bson import ObjectId

CATEGORIES = ['Biology',
              'Chemistry',
              'Geography',
              'History',
              'Literature',
              'Math',
              'Physics',
              'Science']

MIN_RANK, MAX_RANK = 1, 10
MIN_DIFF, MAX_DIFF = 1, 5


def tfidf_transform(col: pd.Series, prefix=''):
    vectorizer = TfidfVectorizer(tokenizer=lambda x: [x] if isinstance(
        x, str) else x, lowercase=False, vocabulary=CATEGORIES)
    columns = [prefix + c for c in CATEGORIES]
    return pd.DataFrame(vectorizer.fit_transform(col).toarray(), columns=columns), columns


def calculate_performance(time_spent, difficulty, outcome):
    max_time = 60 + 30 * difficulty
    return (1 - time_spent/max_time) * outcome


def calculate_sim_rank_difficulty(rank, difficulty):
    rank_norm = (rank - MIN_RANK) / (MAX_RANK - MIN_RANK)
    diff_norm = (difficulty - MIN_DIFF) / (MAX_DIFF - MIN_DIFF)
    return 1 - np.abs(rank_norm - diff_norm)


def calculate_sim_major_category(A, B):
    return np.sum(A*B, axis=1) / (np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1))

def map_id_ix(ids):
    id_to_ix = {}
    ix_to_id = {}
    for ix, id in enumerate(ids):
        id_to_ix[id] = ix
        ix_to_id[ix] = id
    return id_to_ix, ix_to_id