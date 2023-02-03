import re
from collections import Counter
from itertools   import combinations, product

class Results:
    def __init__(self) -> None:
        pass

class Apriori:
    NUM_TRANSACTIONS = int
    SUPPORT = int
    ITEMSET = set()
    DATASET = {}
    TABLE   = {}
    FINAL_TABLE = {}

    def __init__(self,filename,support) -> None:
        self.SUPPORT = support
        self.readFile(filename)
        self.initTable()
        self.run(self.TABLE,1)
        # print(list(combinations(self.TABLE,2)))
        # print(self.combine(self.TABLE,1))

    def initTable(self):
        counts = Counter()
        for key in self.DATASET:
            counts = counts + Counter(self.DATASET[key])
        self.TABLE = dict(counts)
        print('Initial table: ',self.TABLE)

    def run(self,table,k):
        if len(table) > 1 and k < len(self.TABLE) + 1:
            # Create next table
            #   Get combinations for next table
            #   Create new Dictionary for combinations
            #   Add supports to dictionary
            setItems = set([val for key in table for val in key])
            sets = list(combinations(setItems,k))
            print("Sets: ",sets)
            newDict = dict.fromkeys(sets,0)

            for dbKey in self.DATASET:
                for key in newDict:
                    if set(key).issubset(self.DATASET[dbKey]):
                        newDict[key]+=1
            print("New Table: ",newDict)
            tempTable = newDict.copy()
            # Prune table
            for key in tempTable:
                if tempTable[key] < self.SUPPORT:
                    del newDict[key]
            print("Pruned Table: ",newDict,'\n')
            k+=1
            self.run(newDict,k)



    def readFile(self,file:str): 
        try:
            with open(file, 'r', encoding='utf-8') as f:
                # Pull lines from file
                lines = f.readlines()
                # Parse Transactions after first line in file
                    # Strip newline from end of string
                    # Split string into list of ints 
                for line in lines[1:]: # Skip the first line, num transactions not important
                    row = re.split(r'\t+',line)
                    items = row[-1].rstrip('\r\n')
                    itemList = items.split()
                    self.DATASET[row[0]] = itemList
            print('Initial dataset: ',self.DATASET)
        except FileNotFoundError:
            print("Couldn't find",file)

test = Apriori('test.txt',2)