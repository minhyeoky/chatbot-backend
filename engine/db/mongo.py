import numpy as np
import pickle
from pymongo import MongoClient

import config
from engine.data.question import Question
from engine.utils import Singleton


class PymongoWrapper(metaclass=Singleton):
    def __init__(self):

        self.MONGODB_CONFIG = config.MONGODB_CONFIG

        _client = MongoClient(self.MONGODB_CONFIG['local_ip'], self.MONGODB_CONFIG['port'])
        self._db = _client[self.MONGODB_CONFIG['db_name']]
        self._questions = self._db[self.MONGODB_CONFIG['col_question']]

    def insert_question(self, question):
        '''

        :param question: Question object
        :return: InsertOneResult.inserted_id
        '''

        if question.feature_vector is None:
            raise Exception('feature vector is None')

        feature_vector = pickle.dumps(question.feature_vector)
        morphs = pickle.dumps(question.morphs)

        document = {'text': question.text,
                    'answer': question.answer,
                    'feature_vector': feature_vector,
                    'category': question.category,
                    'morphs': morphs}

        return self._questions.insert_one(document).inserted_id

    def get_question_list(self):
        '''

        :return: list of Question objects
        '''
        questions_list = []
        cursor = self._questions.find({})

        for document in cursor:
            question = self._convert_to_question(document)
            question.object_id = document['_id']
            questions_list.append(question)
        return questions_list

    def get_question_by_id(self, id):
        '''

        :param id:
        :return: Question object
        '''

        pass
    def get_question_by_text(self, text):
        '''

        :param text:
        :return: Question object
        '''
        document = self._questions.find_one({'text': text})
        return self._convert_to_question(document)
    def get_questions_by_category(self, category):
        '''
        :param category:
        :return: list of Question objects
        '''

        questions = []
        cursor = self._questions.find({'category': category})

        for document in cursor:
            question = self._convert_to_question(document)
            questions.append(question)

        return questions
    def delete_question(self, id):
        self._questions.delete_one(({'_id':id}))


    def _convert_to_question(self, document):
        feature_vector = pickle.loads(np.array(document['feature_vector']))
        morphs = pickle.loads(document['morphs'])
        question = Question(document['text'],
                            document['category'],
                            document['answer'],
                            feature_vector,
                            morphs)
        return question

    def delete_duplications(self):
        pass # 중복 텍스트 지우기 # TODO

    def replace_question(self, question):
        pass # TODO


if __name__ == '__main__':
    pw = PymongoWrapper()
