'''

Uses "test_scheme.py" to iterate over all possible scheme combinations and collect MMR and MAP scores.
Collects the outputs and uses that data to populate an excel sheet which it stores into a "results" folder as "evaluation_results.xlsx"

'''

import subprocess
import os
import pandas as pd
import sys

# Initialize and validate file paths
evaluation_program_path = "./code/test_scheme.py"
collection_name = "CISI_simplified"
weightings = ["nnn", "nnc", "ntn", "ntc", "lnn", "lnc", "ltn", "ltc"]
tokenizations = ["l", "s"]
k_results = "100"
n_queries = "10"
evaluations = ['map', 'mrr']  # Keep single quotes for subprocess

def test_all_methods():
    output = {eval_metric: {tokenization: {weighting: None for weighting in weightings} for tokenization in tokenizations} for eval_metric in evaluations}
    for eval_metric in evaluations:
        for tokenization in tokenizations:
            for weighting in weightings:
                print("Running:", "python3", evaluation_program_path, collection_name, weighting, tokenization, k_results, n_queries, eval_metric)
                process = subprocess.Popen(
                    [sys.executable, evaluation_program_path, collection_name, weighting, tokenization, k_results, n_queries, eval_metric],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)  # Merge stderr with stdout
                stdout, stderr = process.communicate()  # Wait for process to finish and get the output
                if stderr:
                    print("Error:", stderr.decode().strip())
                if stderr:
                    print("Error:", stderr)
                if process.returncode == 0:  # Check if subprocess succeeded
                    # Assuming the output is a float in string format, e.g., '0.123\n'
                    try:
                        metric_value = float(stdout.decode().strip())
                        output[eval_metric][tokenization][weighting] = metric_value
                        print("Results:", metric_value)
                    except ValueError:
                        # Handle the case where the output is not a float
                        print(f"Error parsing metric value from output: {stdout}")

    # Convert the structured data into pandas DataFrames and save to Excel
    results_folder = 'results'
    os.makedirs(results_folder, exist_ok=True)
    
    results_path = os.path.join(results_folder, 'evaluation_results.xlsx')
    with pd.ExcelWriter(results_path) as writer:
        for eval_metric in evaluations:
            data = []
            for tokenization in tokenizations:
                for weighting in weightings:
                    score = output[eval_metric][tokenization][weighting]
                    # Only include if there is a score (it's not None)
                    if score is not None:
                        data.append((tokenization, weighting, score))
            df = pd.DataFrame(data, columns=['Tokenization', 'Weighting', 'Score'])
            # Remove single quotes from the sheet name
            sheet_name = eval_metric.strip("'")
            df.to_excel(writer, sheet_name=sheet_name, index=False)

test_all_methods()
