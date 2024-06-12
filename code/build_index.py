'''

Reads all documents in the collection file into memory and writes
an inverted index to the processed folder.

The program will be run from the root of the repository.

'''

import sys
from preprocessing import tokenize
from preprocessing import normalize
import collection_object


def read_documents(input_path):
    '''
    Reads the documents in the collection (inside the 'collections' folder).
    '''
    documents = {}

    with open(input_path, 'r') as file:
        documents = {}
        current_id = None
        capture_text = False
        text_buffer = ""

        for line in file:
            if line.startswith('.I'):
                # Submit the text for the previous document (if not reading the first document)
                if current_id:
                    documents[current_id] = text_buffer.strip()
                # Prepare to encounter the text for the new document
                current_id = line.split()[1]
                capture_text = False
                text_buffer = ""
            elif line.startswith('.W'):
                # New document's text has been encountered, begin capturing its contents
                capture_text = True
            elif line.startswith('.X'):
                 capture_text = False
            elif capture_text:
                # Append the new text line
                text_buffer += line
        
        # Submit the last document
        if current_id:
            documents[current_id] = text_buffer.strip()

        print(f'{len(documents)} documents read in total')
        return documents

def build_index(documents, normalization):
    '''
    Builds inverted index.
    '''

    assert type(documents) == dict

    index = {}
    normalized = {}
    
    # Tokenize and normalize all terms inside each document
    for docID in documents:
        original_text = documents[docID]
        normalized[docID] = normalize(tokenize(original_text), normalization)

    for docID in normalized:
        document_tokens = normalized[docID]
        tfs = {}                        # tf: [term, tf] (for a given docID)

        # Calculate term frequencies for the document and initialize index
        for term in document_tokens:
            # Initialize the term in the inverted index if it hasn't been encountered yet
            if term not in index:       
                index[term] = [0, []]   # Term: [DF=0, [postings list]]
            # Calculate term frequencies for all terms in document
            
            if term in tfs:
                # If term is a duplicate, increment its tf for this document
                term_frequency = tfs[term]
                tfs[term] = term_frequency + 1
            else:
                # If term is new for this document, initialize the tf
                tfs[term] = 1
    
        # Sort postings by term frequency and insert into index
        sorted_postings = sorted(tfs.items(), key=lambda x:x[1], reverse=True)
        
        for posting in sorted_postings:
            term = posting[0]
            term_frequency = tfs[term]
            index[term][1].append([term_frequency, docID])   # index[term][DF/postings][tf/docID]

    # Calculate document frequency and tf for each term
    for term in index:
        document_frequency = len(index[term][1])
        index[term][0] = document_frequency

    index['_M_'] = len(documents)
    
    return index

if __name__ == "__main__":
    '''
    main() function
    '''
    # Validate inputs and initialize paths
    collection = collection_object.Collection()
    collection_name = collection.parse_read_inputs().collection
    input_path = collection.get_input_path(collection_name,
                                            file_type='corpus')
    output_path_lemmas = collection.get_output_path(collection_name,
                                            file_type='corpus_lemmas',
                                            # Set this to True if you want to throw an error when the output proccessed index file already exists
                                            throw_file_exists_error=False)
    output_path_stems = collection.get_output_path(collection_name,
                                            file_type='corpus_stems',
                                            # Set this to True if you want to throw an error when the output proccessed index file already exists
                                            throw_file_exists_error=False)
    
    # Read the corpus data into a dictionary
    data = read_documents(input_path)

    # Create index output files
    lemmatized_index = build_index(data, 'lemmatization')
    stemmed_index = build_index(data, 'stemming')

    # Write data to output file
    collection.write_data(lemmatized_index, output_path_lemmas)
    collection.write_data(stemmed_index, output_path_stems)

    print("SUCCESS")

    exit(0)