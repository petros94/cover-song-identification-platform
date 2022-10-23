import pickle

def convert_song_doc_to_dto(doc):
    dto = doc.copy()
    dto['_id'] = str(doc['_id'])
    del dto['features']
    del dto['embeddings']
    return dto