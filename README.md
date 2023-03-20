# Apriori algorithm

## Execution

To execute run:

```bash
python apriori.py <filepath> <support level %>
```

## Example

```bash
python apriori.py ./Datasets/data.txt 
```

Will run the Apriori algorithm on the database file found at ./Datasets/data.txt, with a minimum support level of 50%. An ouput file (MiningResult.txt) will be created in the root directory of apriori.py containing the frequent patterns.

### Example console output

```bash
$ python apriori.py test2.txt 40
|FPs| = 7
Total runtime:  0.073 ms
```

### Example file output

```file
|FPs| = 7
['1', '3', '4'] : 2
['3', '4'] : 2
['1', '4'] : 2
['1'] : 3
['4'] : 2
['1', '3'] : 3
['3'] : 4
```