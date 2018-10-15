import numpy as np
from numpy.linalg import norm

def vec2unit_vec(vec):
    return vec / norm(vec)

# thresholds values based on percentiles
#  so values above get set to pos_val, values below get set to neg_val, and in between get set to middle_val
def threshold_vector_by_pct(vector, pct_cutoff=90, pos_val=1, neg_val=-1, middle_val=0):    
    assert pct_cutoff >= 50
    neg_pct_cutoff = 100-pct_cutoff
    
    pos_threshold = np.percentile(vector, pct_cutoff)
    neg_threshold = np.percentile(vector, neg_pct_cutoff)
    
    mod_vec = vector
    mod_vec = np.where(  mod_vec >= pos_threshold,  pos_val, 
                np.where(mod_vec <  neg_threshold,  neg_val, 
                    middle_val))
    return mod_vec

def sparsify_vector_by_pct(vector, pct_cutoff=90):    
    assert pct_cutoff >= 50
    neg_pct_cutoff = 100-pct_cutoff
    
    pos_threshold = np.percentile(vector, pct_cutoff)
    neg_threshold = np.percentile(vector, neg_pct_cutoff)
    
    mod_vec = vector.copy()
    mod_vec[(mod_vec <= pos_threshold) & (mod_vec >= neg_threshold)] = 0
    return mod_vec

# thresholds values based on pct's computed from a population of values
def threshold_vector_by_popn_pct(vector, pct2val, pct_cutoff=90, pos_val=1, neg_val=-1, middle_val=0):    
    assert pct_cutoff >= 50
    neg_pct_cutoff = 100-pct_cutoff
    mod_vec = vector
    mod_vec = np.where(  mod_vec >= pct2val[pct_cutoff],      pos_val, 
                np.where(mod_vec <  pct2val[neg_pct_cutoff],  neg_val, 
                    middle_val))
    return mod_vec

# thresholds values to above (inc.) and below a threshold
def threshold_vector_by_val(vector, cutoff=0, pos_val=1, neg_val=-1):
    mod_vec = vector
    mod_vec = np.where(  mod_vec >= cutoff,  pos_val, neg_val)
    return mod_vec