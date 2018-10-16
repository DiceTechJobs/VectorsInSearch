    <field name="vector" type="vector" indexed="true" stored="true" omitNorms="true" multiValued="true" docValues="false"/>
    <dynamicField name="vector_*" type="vector" indexed="true" stored="true" omitNorms="true" multiValued="true" docValues="false"/> 
    
	<fieldType name="vector" class="solr.TextField" positionIncrementGap="100" autoGeneratePhraseQueries="false">
		<analyzer>
			<tokenizer class="solr.WhitespaceTokenizerFactory"/>			
			<filter class="solr.TrimFilterFactory" />									
			<!-- extract payloads -->
			<filter class="solr.DelimitedPayloadTokenFilterFactory" encoder="float" delimiter="|"/>						
		</analyzer>		
		<!-- Custom similarity class that recognizes payloads and ignores tf and idf for this field -->
        <!-- Define <similarity class="solr.SchemaSimilarityFactory"/> as the similarity class in your schema.xml to configure per field type similarity -->
		<similarity class="org.dice.solrenhancements.similarity.PayloadOnlySimilarity"/>
	</fieldType>
	
	
	
	<field name="clusters" type="cluster" indexed="true" stored="true" omitNorms="true" multiValued="true" omitTermFreqAndPositions="true"/>
	<dynamicField name="cluster_*" type="cluster" indexed="true" stored="true" omitNorms="true" multiValued="true" omitTermFreqAndPositions="true"/>
	<dynamicField name="tokens_*"  type="cluster" indexed="true" stored="true" omitNorms="true" multiValued="true" omitTermFreqAndPositions="true"/>
	
	<fieldType name="cluster" class="solr.TextField" positionIncrementGap="100" autoGeneratePhraseQueries="false">
		<analyzer>
			<tokenizer class="solr.WhitespaceTokenizerFactory"/>			
			<filter class="solr.TrimFilterFactory" />			
		</analyzer>
		<!-- Custom similarity class that ignores length norms, tf and idf for this field -->
        <!-- Define <similarity class="solr.SchemaSimilarityFactory"/> as the similarity class in your schema.xml to configure per field type similarity -->
		<similarity class="org.dice.solrenhancements.similarity.HammingSimilarity"/>
	</fieldType>

	<similarity class="solr.SchemaSimilarityFactory">
		<str name="defaultSimFromFieldType">cluster</str>
	</similarity>

