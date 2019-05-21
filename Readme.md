# Vectors in Search

Dice.com code for implementing the ideas discussed in the following talks:

* 'Vectors in Search' - [Activate 2018 conference](https://activate-conf.com/more-events/)
* 'Searching with Vectors' - [Haystack 2019 conference](https://haystackconf.com/2019/vectors/)

This extends my earlier work on 'Conceptual Search' which can be found here - https://github.com/DiceTechJobs/ConceptualSearch (including slides and video links). In this talk, I present a number of different approaches for searching vectors at scale using an inverted index. This implements approaches to [Approximate k-Nearest Neighbor Search](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximate_nearest_neighbor) including:

- LSH (using the Sim Hash)
- K-Means Tree
- Vector Thresholding

and describes how these ideas can be implemented and queried efficiently within an inverted index.

**UPDATE:**
After talking with [Trey Grainger](https://www.linkedin.com/in/treygrainger/) and [Erik Hatcher](https://www.linkedin.com/in/erik-hatcher-94820/) from LucidWorks, they recommended using term frequency in place of payloads for the solutions where I embed term weights into the index and use a special payload aware similarity function (which would also not be needed). Payloads incur a significant performance penalty. The challenge with this is the negative weights, I assume it is not possible to encode negative term frequencies, but this can be worked around by having different tokens for positive and negative weighted tokens, and making similar adjustments at query time (where negative boosts can be applied in Solr as needed).

Lucene Documentation: [Lucene Delimited Term Frequency Filter](https://lucene.apache.org/core/7_0_0/analyzers-common/org/apache/lucene/analysis/miscellaneous/DelimitedTermFrequencyTokenFilter.html)

There has also been a recent update to Lucene core that is applicable here and is soon to make it's way into Elastic search at time of writing: [Block Max WAND](https://www.elastic.co/blog/faster-retrieval-of-top-hits-in-elasticsearch-with-block-max-wand). This produces a signifcant speed up for large boolean OR queries where you don't need to know the exact number of results but just care about getting the top-N results as fast as possible. All of the approaches I discuss here generate relatively large OR queries and so this is very relevant. I have also read that the current implementation of minimum-should-match also includes similar optimizations, and so the same sort of performance gain may already be attained using appropriate mm settings, something that I was already experimenting with in my code.  

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

## Links to Talks

* **Activate 2018:** 'Vectors in Search'
  * [Slides](https://www.slideshare.net/lucidworks/vectors-in-search-towards-more-semantic-matching-simon-hughes-dicecom?qid=4c9af9c0-0554-4251-bd47-9345ff508569&v=&b=&from_search=2)
  * [Video](https://www.youtube.com/watch?v=rSDqhGn_8Zo&list=PLU6n9Voqu_1HW8-VavVMa9lP8-oF8Oh5t&index=21&t=56s)

* **Haystack 2019:** 'Searching with Vectors'
  * [Slides](https://www.slideshare.net/o19s/haystack-2019-search-with-vectors-simon-hughes)
  * [Video](https://www.youtube.com/watch?v=hycH6Rn4RaU&list=PLCoJWKqBHERu9Fe0W12D7XKwGT2eoJJNU&index=19)

## Author
Simon Hughes ( Chief Data Scientist, Dice.com )
* LinkedIn - https://www.linkedin.com/in/simon-hughes-data-scientist/
* Twitter - https://twitter.com/hughes_meister  