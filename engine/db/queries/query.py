import pickle

import numpy as np

from engine.db.questions.index import find_by_text


class Query(object):  # TODO 어떤 정보가 필요 할 지 계속 고민 해보기
    def __init__(self, chat, feature_vector, keywords,
                 matched_question, manhattan_similarity,
                 jaccard_similarity, category=None):
        self.chat = chat
        self.feature_vector = feature_vector
        self.keywords = keywords
        self.matched_question = matched_question  # 어떤 질문과 매칭 되었었는지.
        self.manhattan_similarity = manhattan_similarity  # 거리는 어떠 하였는 지
        self.jaccard_similarity = jaccard_similarity
        self.category = category

    def __str__(self):
        return 'Query chat:%5s, keywords%10s, question:%5s, feature_distance:%5.3f, jaccard_distance:%5.3f' \
               % (self.chat, self.keywords, self.matched_question.text, self.manhattan_similarity,
                  self.jaccard_similarity)


def convert_to_query(document):
    feature_vector = pickle.loads(np.array(document['feature_vector']))
    matched_question = find_by_text(document['matched_question'])
    query = Query(document['chat'], feature_vector, document['keywords'],
                  matched_question, document['manhattan_similarity'], document['jaccard_similarity'])
    return query


def convert_to_document(query):
    query.feature_vector = pickle.dumps(query.feature_vector)
    query.matched_question = query.matched_question.text
    return query.__dict__
