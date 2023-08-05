# CompAnno: Human-friendly comparison tools for annotated sequences.

CompAnno is a user-friendly library for comparing features across:
  - genomes
  - sets of genomes
  - regions or subsets within the same genome


# Installation
### Bioconda
```
conda install -c induja companno
```

### Quickstart
CompAnno uses AnnotationTable objects to load and store the contents of gff files (An annotation format provided by NCBI, and also output by prokka). Annotations can be loaded from a file as follows:
```python
from companno import AnnotationTable, compare_counts, compare_cogs
k12 = AnnotationTable('k12.gff')
O157H7 = AnnotationTable('O157H7.gff')
HS = AnnotationTable('HS.gff')
```

##### Compare 2 genomes:

`compare_counts` will count the total number of annotations for each value of the given field in each `AnnotationTable`, and also calculate the difference between the table with the highest count and that with the lowest.

Ex. when given strand, `compare_counts` will count how many values are on the positive strand, and how many are on the negative strand.

```python
compare_counts({'k12': k12, 'O157H7': O157H7}, 'strand')
```

Output:

|      | k12  | O157H7 | difference |
| ---- | ---- | ------ | ---------- |
| +    | 2207 | 2719   | 512        |
| -    | 2291 | 2727   | 436        |

##### Compare COGS for 2 genomes:

`compare_cogs` will run compare counts for the field `cogs`, and then annotate the output with the cog names and cog categories.

```python
compare_cogs({'k12':k12, 'O157H7':O157H7})
```

Output:

|         | k12  | O157H7 | difference | category | name                                         |
| ------- | ---- | ------ | ---------- | -------- | -------------------------------------------- |
| COG2963 | 0    | 19     | 19         | X        | Transposase and inactivated derivatives      |
| COG2310 | 0    | 10     | 10         | T        | Stress response protein SCP2                 |
| COG3637 | 1    | 11     | 10         | M        | Opacity protein and related surface antigens |
| ...     | ...  | ...    | ...        | ...      | ...                                          |

##### Compare across many genomes:

```python
compare_cogs({'k12':k12, 'O157H7':O157H7, 'HS': HS})
```

Output:

|         | k12  | O157H7 | HS   | difference | category | name                                         |
| ------- | ---- | ------ | ---- | ---------- | -------- | -------------------------------------------- |
| COG2963 | 0    | 19     | 0    | 19         | X        | Transposase and inactivated derivatives      |
| COG2310 | 0    | 10     | 0    | 10         | T        | Stress response protein SCP2                 |
| COG3637 | 1    | 11     | 2    | 10         | M        | Opacity protein and related surface antigens |
| ...     | ...  | ...    | ...  | ...        | ...      | ...                                          |

##### Compare acrros genome sets:

```python
k12_and_HS = AnnotationTable().append(k12).append(HS)
compare_cogs({'k12_and_HS': k12_and_HS, 'O157H7':O157H7})
```

##### Custom comparisons:

Comparison are not limited to whole genomes. Comparison functions work equally well
across genome subsets:

```python
k12_positive_strand = k12.get("strand", "+")
k12_negative_strand = k12.get("strand", "-")
compare_cogs({"+ strand" : k12_positive_strand, "- strand": k12_negative_strand})
```

Can use lambda functions in python to get very specific subets of an Annotation Table:

```python
k12_20000_to_130000 = k12.get('start', lambda start: start > 20000) \
						.get('end', lambda end: end < 130000)
O157H7_20000_to_130000 = O157H7.get('start', lambda start: start > 20000) \
								.get('end', lambda end: end < 130000)
# return how many annotations are on each strand, for each subset
compare_counts({"k12_region" : k12_20000_to_130000, "O157H7_region": O157H7_20000_to_130000}, 'strand')
```

### Under the Hood

CompAnno provides easy-to-learn wrappers around pandas, a popular C-optimized python
libray for data processing.

Designed for interoperability, CompAnno AnnotationTable
objects can be easily imported to and exported from pandas DataFrames.

##### AnnotationTable to DataFrame:

```python
k12.as_df() # Returns pandas dataframe
```

##### DataFrame to AnnotationTable:

```python

import pandas as pd

df = pd.read_csv('frick.csv') # where frick.csv contains annotation information using
								# gff headers (start, stop, strand, etc.)
frick = pd.DataFrame(df) ## frik is an Annotation Table
```
