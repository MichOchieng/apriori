import re
import sys
from math import floor
from collections import Counter
from itertools   import combinations
from timeit import default_timer as timer

class Table:
    TABLE         = {}
    SUPPORT_LEVEL = int
    DATABASE      = list

    def __init__(self,db,minSup) -> None:
        self.DATABASE = db
        self.SUPPORT_LEVEL = minSup

    # Creates the first table C1
    def initTable(self):
        for item in self.DATABASE:
            for i in range(len(item)):
                tempSet = frozenset([item[i]]) 
                # Checks to see if itemset is in the table
                if tempSet not in self.TABLE: # Add to table
                    self.TABLE[tempSet] = 1 
                else: # Increase count/support level
                    self.TABLE[tempSet] += 1            

    # Joins itemssets
    def createNextTable(self):
        nextTable = {}
        # Get list of itemsets
        keys = list(self.TABLE.keys())
        # Join itemsets
        for i in range(len(keys)):
            for j in range(i+1,len(keys)):
                newKey = set()
                set0 = keys[i]
                set1 = keys[j]

                # Pruning
                if self.TABLE[set0] >= self.SUPPORT_LEVEL and self.TABLE[set1] >= self.SUPPORT_LEVEL:
                    newKey = set0.union(set1)
                # Check for infrequent subset
                # Only add newKey if not an infrequent subset
                for item in newKey:
                    subset = newKey - {item}
                    if subset not in keys or self.TABLE[subset] < self.SUPPORT_LEVEL:
                        break
                nextTable[frozenset(newKey)] = 0
        self.TABLE = nextTable

    # Adds supports
    def fillTable(self):
        for item in self.DATABASE:
            for key in self.TABLE.keys():
                if key.issubset(item):
                    self.TABLE[key] += 1

    def getTable(self) -> dict:
        return self.TABLE
    
class Apriori:
    SUPPORT      = int
    TRANSACTIONS = []
    FINAL_TABLE  = Table

    def __init__(self) -> None:
        try:
            self.SUPPORT_LEVEL = int(sys.argv[2])
        except ValueError:
            print(sys.argv[2], 'is not a number!')
            exit()
        except IndexError:
            print('Make sure you enter the filepath and support level!')
            exit()
        # Read in transactions from file
        self.readFile(sys.argv[1])
        # Create first table from transactions
        table = Table(self.TRANSACTIONS,self.SUPPORT)
        table.initTable()
        print(table.getTable())
        # Begin loop
        table.createNextTable()
        table.fillTable()
        print(table.getTable())
        # done = False
        # while not done:
        #     pass
        # t0 = timer()
        # self.FINAL_TABLE = self.apriori(self.TABLE,1)
        # t1 = timer()
        # self.getRunTime(t0,t1)
        

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
                    row = re.split(r'\t+',line)[-1].rstrip('\r\n').split()
                    self.TRANSACTIONS.append(row)
            print('Transactions: ',self.TRANSACTIONS)
        except FileNotFoundError:
            print("Couldn't find file:",file,':(')
            exit()
Apriori()