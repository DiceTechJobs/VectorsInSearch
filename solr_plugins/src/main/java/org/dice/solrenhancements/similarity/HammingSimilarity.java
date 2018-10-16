
package org.dice.solrenhancements.similarity;

import org.apache.lucene.search.similarities.ClassicSimilarity;

/**
 * Created by simon.hughes on 4/16/14.
 * Turn off all weightings
 */
public class HammingSimilarity extends ClassicSimilarity {

    @Override
    public float tf(float freq) {

        if(freq > 0)
        {
            return 1;
        }
        else {
            return 0;
        }
    }

    @Override
    public float lengthNorm(int length)
    {
        return 1;
    }

    @Override
    public float sloppyFreq(int distance)
    {
        return 1.0f;
    }

    @Override
    public float idf(long docFreq, long numDocs)
    {
        return 1.0f;
    }
}
