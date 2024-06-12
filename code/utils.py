'''

Used by the tests to read .QRY and .REL files

'''

def read_answers(collection_path):
    '''
    Reads the answers from .REL files
    '''
    answers = {}

    with open(collection_path, 'r') as file:
        for line in file:
            # Split the current line's data into an array and assign IDs accordingly
            line_parts = line.strip().split()
            query_id = int(line_parts[0])
            document_id = int(line_parts[1])

            # Create a dictionary key for newly encountered queries
            if query_id not in answers:
                answers[query_id] = []

            # Assign the document ID to it's corresponding query
            answers[query_id].append(document_id)

    return answers

def read_queries(collection_path):
    '''
    Reads the queries from .QRY files
    '''

    with open(collection_path, 'r') as file:
        queries = {}
        current_id = None
        text_buffer = ""

        for line in file:
            if line.startswith('.I'):
                # Submit the text for the previous document (if not reading the first document)
                if current_id:
                    queries[current_id] = text_buffer.strip()
                # Prepare to encounter the text for the new document
                current_id = line.split()[1]
                capture_text = False
                text_buffer = ""
            elif line.startswith('.W'):
                # New document's text has been encountered, set variable accordingly
                capture_text = True
                continue
            elif capture_text:
                # Append the new text line
                text_buffer += line

        # Submit the last document
        if current_id:
            queries[current_id] = text_buffer.strip()

        return queries
    
class Query:
    def __init__(self, collection, scheme, n, query):
        self.collection = collection
        self.scheme = scheme
        self.n = n
        self.query = query