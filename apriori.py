import re
import sys
from timeit import default_timer as timer
from itertools import chain, combinations

class Table:
    TABLE         = {}
    SUPPORT_LEVEL = int
    DATABASE      = list
    SUPPORT_TABLE = {}

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
        self.prune()    
        self.SUPPORT_TABLE.update(self.TABLE)     

    # Joins itemssets 
    def createNextTable(self,k):
        nextTable = {}
        # Get list of itemsets
        keys = list(self.TABLE.keys())
        # Join itemsets
        for i in range(len(keys)):
            for j in range(i+1,len(keys)):
                flag = False
                newKey = set()
                set0 = keys[i]
                set1 = keys[j]

                newKey = set0.union(set1)
                if len(newKey) == k:
                    # Check for infrequent subset
                    # Only add newKey if not an infrequent subset
                    for item in newKey:
                        subset = newKey - {item}
                        if subset not in self.TABLE or self.TABLE[subset] < self.SUPPORT_LEVEL:
                            flag = True
                            break
                    # Stops empty keys or keys of varying size from being added to tables
                    if not flag:
                        nextTable[frozenset(newKey)] = 0
        return nextTable

    # Adds supports
    def fillTable(self):
        for item in self.DATABASE:
            for key in self.TABLE.keys():
                if key.issubset(item):
                    self.TABLE[key] += 1
        self.prune() 
        self.SUPPORT_TABLE.update(self.TABLE)  
    
    def prune(self):
        temp = self.TABLE.copy()
        for key in temp.keys():
            if self.TABLE[key] < self.SUPPORT_LEVEL:
                del self.TABLE[key]

    def getTable(self) -> dict:
        return self.TABLE

    def getSupports(self) -> dict:
        return self.SUPPORT_TABLE

    def setTable(self,table):
        self.TABLE = table
    
class Apriori:
    SUPPORT      = int
    TRANSACTIONS = []
    FINAL_TABLE  = Table
    CONFIDENCE   = int
    SUBSETS      = list
    RULES        = list


    def __init__(self) -> None:
        # Init Confidence and Support level
        try:
            self.CONFIDENCE = int(sys.argv[3])
            self.SUPPORT    = int(sys.argv[2])
        except ValueError:
            print('Confidence and support levels must be entered as numbers.')
            exit()
        except IndexError:
            print('Make sure you enter the filepath, support and confidence level level!')
            exit()
        # Read in transactions from file
        self.readFile(sys.argv[1])
        t0 = timer()
        # Begin loop
        done = False
        k = 1
        table = Table(self.TRANSACTIONS,self.SUPPORT)
        while not done:
            if k == 1: # Create first table from transactions
                table.initTable()
                table.setTable(table.getTable())
                k+=1
                continue
            temp = table.createNextTable(k)
            if len(temp) > 0:
                table.setTable(temp)
                table.fillTable()
                k+=1
            else:
                self.FINAL_TABLE = table
                done = True
        print('Final table',self.FINAL_TABLE.getTable())
        print('Sup table',self.FINAL_TABLE.getSupports())
        self.SUBSETS = self.powerset(self.FINAL_TABLE.getTable().keys())
        print(self.getRules())
        t1 = timer()
        self.getRunTime(t0,t1)

    def powerset(self,itemSets):
        powerset = []
        for item in itemSets:
            for subset in chain.from_iterable(combinations(item,i) for i in range(len(item) + 1)):
                powerset.append(frozenset(subset))
        return powerset[1:-1]
            
    def getRules(self):
        supportTable = self.FINAL_TABLE.getSupports()
        rules = []
        for key in self.FINAL_TABLE.getTable().keys():
            for subset in self.SUBSETS:
                if (supportTable[key] / supportTable[subset]) * 100 > self.CONFIDENCE:
                    rules.append(subset)
        return rules

    def getRunTime(self,t0,t1):
        totalRunTime = t1-t0
        if totalRunTime < 1:
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
                for line in lines[1:]:
                    row = re.split(r'\t+',line)[-1].rstrip('\r\n').split()
                    self.TRANSACTIONS.append(row)
        except FileNotFoundError:
            print("Couldn't find file:",file,':(')
            exit()
    
    def writeFile(self):
        with open('output.txt','w') as f:
            f.write('|FPS| = ',len(self.RULES))
            for rule in self.RULES:
                pass
Apriori()