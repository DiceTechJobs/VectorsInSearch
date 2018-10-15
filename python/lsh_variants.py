import numpy

def generate_random_vector(shape):
    v = numpy.random.normal(loc=0.0, scale=0.2, size=vecs[0].shape)
    l = numpy.linalg.norm(v)
    return v/l

class LSHHasher(object):
    def __init__(self, num_vectors, vector_shape):
        self.num_vectors = num_vectors
        self.vector_shape = vector_shape
        self.random_vectors = [generate_random_vector(self.vector_shape) for i in range(self.num_vectors)]
        
    def hash_vector(self, vector, num_bits=None, as_str=False):
        if num_bits is None:
            num_bits = self.num_vectors
        assert num_bits <= self.num_vectors, "Can't have more bits than vectors"
        bits = []
        for random_vec in self.random_vectors[:num_bits]:
            cos_sim = np.dot(vector, random_vec)
            hash_bit = +1 if cos_sim >= 0 else -1
            if as_str:
                hash_bit = "+1" if hash_bit == 1 else "-1"
            bits.append(hash_bit)
        return bits