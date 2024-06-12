'''

Picks and runs "n" random queries from the collection using "query.py".
Collects the results and evaluates performance using the chosen metric

Input (in order):
    collection name, 
    weighting scheme for documents (see collection_object.py for details), 
    the text normalization (l or s), 
    the number of results to be returned for each query (k), 
    a number of queries to be tested (n), 
    and an evaluation metric (mrr or map)

Output:
    The value of mrr or map@k that it calculated

'''

import argparse
import subprocess
import os
import random
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Evaluate retrieval performance using MRR or MAP.')
    parser.add_argument('collection', type=str, help='Name of the collection')
    parser.add_argument('weighting_scheme', type=str, help='Weighting scheme for documents')
    parser.add_argument('text_normalization', choices=['l', 's'], help='Text normalization method: l for lemmatization, s for stemming')
    parser.add_argument('k', type=int, help='Number of results to return for each query')
    parser.add_argument('n', type=int, help='Number of queries to test')
    parser.add_argument('evaluation_metric', choices=['mrr', 'map'], help='Evaluation metric: MRR or MAP')
    return parser.parse_args()

def calculate_mrr(queries, all_answers):
    reciprocal_ranks = []
    for query_id, found_answers in queries:
        rank = None
        for i, doc_id in enumerate(found_answers, start=1):
            if doc_id in all_answers[query_id]:
                rank = i
                break
        if rank is not None:
            reciprocal_ranks.append(1 / rank)
        else:
            reciprocal_ranks.append(0)
    return sum(reciprocal_ranks) / len(reciprocal_ranks)

def calculate_map(queries, all_answers):
    avg_precisions = []
    for query_id, found_answers in queries:
        relevant_docs = all_answers[query_id]
        precisions = []
        hit_count = 0
        for i, doc_id in enumerate(found_answers, start=1):
            if doc_id in relevant_docs:
                hit_count += 1
                precisions.append(hit_count / i)
        if precisions:
            avg_precisions.append(sum(precisions) / len(relevant_docs))
        else:
            avg_precisions.append(0)
    return sum(avg_precisions) / len(avg_precisions) if avg_precisions else 0

def main():
    args = parse_arguments()

    from utils import read_queries, read_answers

    query_filepath = f"./collections/{args.collection}.QRY"
    answer_filepath = f"./collections/{args.collection}.REL"

    if not os.path.exists(query_filepath) or not os.path.exists(answer_filepath):
        exit(1)

    all_queries = read_queries(query_filepath)
    all_answers = read_answers(answer_filepath)

    selected_queries = random.sample(list(all_queries.items()), args.n)

    query_results = []

    for query_id, query_text in selected_queries:
        command = [
            sys.executable, "./code/query.py", args.collection, args.weighting_scheme, args.text_normalization, str(args.k), query_text
        ]
        process = subprocess.run(command, capture_output=True, text=True)
        output = process.stdout.strip().split('\t')
        found_answers = [int(pair.split(':')[0]) for pair in output if pair]
        query_results.append((query_id, found_answers))  # Note: Keep query_id as int for consistency

    formatted_query_results = [(int(query_id), found_answers) for query_id, found_answers in query_results]

    if args.evaluation_metric == 'mrr':
        metric_value = calculate_mrr(formatted_query_results, all_answers)
    else:  # 'map'
        metric_value = calculate_map(formatted_query_results, all_answers)

    print(f"{metric_value:.3f}")

if __name__ == "__main__":
    main()

