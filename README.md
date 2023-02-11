# Apriori algorithm

## Execution

To execute run:

```bash
python apriori.py <filepath> <support level> <confidence level>
```

### Example

```bash
python apriori.py ./Datasets/data.txt 2 60
```

Will run the Apriori algorithm on the database file found at ./Datasets/data.txt, with a minimum support level of 2 and confidence of 60%. An ouput file (MiningResult.txt) will be created in the root directory of apriori.py containing association rules for the frequent itemsets.
