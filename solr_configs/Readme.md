# Solr Config Snippets

Due to licensing, I cannot copy the entire solr config and schema xml here. So instead I have just included the snippets needed to enable the solr plugins:

1. **solrcongix.xml**
 - Add the payloadEdismax parser to the solrconfig.xml.
 - Configure the solrconfig.xml to load the plugins jar file
2. **schema.xml**
 - Add the field definitions for the vector field and cluster field types
 - Set the similarity class to schema similarity
