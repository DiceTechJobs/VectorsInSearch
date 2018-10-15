import numpy as np
from queue import PriorityQueue
from kmeans_tree import KMeansTree

class BruteForceSearcher(object):
    """
    Does a brute force k-nn search. This is our gold standard, we want to get close to this in terms of accuracy
    But be must faster
    """

    def __init__(self, km_tree):
        self.km_tree = km_tree
        self.vecs = km_tree.vectors
        self.stacked_vecs = np.vstack(self.vecs)

    def search(self, vector, k_neighbors=10):
        # compute sims
        dot_prod = np.dot(vector.reshape(1, len(vector)), self.stacked_vecs.T)
        dot_prod = dot_prod[0, :]
        ixs = np.argsort(dot_prod)[::-1]  # reverse order so in best to worse
        top_ixs = ixs[:k_neighbors]
        result = []
        for ix in top_ixs:
            sim = dot_prod[ix]
            result.append((sim, ix))
        return result

class BestBinFirstSearcher(object):
    def __init__(self, km_tree, default_max_points_to_search=100):
        self.km_tree = km_tree
        self.default_max_points_to_search = default_max_points_to_search

    def __compute_similarity__(self, vec1, vec2):
        return np.dot(vec1, vec2)

    def __compute_similarity__(self, vec1, vec2):
        return np.dot(vec1, vec2)

    def __find_best_leaf_node__(self, parent_node_id, vector, q):
        # This can happen im the while loop if nodes pushed on the q are leaf nodes
        if self.km_tree.is_a_leaf_node(parent_node_id):
            leaf_centroid = self.km_tree.id2centroid[parent_node_id]
            cosine_sim = self.__compute_similarity__(vector, leaf_centroid)
            # print("Best node: {node} with sim: {sim}".format(node=parent_node_id, sim=cosine_sim))
            return -cosine_sim, parent_node_id

        sub_tree = self.km_tree.get_subtree_for_node(parent_node_id)
        if len(sub_tree) == 0:
            raise Exception("Sub tree should not be empty")

        tmp_q = PriorityQueue()
        for child_node_id, child_sub_tree in sub_tree.items():
            centroid = self.km_tree.id2centroid[child_node_id]
            cosine_sim = self.__compute_similarity__(vector, centroid)
            # NOTE - this is a min heap, so returns the lowest value, so negate
            tmp_q.put((-cosine_sim, child_node_id))

        # pop the top sim and node from the tmp priority q
        best_sim, best_node = tmp_q.get()
        # we need to add the items here so they don't include the current best node
        # which we just popped and removed - we only want the remaining nodes
        while not tmp_q.empty():
            # the get above removes the top item, which is the only reason this part of the code exists
            q.put(tmp_q.get())

        if self.km_tree.is_a_leaf_node(best_node):
            # negative as it was negated when added to the queue
            # print("Best node: {node} with sim: {sim}".format(node=best_node, sim=best_sim))
            return best_sim, best_node
        else:
            return self.__find_best_leaf_node__(best_node, vector, q)

    def __add_neighbors_from_leaf_node_to_q__(self, leaf_node_id, vector, result_ix_q):
        ixs = self.km_tree.leaf_nodeid2ixs[leaf_node_id]
        for ix in ixs:
            cosine_sim = self.__compute_similarity__(vector, self.km_tree.vectors[ix])
            result_ix_q.put((-cosine_sim, ix))
        return len(ixs)
    
    def search_best_leaf_nodes(self, vector, max_nodes_to_search=30, k_neighbors=None):
        if k_neighbors is not None:
            assert max_nodes_to_search >= k_neighbors, "Max Nodes must be >= k neighbors"
        # this contains -sim, node_id pairs
        q = PriorityQueue()
        nodes_searched = 0
        # this contains -sim, ix pairs, unlike q
        result_node_q = PriorityQueue()

        matching_docs = 0
        best_sim, best_node = self.__find_best_leaf_node__(KMeansTree.ROOT, vector, q)
        result_node_q.put((best_sim, best_node))
        matching_docs += len(self.km_tree.get_indices_for_node(best_node))
        nodes_searched += 1

        while not q.empty() and (nodes_searched < max_nodes_to_search or 
                                 (k_neighbors is not None and matching_docs < k_neighbors)):
            _, next_best_point = q.get()
            best_sim, best_node = self.__find_best_leaf_node__(next_best_point, vector, q)
            result_node_q.put((best_sim, best_node))
            matching_docs += len(self.km_tree.get_indices_for_node(best_node))
            nodes_searched += 1

        best_nodes = []
        while not result_node_q.empty():
            sim, node = result_node_q.get()
            # reverse similarity
            best_nodes.append((-sim, node))
        return best_nodes

    def search_subtree(self, vector):
        # for a vector, find the best leaf node, and then return all the nodes along that route, in sim order
        # this contains -sim, node_id pairs
        q = PriorityQueue()
        # this contains -sim, ix pairs, unlike q
        best_sim, best_node = self.__find_best_leaf_node__(KMeansTree.ROOT, vector, q)

        sub_tree_nodes = []
        while not q.empty():
            sim, node = q.get()
            # reverse similarity
            sub_tree_nodes.append((-sim, node))
        return sub_tree_nodes

    def search(self, vector, k_neighbors=10, max_points_to_search=None):
        if max_points_to_search is None:
            max_points_to_search = self.default_max_points_to_search

        assert max_points_to_search >= k_neighbors, \
            "Max Points to Search must be >= k neighbors. max={max}, k-neighbors={k_neighbors}".format(
                max=max_points_to_search, k_neighbors=k_neighbors
            )
        # this contains -sim, node_id pairs
        q = PriorityQueue()
        points_searched = 0
        # this contains -sim, ix pairs, unlike q
        result_ix_q = PriorityQueue()

        best_sim, best_node = self.__find_best_leaf_node__(KMeansTree.ROOT, vector, q)

        num_added = self.__add_neighbors_from_leaf_node_to_q__(best_node, vector, result_ix_q)
        points_searched += num_added

        while not q.empty() and points_searched < max_points_to_search:
            _, next_best_point = q.get()
            _, best_node = self.__find_best_leaf_node__(next_best_point, vector, q)
            num_added = self.__add_neighbors_from_leaf_node_to_q__(best_node, vector, result_ix_q)
            points_searched += num_added

        k_best = []
        while not result_ix_q.empty() and len(k_best) < k_neighbors:
            sim, ix = result_ix_q.get()
            # reverse similarity sign
            k_best.append((-sim, ix))
        return k_best
    
    def __find_best_node__(self, parent_node_id, vector, q, depth, max_depth):
        
        # This can happen im the while loop if nodes pushed on the q are leaf nodes
        if self.km_tree.is_a_leaf_node(parent_node_id) or depth >= max_depth:
            centroid = self.km_tree.id2centroid[parent_node_id]
            cosine_sim = self.__compute_similarity__(vector, centroid)
            # print("Best node: {node} with sim: {sim}".format(node=parent_node_id, sim=cosine_sim))
            return -cosine_sim, parent_node_id

        sub_tree = self.km_tree.get_subtree_for_node(parent_node_id)
        if len(sub_tree) == 0:
            raise Exception("Sub tree should not be empty")

        tmp_q = PriorityQueue()
        for child_node_id, child_sub_tree in sub_tree.items():
            centroid = self.km_tree.id2centroid[child_node_id]
            cosine_sim = self.__compute_similarity__(vector, centroid)
            # NOTE - this is a min heap, so returns the lowest value, so negate
            tmp_q.put((-cosine_sim, child_node_id))

        # pop (i.e. REMOVE) the top sim and node from the tmp priority q
        best_sim, best_node = tmp_q.get()        
        # we need to add the items here so they don't include the current best node
        # which we just popped and removed - we only want the remaining nodes
        while not tmp_q.empty():
            # the get above removes the top item, which is the only reason this part of the code exists
            q.put(tmp_q.get())

        return self.__find_best_node__(best_node, vector, q, depth=depth+1, max_depth=max_depth)

    def search_best_nodes(self, vector, max_nodes_to_search=30, max_depth=None):
        if max_depth is None:
            max_depth = self.km_tree.max_depth            
        assert max_depth > 0, "Max depth has to be at least 1"
        q = PriorityQueue()
        nodes_searched = 0
        # this contains -sim, ix pairs, unlike q
        result_node_q = PriorityQueue()

        matching_docs = 0
        best_sim, best_node = self.__find_best_node__(KMeansTree.ROOT, vector, q, depth=0, max_depth=max_depth)
        result_node_q.put((best_sim, best_node))
        nodes_searched += 1

        while not q.empty() and nodes_searched < max_nodes_to_search :
            _, next_best_point = q.get()
            node_depth = self.km_tree.id2_depth[next_best_point]
            best_sim, best_node = self.__find_best_node__(next_best_point, vector, q, depth=node_depth, max_depth=max_depth)
            result_node_q.put((best_sim, best_node))            
            nodes_searched += 1

        best_nodes = []
        while not result_node_q.empty():
            sim, node = result_node_q.get()
            # reverse similarity
            best_nodes.append((-sim, node))
        return best_nodes
