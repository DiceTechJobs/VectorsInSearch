# Vectors in Search

Dice.com code for implementing the ideas discussed in the [Vectors in Search](https://sched.co/FkM3) talk from the Activate 2018 conference.

## Directory Structure
- **python**
  - Code for implementing the k-means tree and vector thresholding algorithms, and indexing and searching vectors in solr using these techniques.
- **solr_vectors_in_search_plugins**
  - Java code for implementing the custom similarity classes and payloadEdismax parser described in the talk.
- **solr_configs**
  - Xml snippets for importing the solr plugins from the 'solr_vectors_in_search_plugins' java code.

## Implementation Details
- Solr Version - 7.5
- Python Version - 3.x+ (3.5 used)
