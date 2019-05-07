from engine.db.contexts.context import *
from engine.db.index import *

_contexts = db[MONGODB_CONFIG['col_contexts']]


def create_insert(text, subject):
    documnet = convert_to_document(text, subject)
    return insert(documnet)


def insert(document):
    return _contexts.update_one({'subject': document['subject']},
                                {'$set': document}, upsert=True)


def find_all():
    contexts = _contexts.find({})
    return contexts
    # return list(map(convert_to_context, contexts))
