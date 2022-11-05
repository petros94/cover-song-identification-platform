import pickle

def convert_song_doc_to_dto(doc):
    dto = doc.copy()
    dto['_id'] = str(doc['_id'])
    del dto['embeddings']
    del dto['embeddings_seg']
    return dto

def convert_song_doc_to_dto_with_dist(doc, dist, emb):
    dto = doc.copy()
    dto['_id'] = str(doc['_id'])
    dto['dist'] = round(float(dist),3)
    del dto['embeddings']
    del dto['embeddings_seg']
    dto['embeddings'] = emb
    return dto

def convert_song_doc_to_dto_with_dist_cover(doc, dist, emb, cover):
    dto = doc.copy()
    dto['_id'] = str(doc['_id'])
    dto['dist'] = round(float(dist),3)
    dto['is_cover'] = cover
    del dto['embeddings']
    del dto['embeddings_seg']
    dto['embeddings'] = emb
    return dto