'''

Reads in a collection name, a scoring scheme, k, and a keyword query 
and prints to STDOUT the IDs of the k documents in the collection 
with highest score, sorted by decreasing score

The program will be run from the root of the repository.

'''

import sys
from preprocessing import tokenize
from preprocessing import normalize
import collection_object
import math
import heapq

def compute_cosine_similarity(query_vector, doc_vector, normalization):
    """Compute the cosine similarity between two vectors."""
    dot_product = sum(query_vector.get(key, 0) * doc_vector.get(key, 0) for key in set(query_vector.keys()).union(doc_vector.keys()))

    if normalization == "c":
        # Normalize
        query_norm = math.sqrt(sum(value * value for value in query_vector.values()))
        doc_norm = math.sqrt(sum(value * value for value in doc_vector.values()))
        if query_norm * doc_norm == 0:  # Prevent division by zero
            return 0
        return dot_product / (query_norm * doc_norm)
    else:
        # Don't normalize
        return dot_product

def build_query_vector(keyword_query, preprocessing_method):
    '''
    Takes a query, tokenizes and normalizes it, builds a query vector
    using the 'nnn' weighting scheme.
    '''

    terms = normalize(tokenize(keyword_query), preprocessing_method)
    query_vector = {}
    for term in terms:
        if term in index:
            df = 1
            tf = terms.count(term)
            query_vector[term] = tf * df
        else:
            raise ValueError("'{}' is not a term in the vocabulary".format(term))

    return query_vector


def tokenize_and_answer(keyword_query, tf_scheme, df_scheme, normalization, k, preprocessing_method):
    '''
    Takes a query, tokenizes and normalizes it, builds a query vector, 
    and scores the documents using the dot product algorithm discussed in class,
    returns the k highest ranked documents in order.
    '''
    assert type(keyword_query) == str

    query_vector = build_query_vector(keyword_query, preprocessing_method)
    min_heap = []           # Uses the heapq library
    document_vectors = {}   # document_vectors[docID][term][tf-idf]
    answer = None # TODO: use the right data structure

    for term in query_vector.keys():
        if term in index:
            # Calculate df according to scheme
            if df_scheme == "t":
                # Use idf
                doc_count = index["_M_"]
                doc_frequency = index[term][0]
                if doc_frequency == 0 or doc_count == 0:
                    df = 0
                else:
                    df = math.log10((doc_count) / (doc_frequency))
            else:
                # Use regular df
                df = 1

            # Grab all postings for the current term
            for term_frequency, doc_id in index[term][1]:
                # Calculate tf according to scheme
                if tf_scheme == "l":
                    tf = math.log10(term_frequency) + 1
                else:
                    tf = term_frequency
                    
                tf_idf = tf * df

                # Build document vectors to calculate cosine similarities with
                if doc_id not in document_vectors:
                    document_vectors[doc_id] = {}           # Initialize docID if it doesn't exist
                document_vectors[doc_id][term] = tf_idf
    
    # Compute cosine similarity for each document
    for doc_id, doc_vector in document_vectors.items():
        cosine_sim = compute_cosine_similarity(query_vector, doc_vector, normalization)
        if len(min_heap) <= k:
            heapq.heappush(min_heap, (cosine_sim, doc_id))
        else:
            heapq.heappushpop(min_heap, (cosine_sim, doc_id))
    
    top_k = heapq.nlargest(k, min_heap)
    answer = [(doc_id, score) for score, doc_id in top_k]

    return answer


index = {}

if __name__ == "__main__":
    '''
    "main()" function goes here
    '''

    # Read and validate input arguments
    collection = collection_object.Collection()
    args = collection.parse_query_inputs()

    # Get the query, preprocessing method, and weighting scheme
    max_answers = args.k
    query = args.query
    preprocessing_method = args.tokenization

    tf_scheme = args.weighting_scheme[0]
    df_scheme = args.weighting_scheme[1]
    normalization = args.weighting_scheme[2]
    
    # Get the collection to query on
    collection_name = args.collection
    if preprocessing_method == 'lemmatization':
        file_type = 'corpus_lemmas'
    else:
        file_type = 'corpus_stems'
    output_path = collection.get_output_path(collection_name, file_type, throw_file_exists_error=False)
    
    index = collection.read_data(output_path)

    # Get answers to query
    answers = tokenize_and_answer(query, df_scheme, tf_scheme, normalization, max_answers, preprocessing_method)

    # Print results
    for docID, score in answers:
        print("{d}:{s:.3f}".format(d = docID, s=score), end="\t")
    
    exit(0)