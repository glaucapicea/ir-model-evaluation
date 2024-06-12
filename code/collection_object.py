'''

An object used to represent the different files of a collection
handles argument parsing, validation of inputs, constructing filepaths, and reading/writing data to files

'''

import sys
import os
import argparse
import json

class Collection:
    def __init__(self):
        self.input_extensions = {
            "answers": ".REL",
            "corpus": ".ALL",
            "queries": ".QRY"
        }
        self.output_extensions = {
            "answers": ".REL",
            "corpus_lemmas": "corpus_lemmas",
            "corpus_stems": "corpus_stems",
            "queries": ".QRY"
        }

    # ----------------------------------------------------------------------------------------------------
    # Data types used to validate inputs
    # ----------------------------------------------------------------------------------------------------
    
    @staticmethod
    def weighting_scheme(string):
        '''Custom type which to validate if an input contains a weighting scheme of nnn format'''
        valid_types = {
            "tf": ["n", "l"],
            "df": ["n", "t"],
            "norm": ["n", "c"]
        }

        # Validate length and weighting types of scheme input
        if len(string) != 3 or any(char not in 'nltc' for char in string):
            raise argparse.ArgumentTypeError("Scheme must be three characters long")
        tf = string[0]
        df = string[1]
        norm = string[2]
        if tf not in valid_types["tf"] or df not in valid_types["df"] or norm not in valid_types["norm"]:
            raise argparse.ArgumentTypeError("Weighting scheme types invalid. tf = [n, l], df = [n, t], norm = [n, c]")
        
        return string
    
    @staticmethod
    def tokenization(string):
        '''Custom type which is used to validate if an input contains a valid tokenization scheme'''
        valid_types = {
            "l": "lemmatization",
            "s": "stemming"
        }

        # Validate length and type of normalization input
        if len(string) != 1 or string not in valid_types:
            raise argparse.ArgumentTypeError("Normalization scheme invalid, must be either 'l' (lemmatization) or 's' (stemming)")
        
        return valid_types[string]
    
    @staticmethod
    def positive_int(value):
        '''Custom type used to validate if an input is a positive integer'''
        try:
            value = int(value)
            if value <= 0:
                raise argparse.ArgumentTypeError("{} is not a positive integer".format(value))
        except ValueError:
            raise Exception("{} is not an integer".format(value))
        return value
    
    @staticmethod
    def evaluation(string):
        '''Custom type which is used to validate if an input contains a valid tokenization scheme'''
        valid_types = ["mmr", "map"]

        # Validate length and type of normalization input
        if len(string) != 3 or string not in valid_types:
            raise argparse.ArgumentError("Evaluation metric invalid, must be either 'map' or 'mmr'")
        
        return string
    
    # ----------------------------------------------------------------------------------------------------
    # Input reading commands
    # ----------------------------------------------------------------------------------------------------

    def parse_read_inputs(self):
        ''' Grab input terminal parameter, used for build_index.py '''
        parser = argparse.ArgumentParser()
        parser.add_argument("collection",
                                type=str,
                                help="Name of the collection to process")
        args = parser.parse_args()
        return args
    
    def parse_query_inputs(self):
        ''' Grab input terminal parameters, used for query.py '''
        parser = argparse.ArgumentParser()
        parser.add_argument("collection",
                            type=str,
                            help="Name of the collection to process")
        parser.add_argument("weighting_scheme",
                            type=Collection.weighting_scheme,
                            help="The scoring scheme to use on the query")
        parser.add_argument("tokenization",
                            type=Collection.tokenization)
        parser.add_argument("k",
                            type=Collection.positive_int,
                            help="The maximum number of answers to retrieve")
        parser.add_argument("query",
                            type=str,
                            help="The query to run")
        args = parser.parse_args()
        return args
    
    def parse_evaluation_inputs(self):
        ''' Grab input terminal parameters, used for evaluation.py '''
        parser = argparse.ArgumentParser()
        parser.add_argument("collection",
                            type=str,
                            help="Name of the collection to process")
        parser.add_argument("weighting_scheme",
                            type=Collection.weighting_scheme,
                            help="The scoring scheme to use on the query")
        parser.add_argument("tokenization",
                            type=Collection.tokenization)
        parser.add_argument("k",
                            type=Collection.positive_int,
                            help="The maximum number of answers to retrieve")
        parser.add_argument("n",
                            type=Collection.positive_int,
                            help="The number of queries to test")
        parser.add_argument("evaluation_metric",
                            type=Collection.evaluation,
                            help="Evaluation metric to use on query results")
        args = parser.parse_args()
        return args

    # ----------------------------------------------------------------------------------------------------
    # Collection file related commands
    # ----------------------------------------------------------------------------------------------------

    def get_input_path(self, name, file_type):
        '''
        Return collection path if it exists.
        '''
        # Validate input file type
        if not file_type in self.input_extensions.keys():
            raise ValueError(f'Valid file types are: ["answers", "corpus", "queries"]')
        extension = self.input_extensions[file_type]

        # Construct and validate path
        collection_path = f'./collections/{name}{extension}'
        if not os.path.exists(collection_path):
            raise FileNotFoundError(f'There is no valid collection "{name}" at {collection_path}')
        return collection_path

    def get_output_path(self, name, file_type, throw_file_exists_error=True):
        '''
        Return output path if it exists.
        '''
        # Validate input file type
        if not file_type in self.output_extensions.keys():
            raise ValueError(f'Valid file types are: ["answers", "corpus", "queries"]')
        extension = self.output_extensions[file_type]

        # Construct and validate path
        output_path = f'./processed/{name}_{extension}.json'
        if (throw_file_exists_error == True):
            if os.path.exists(output_path):
                raise FileExistsError(f'The output collection at {output_path} already exists')
        return output_path
    
    def write_data(self, data, output_path):
        '''Writes the input dictionary to the specified JSON file location'''
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    def read_data(self, output_path):
        with open(output_path, 'r') as file:
            content = json.load(file)
        return content
