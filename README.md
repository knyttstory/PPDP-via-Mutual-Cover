# PPDP via Mutual Cover

Implementation of the mutual cover algorithm.

+ filter_data.csv is the sample data we used
+ data_preprocessing.py is the method to sample data
+ mutual_cover_diversity.py is the mutual cover algorithm
+ disclosure_mutual_diversity.py is the method to measure the identity disclosure and attribute disclosure
+ penalty_mutual_diversity.py is the method to evaluate the information loss
+ query_mutual.py is the query test method

## Requirements
 + numpy
 + pandas
 + scipy


## Usage

1. run mutual_cover_diversity.py to generate the anonymized version of filter_data.csv
2. run disclosure_mutual_diversity.py, penalty_mutual_diversity.py and query_mutual.py to generate the corresponding experimental results separately
