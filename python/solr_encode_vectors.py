# Needed for indexing
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

def solr_encode_vector_for_query(vector, field):
    stokens = " ".join(["{i}^{val}".format(field=field, i=i, val=val) for i, val in enumerate(vector)])
    return "{field}:({stokens})".format(field=field, stokens=stokens) 


def solr_encode_sparse_vector_for_query(vector, field):
    stokens = " ".join(["{i}^{val}".format(field=field, i=i, val=val) 
                        for i, val in enumerate(vector) if val != 0.0])
    return "{field}:({stokens})".format(field=field, stokens=stokens) 

# encodes sparse vector as tokens, including weights
def solr_encode_quantize_sparse_vector_for_query(vector, field, decimal_places=2):
    stokens = " ".join(["{i}_{dp}dp_{sign}_{val}".format(i=i, dp=decimal_places, 
                                               sign="neg" if val < 0 else "pos", 
                                               val=round(abs(val),decimal_places)) 
              for i, val in enumerate(vector) if val != 0.0])
    
    return "{field}:({stokens})".format(field=field, stokens=stokens) 