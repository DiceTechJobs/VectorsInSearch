# Indexing functions
def solr_encode_vector(vector):
    tokens = ["{i}|{val}".format(i=i, val=val) for i, val in enumerate(vector)]
    return " ".join(tokens)

def solr_encode_sparse_vector(vector):
    tokens = ["{i}|{val}".format(i=i, val=val) for i, val in enumerate(vector) if val != 0.0]
    return " ".join(tokens)

# encodes sparse vector as tokens, including weights
def solr_encode_quantize_sparse_vector(vector, decimal_places=2):
    tokens = ["{i}_{dp}dp_{sign}_{val}".format(i=i, dp=decimal_places, 
                                               sign="neg" if val < 0 else "pos", 
                                               val=round(abs(val),decimal_places)) 
              for i, val in enumerate(vector) if val != 0.0]
    
    return tokens

def solr_encode_hash_finger_print(hash_vector):
    return ["".join(map(lambda s: str(s).rjust(2, '+'), hash_vector))]

# Query functions
def __tokens_to_field_query__(field, stokens):
    return "{field}:({stokens})".format(field=field, stokens=stokens)

def __build_field_query__(field, vector, sparse=True):
    stokens = " ".join(["{i}^{val}".format(field=field, i=i, val=val) 
                        for i, val in enumerate(vector) if (sparse and val != 0.0) or not sparse])
    return __tokens_to_field_query__(field, stokens)

def solr_encode_vector_for_query(vector, field):
    return __build_field_query__(field, vector, sparse=False)

def solr_encode_sparse_vector_for_query(vector, field):
    return __build_field_query__(field, vector, sparse=True)

def __tokenize_vector_component__(i, val, decimal_places):
    rounded_val = round(abs(val),decimal_places)
    return "{i}_{dp}dp_{sign}_{val}".format(i=i, dp=decimal_places, 
                                            sign="neg" if val < 0 else "pos", 
                                            val=rounded_val)

# encodes sparse vector as tokens, including weights
def solr_encode_quantize_sparse_vector_for_query(vector, field, decimal_places=2):
    stokens = " ".join(["{i}_{dp}dp_{sign}_{val}".format(i=i, dp=decimal_places, 
                                               sign="neg" if val < 0 else "pos", 
                                               val=round(abs(val),decimal_places)) 
              for i, val in enumerate(vector) if val != 0.0])
    
    return __tokens_to_field_query__(field, stokens)

def solr_encode_hash_finger_print_for_query(hash_vector, field):
    finger_prints = solr_encode_hash_finger_print(hash_vector)
    assert len(finger_prints) == 1, "Should only be one finger print"
    return __tokens_to_field_query__(field, "\"" + finger_prints[0] + "\"")
