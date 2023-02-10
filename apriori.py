import re
import sys
from math import floor
from collections import Counter
from itertools   import combinations
from timeit import default_timer as timer

class Apriori:
    NUM_TRANSACTIONS = int
    SUPPORT_LEVEL = int
    SUPPORT = int
    ITEMSET = set()
    DATASET = {}
    TABLE   = {}
    FINAL_TABLE = {}

    def __init__(self) -> None:
        try:
            self.SUPPORT_LEVEL = int(sys.argv[2])
        except ValueError:
            print(sys.argv[2], 'is not a number!')
            exit()
        except IndexError:
            print('Make sure you enter the filepath and support level!')
            exit()
        self.readFile(sys.argv[1])
        self.initTable()
        t0 = timer()
        self.FINAL_TABLE = self.apriori(self.TABLE,1)
        t1 = timer()
        self.getRunTime(t0,t1)
        

    def initTable(self):
        counts = Counter()
        for key in self.DATASET:
            counts = counts + Counter(self.DATASET[key])
        self.TABLE = dict(counts)

    def addSupports(self,table) -> dict:
        for dbKey in self.DATASET:
            for key in table:
                if set(key).issubset(self.DATASET[dbKey]):
                    table[key]+=1
        return table
        

    def createSets(self,table,k) -> list:
        # Create a set of all unique table values
        if k == 1:
            setItems = set(key for key in table)
        else:
            setItems = set(value for key in table for value in key)
        # Return a list of combinations of size k given the above set items
        return list(combinations(setItems,k))

    def prune(self,table) -> dict:
        iterTable = table.copy()
        for key in iterTable:
            if iterTable[key] < self.SUPPORT:
                del table[key]
        return table

    def apriori(self,table,k) -> dict:
        # Create next table
        #   Get combinations for next table
        #   Create new Dictionary for combinations
        #   Add supports to dictionary        
        sets = self.createSets(table,k)
        nextTable = dict.fromkeys(sets,0)
        nextTable = self.addSupports(nextTable)
        # Prune table
        nextTable = self.prune(nextTable)
        # Check for final table
        if len(nextTable) > 0 and k < len(self.TABLE) + 1:
            k+=1
            self.apriori(nextTable,k)
        else:
            print('Final table: ',table)
            return table

    def getRunTime(self,t0,t1):
        totalRunTime = t1-t0
        if totalRunTime < 1000:
            print('Total runtime: ',round(totalRunTime*1000,3),'ms')
        else:
            print('Total runtime: ',round(totalRunTime,3),'sec')

    def readFile(self,file:str): 
        try:
            with open(file, 'r', encoding='utf-8') as f:
                # Pull lines from file
                lines = f.readlines()
                # Parse Transactions after first line in file
                    # Strip newline from end of string
                    # Split string into list of ints 
                # Init num transactions
                self.NUM_TRANSACTIONS = int(lines[0])
                # Init support
                self.SUPPORT = floor(self.NUM_TRANSACTIONS * (self.SUPPORT_LEVEL / 100))
                print("Support level: ",self.SUPPORT)
                for line in lines[1:]:
                    row = re.split(r'\t+',line)
                    items = row[-1].rstrip('\r\n')
                    itemList = items.split()
                    self.DATASET[row[0]] = itemList
            print('Initial dataset: ',self.DATASET)
        except FileNotFoundError:
            print("Couldn't find file:",file,':(')
            exit()

Apriori()