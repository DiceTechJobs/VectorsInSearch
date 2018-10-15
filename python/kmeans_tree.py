import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans

class Labeller(object):
    # get's new node labels
    def __init__(self):
        self.current = -1  # needs to be -1 so first one is 0

    def get_new_node_id(self):
        self.current += 1
        return str(self.current)

class KMeansTree(object):
    ROOT = "ROOT"

    def __init__(self, branch_factor, n_init=15, max_iter=300, n_jobs=1, max_cluster_size=None, verbose=False):
        self.branch_factor = branch_factor
        self.lbl = Labeller()
        self.id2kmeans = dict()  # maps node-id to the kmeans cluster that created it's childen
        self.id2centroid = dict()
        self.n_init = n_init
        self.max_iter = max_iter
        self.tree = {}
        self.nodes = []
        self.vectors = []
        # maps vector indices to cluster node_ids
        self.ix2leaf_node_id = dict()
        self.leaf_nodeid2ixs = dict()
        self.depth_to_node_id = defaultdict(set)
        self.depth_to_node_id[0].add(KMeansTree.ROOT)
        self.id2_depth = dict()
        self.id2_depth[KMeansTree.ROOT] = 0
        self.verbose = verbose
        # for fast sub-tree querying
        self.id2sub_tree = dict()
        self.max_cluster_size = max_cluster_size if max_cluster_size else self.branch_factor
        assert self.max_cluster_size >= self.branch_factor, "Max cluster size must be >= branch_factor"
        # debugging
        self.max_depth = -1

    def is_a_leaf_node(self, node_id):
        return node_id in self.leaf_nodeid2ixs

    def get_subtree_for_node(self, node_id):
        return self.id2sub_tree[node_id]

    def get_leaf_node_for_ix(self, ix):
        assert ix in self.ix2leaf_node_id, "Index {ix} not found".format(ix=ix)
        return self.ix2leaf_node_id[ix]

    # get's all child indices for a node
    def get_indices_for_node(self, node_id):
        if self.is_a_leaf_node(node_id):
            return self.leaf_nodeid2ixs[node_id]
        else:
            indices = []
            for node_id, _ in self.id2sub_tree[node_id].items():
                indices.extend(self.get_indices_for_node(node_id))
            return indices

    def get_leaf_nodes(self):
        return list(self.leaf_nodeid2ixs.keys())

    def get_internal_nodes(self):
        return [node_id for node_id in self.nodes if not self.is_a_leaf_node(node_id)]

    def get_nodes_at_level(self, level):
        return self.depth_to_node_id[level]

    def __add_leaf_node__(self, ixs, parent_node_id, depth):
        if self.verbose:
            print("{indent}L - depth={depth}, size={size}, parent={parent_node_id}".format(
                indent="\t" * depth, size=len(ixs), depth=depth, parent_node_id=parent_node_id))
        self.leaf_nodeid2ixs[parent_node_id] = ixs
        for ix in ixs:
            assert ix not in self.ix2leaf_node_id, "Index already mapped"
            self.ix2leaf_node_id[ix] = parent_node_id
        self.depth_to_node_id[depth].add(parent_node_id)
        return dict()  # return empty dictionary as no children

    def __build_tree__(self, vecs, ixs, parent_node_id, depth):

        if self.verbose and depth > self.max_depth:
            print("New Max Depth={depth}, size={size}".format(depth=depth, size=len(vecs)))
        self.max_depth = max(self.max_depth, depth)

        if len(vecs) <= self.max_cluster_size:
            return self.__add_leaf_node__(ixs=ixs, parent_node_id=parent_node_id, depth=depth)

        if self.verbose:
            print("{indent}I - depth={depth}, size: {size}, parent: {parent_node_id}".format(
                indent="\t" * depth, size=len(vecs), depth=depth, parent_node_id=parent_node_id))
        # TODO - get node id, make recursive, store depth
        km = KMeans(n_clusters=min(self.branch_factor, len(vecs)), n_init=self.n_init, max_iter=self.max_iter)
        km.fit(vecs)
        # store kmeans for later just in case
        self.id2kmeans[parent_node_id] = km

        assert len(km.labels_) == len(vecs), "|labels|  != |vecs|"
        assert len(ixs) == len(vecs), "|indices| != |vecs|"

        # group vectors by cluster labels
        lbl2vecs = defaultdict(list)
        lbl2ixs = defaultdict(list)
        for lbl, ix, vec in zip(km.labels_, ixs, vecs):
            lbl2vecs[lbl].append(vec)
            lbl2ixs[lbl].append(ix)

        lbls = lbl2vecs.keys()
        if len(lbls) == 1:
            # if only one cluster found - items could all be identical (I have found instances of this)
            # make a leaf node
            return self.__add_leaf_node__(ixs=ixs, parent_node_id=parent_node_id, depth=depth)

        tree = {}
        for lbl, child_vecs in lbl2vecs.items():
            child_ixs = lbl2ixs[lbl]
            child_node_id = "{parent_node_id}->{childid}".format(parent_node_id=parent_node_id,
                                                                 childid=self.lbl.get_new_node_id())
            self.nodes.append(child_node_id)
            self.depth_to_node_id[depth + 1].add(child_node_id)
            centroid = km.cluster_centers_[lbl]
            # we need to normalize centroids so we can do np.dot
            norm_centroid = centroid / np.linalg.norm(centroid)
            self.id2centroid[child_node_id] = norm_centroid
            sub_tree = self.__build_tree__(vecs=child_vecs, ixs=child_ixs, parent_node_id=child_node_id,
                                           depth=depth + 1)
            self.id2sub_tree[child_node_id] = sub_tree
            tree[child_node_id] = sub_tree
            
        # build node_id to depth mapping
        for depth, node_ids in self.depth_to_node_id.items():
            for node_id in node_ids:
                self.id2_depth[node_id] = depth
        return tree

    def __build_labels__(self):
        # we have to now map the initial vectors to their leaf clusters, for sklearn structure
        leaf_labeller = Labeller()
        labels_ = []
        leaf_node_labels_ = []  # retain the original labelling scheme
        node2lbl = dict()
        for ix in sorted(self.ix2leaf_node_id.keys()):  # sort just in case hash ordering changes
            parent_node_id = self.ix2leaf_node_id[ix]
            leaf_node_labels_.append(parent_node_id)

            if parent_node_id in node2lbl:
                labels_.append(node2lbl[parent_node_id])
            else:
                new_lbl = int(leaf_labeller.get_new_node_id())
                labels_.append(new_lbl)
                node2lbl[parent_node_id] = new_lbl
        return labels_, leaf_node_labels_

    def fit(self, vecs):
        # get the ixs of the vecs so we can return the labels latter
        self.vectors = vecs
        ixs = np.arange(len(vecs))
        self.tree[KMeansTree.ROOT] = self.__build_tree__(vecs=vecs, ixs=ixs, parent_node_id=KMeansTree.ROOT, depth=0)
        # make sure ROOT is mapped
        self.id2sub_tree[KMeansTree.ROOT] = self.tree[KMeansTree.ROOT]
        self.labels_, self.leaf_node_labels_ = self.__build_labels__()
        assert len(self.labels_) == len(vecs), "|labels| != |vectors|"
