# Vectors in Search

Dice.com code for implementing the ideas discussed in the [Vectors in Search](https://sched.co/FkM3) talk from the Activate 2018 conference, by Simon Hughes ( Chief Data Scientist, Dice.com ), and my later talk ['Searching with Vectors'](https://haystackconf.com/2019/vectors/) from the [HayStack Conference](https://haystackconf.com) in 2019. This extends my earlier work on 'Conceptual Search' which can be found here - https://github.com/DiceTechJobs/ConceptualSearch (including slides and video links). In this talk, I present a number of different approaches for searching vectors at scale using an inverted index. This implements approaches to [Approximate k-Nearest Neighbor Search](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximate_nearest_neighbor) including:

- LSH (using the Sim Hash)
- K-Means Tree
- Vector Thresholding

and describes how these ideas can be implemented and queried efficiently within an inverted index.

## Directory Structure
- **python**
  - Code for implementing the k-means tree, LSH sim hash and vector thresholding algorithms, and indexing and searching vectors in solr using these techniques.
- **solr_plugins**
  - Java code for implementing the custom similarity classes and payloadEdismax parser described in the talk.
- **solr_configs**
  - Xml snippets for importing the solr plugins from the 'solr_vectors_in_search_plugins' java code.

## Implementation Details
- Solr Version - 7.5
- Python Version - 3.x+ (3.5 used)

## Links
* [Slides from the talk](https://www.slideshare.net/lucidworks/vectors-in-search-towards-more-semantic-matching-simon-hughes-dicecom)
* [Video of the Talk](https://www.youtube.com/watch?v=rSDqhGn_8Zo&list=PLU6n9Voqu_1HW8-VavVMa9lP8-oF8Oh5t&index=20&t=0s)

