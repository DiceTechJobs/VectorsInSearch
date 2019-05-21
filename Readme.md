# Vectors in Search

Dice.com code for implementing the ideas discussed in the folowing talks:
 
* [Vectors in Search](https://sched.co/FkM3)  - [Activate 2018 conference](), by Simon Hughes ( Chief Data Scientist, Dice.com )

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

## Tutorial
I will add a notebook shortly that outlines how to use this code to load and search vectors efficiently within solr.

## Links

* **Activate 2018: 'Vectors in Search'**
  * [Slides](https://www.slideshare.net/lucidworks/vectors-in-search-towards-more-semantic-matching-simon-hughes-dicecom?qid=4c9af9c0-0554-4251-bd47-9345ff508569&v=&b=&from_search=2)
  * [Video](https://www.youtube.com/watch?v=rSDqhGn_8Zo&list=PLU6n9Voqu_1HW8-VavVMa9lP8-oF8Oh5t&index=21&t=56s)

