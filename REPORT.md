# **Report Introduction:**
   This report aims to validate the effectiveness of a query processing system by comparing its results against a standard set of relevant documents for a subset of queries from the CISI_simplified dataset. It highlights the significance of various scoring parameters and configurations in determining query result relevance. Below is an elaboration on the different scoring parameters that can influence the outcomes of such a system, reflecting the critical aspects of information retrieval processes:

   - **Term Frequency (TF)**: Reflects how many times a term appears within a document. Higher TF values suggest that the term is more relevant to the document, influencing the document's ranking in query results.
   - **Document Frequency (DF)**: Indicates the number of documents that contain a term. Lower DF values signify that the term is rare, potentially making it more significant for distinguishing relevant documents.
   - **Inverse Document Frequency (IDF)**: A measure used to diminish the weight of terms that appear frequently across the document collection, thereby amplifying the importance of rarer terms in the ranking process.
   - **TF-IDF Score**: Combines TF and IDF to evaluate a term's relevance within a document relative to the entire collection. It helps to prioritize documents containing terms that are both commonly used within specific documents and rare across the entire document set.
   - **Cosine Similarity**: Measures the cosine of the angle between two vectors, in this case, the query vector and document vectors, in a multi-dimensional space. It's used to determine the similarity between the query and each document, with higher values indicating greater relevance.
   
# **Metrics:**
   We can evaluate the effectiveness of different scoring parameter configurations using the following metrics:
   - **Mean Reciprocal rank (MRR)**: MRR is an evaluation metric used to assess the effectiveness of a search algorithm by focusing on the rank of the first relevant result. It's especially useful when the primary concern is how high the first relevant document appears in the search results. MRR is calculated as the average of the reciprocal ranks of the first relevant document for a set of queries. This metric emphasizes the importance of the top result, underlining scenarios where users are likely to consider only the first few documents.
   - **Mean Average Precision (MAP)**: MAP evaluates the quality of search results across all ranks, making it a comprehensive metric for scenarios where the entire list of retrieved documents matters. It calculates the precision of search results at each rank where a relevant document is found, averages these values for each query, and then averages those averages across all queries. This metric accounts for both the precision and recall of the search results, providing a balanced view of overall performance.

   In summary, MRR provides insight into how effectively a search algorithm or system places the first relevant result, while MAP offers a nuanced view of how well the system performs across all its retrieved results, making both metrics invaluable for evaluating and refining search systems.
   
# **Methodology**
   - **Objective**: The aim is to identify the scoring parameter and preprocessing method combination that yields the highest agreement with a set of known relevant documents for a series of queries, as measured by the MRR (Mean Reciprocal Rank) and MAP (Mean Average Precision) evaluation metrics.
   - **Evaluation Script**: `test_all_schemes.py` will automate the process of running a series of experiments. It iterates through every combination of schemes (weighting scheme, preprocessing method, tokenization method) across different configurations using `test_scheme.py` which will output the evaluation metrics for each. 
   - **Metrics Calculation**: The `test_scheme.py` script will compute evaluation metrics for each configuration tested, allowing for direct comparison between them. The metrics of interest are precision, recall, F1 score, and MAP.
   - **Configuration Parameters**:
     1. **Preprocessing Methods**: Options for text normalization, i.e., stemming (s) or lemmatization (l).
     2. **Weighting Schemes**: Different schemes for calculating the tf-idf score
         - term frequency: [none (n), logarithmic (l)]
         - document frequency: [none (n), inverse document frequency (t)]
         - normalization: [none (n), cosine (c)]
   - **Experimentation Process**:
      1. `build_index.py` was ran on the `CISI_simplified` collection to create the indexes to query on
      2. `test_all_schemes.py` was ran and called to iterate over all possible scheme combinations and get MMR and MAP scores using `test_scheme.py`
      3. `test_scheme.py` reads in all queries from the CISI dataset.
      4. It then runs each query against the system using each combination of preprocessing method and weighting scheme.
      5. For each run, it compares the system's output with the known relevant documents and calculates the evaluation metrics.
      6. It logs the performance of each configuration in terms of the metrics calculated.
      7. `test_all_schemes.py` collects these logs and puts them into a dictionary to keep track of the schemes used
      8. `test_all_schemes.py` outputs this dictionary into an excel sheet and populates the appropriate fields with the data it collected
   - **Usage**:
   You'll need pandas and openpyxl to create and write to Excel files. import them and then run the evaluation program
   Example command for the test_all_schemes.py:
   ```
   python3 ./code/build_index.py CISI_simplified
   pip install pandas openpyxl
   python3 ./code/test_all_schemes.py
   ```
   This does use an external library as filling out an excel sheet manually would be very tedious, but you can run the original test_scheme.py as shown below (in this example, using weighting scheme=ltc, tokenization=l, k=100, n=10, scoring=mmr)
   ```
   python3 ./code/build_index.py CISI_simplified
   python3 ./code/test_scheme.py CISI_simplified ltc l 100 10 'mrr'
   ```

# **Results**
   - [evaluation_results.xlsx](https://github.com/CMPUT-361/cmput361-a4-w24-shubhkaran30546/files/14892538/evaluation_results.xlsx)
   - Note: There are 2 pages in this excel sheet: one corresponding to the MAP scores, and the other to the MRR scores. The scores are sorted in decreasing order of score.

# **Conclusion:**
   ## Weighting Scheme Performance
   - For MAP:
      - The ltc weighting scheme with lemmatization (l) has the highest MAP score of 0.043.   (Page 1 row 3)
      - The ntc weighting scheme with stemming (s) has the highest MAP score of 0.046.       (Page 1 row 2)
   - For MRR:
      - The ltc weighting scheme shows strong performance with both lemmatization and stemming, scoring 0.198 and 0.240 respectively. (Page 2 row 7 and 6 respectively)
      - The ntc weighting scheme with stemming outperforms all other combinations with an MRR score of 0.561. (Page 2 row 2)
   ## Tokenization Method Performance
   - Across the different weighting schemes, stemming (s) tends to result in higher MAP scores compared to lemmatization (l).
   - Stemming (s) also consistently shows higher MRR scores across most weighting schemes, with the ntc weighting scheme and stemming showing the highest MRR score.

   ## Conclusions
   - There does not seem to be a single weighting scheme that is always best regardless of the text normalization method. However, the ntc weighting scheme performs exceptionally well with stemming for the MRR metric, and ltc does well with lemmatization for MAP.
   - Stemming (s) appears to be a more effective normalization method than lemmatization (l) in this experiment, as it yields higher scores in both MAP and MRR for most weighting schemes.
   - The ntc weighting scheme (no term frequency, inverse document frequency, cosine normalization) with stemming (s) is particularly notable for achieving the highest MRR score of 0.561, suggesting that for the task of finding the most relevant documents, this combination is the most effective in this dataset.
   - Similarly, for MAP, the ntc weighting scheme with stemming (s) yields the highest score of 0.046, indicating that it is also effective in ensuring relevant documents are ranked higher overall.
