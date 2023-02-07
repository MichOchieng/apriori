import re
from collections import Counter
from itertools   import combinations
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
        self.apriori(self.TABLE,1)
        # print(list(combinations(self.TABLE,2)))
        # print(self.combine(self.TABLE,1))
        

    def initTable(self):
        counts = Counter()
        for key in self.DATASET:
            counts = counts + Counter(self.DATASET[key])
        self.TABLE = dict(counts)
        print('Initial table: ',self.TABLE)

    def addSupports(self,table) -> dict:
        for dbKey in self.DATASET:
            for key in table:
                if set(key).issubset(self.DATASET[dbKey]):
                    table[key]+=1
        return table
        

    def createSets(self,table,k) -> list:
        # Create a set of all unique table values
        setItems = set(value for key in table for value in key)
        # Return a list of combinations of size k given the above set items
        return list(combinations(setItems,k))

    def prune(self,table) -> dict:
        iterTable = table.copy()
        for key in iterTable:
            if iterTable[key] < self.SUPPORT:
                del table[key]
        return table

    def apriori(self,table,k):
        # Create next table
        #   Get combinations for next table
        #   Create new Dictionary for combinations
        #   Add supports to dictionary        
        sets = self.createSets(table,k)
        print('Sets: ',sets)
        nextTable = dict.fromkeys(sets,0)
        nextTable = self.addSupports(nextTable)
        print("New Table: ",nextTable)
        # Prune table
        nextTable = self.prune(nextTable)
        print("Pruned next Table: ",nextTable,'\n')
        if len(nextTable) > 0 and k < len(self.TABLE) + 1:
            k+=1
            self.apriori(nextTable,k)
        else:
            print('Final table: ',table)
            return table

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

test = Apriori('./Datasets/data.txt',2)