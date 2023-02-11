import re
import sys
from timeit import default_timer as timer
from itertools import chain, combinations

class Table:
    TABLE         = {} # Main table that will end up containing frequent itemsets
    SUPPORT_LEVEL = int
    DATABASE      = list
    SUPPORT_TABLE = {} # Table used to determine association rules

    def __init__(self,db,minSup) -> None:
        self.DATABASE = db
        self.SUPPORT_LEVEL = minSup

    # Creates the first table C1
    def initTable(self) -> None:
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

    # Creates table Ck with empty supports
    def createNextTable(self,k) -> dict:
        nextTable = {}
        # Get list of current itemsets
        keys = list(self.TABLE.keys())
        # Create new sets by joining current itemsets
        for i in range(len(keys)):
            for j in range(i+1,len(keys)):
                flag = False
                newKey = set()
                set0 = keys[i]
                set1 = keys[j]

                newKey = set0.union(set1)
                if len(newKey) == k: # Stops empty keys or keys of varying size from being added to tables
                    # Check for infrequent subset
                    for item in newKey:
                        subset = newKey - {item}
                        if subset not in self.TABLE or self.TABLE[subset] < self.SUPPORT_LEVEL:
                            flag = True
                            break
                    # Only add newKey if not an infrequent subset
                    if not flag:
                        nextTable[frozenset(newKey)] = 0
        return nextTable

    # Adds supports to a table Ck then prunes table to create Lk
    def fillTable(self) -> None:
        for item in self.DATABASE:
            for key in self.TABLE.keys():
                if key.issubset(item):
                    self.TABLE[key] += 1
        self.prune() 
        self.SUPPORT_TABLE.update(self.TABLE) # Keeps track of subset supports 
    
    def prune(self) -> None:
        temp = self.TABLE.copy()
        for key in temp.keys():
            if self.TABLE[key] < self.SUPPORT_LEVEL:
                del self.TABLE[key]

    def getTable(self) -> dict:
        return self.TABLE

    def getSupports(self) -> dict:
        return self.SUPPORT_TABLE

    def setTable(self,table) -> None:
        self.TABLE = table
    
class Apriori:
    SUPPORT      = int
    TRANSACTIONS = []
    FINAL_TABLE  = Table
    CONFIDENCE   = int
    SUBSETS      = []
    RULES        = set()


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

        # Begin creating tables
        done = False
        k = 1
        table = Table(self.TRANSACTIONS,self.SUPPORT)
        t0 = timer()
        while not done:
            if k == 1: # Create first table (C1) from transactions
                table.initTable()
                table.setTable(table.getTable())
                k+=1
                continue
            # On all other iterations, overwrite the previous table if temp table isn't empty
            temp = table.createNextTable(k)
            if len(temp) > 0:
                table.setTable(temp)
                table.fillTable()
                k+=1
            else:
                self.FINAL_TABLE = table
                done = True

        #  Create subsets from frequent itemsets and init association rules
        self.SUBSETS = self.powerset(self.FINAL_TABLE.getTable().keys())
        self.RULES   = self.getRules()
        t1 = timer()
        print('|FPs| = ' + str(len(self.RULES)))
        self.writeFile()
        self.getRunTime(t0,t1)

    # Loops through all frequent item sets and creates powersets to later determine association rules
    def powerset(self,itemSets):
        powerset = set()
        for item in itemSets:
            for subset in chain.from_iterable(combinations(item,i) for i in range(len(item) + 1)):
                if len(subset) > 0: # Prevents empty sets from being added 
                    powerset.add(frozenset(subset))
        return list(powerset)[1:]
    
    # Loops through subsets and finds association rules based on user input
    def getRules(self):
        rules = set()
        keys  = self.FINAL_TABLE.getTable().keys()
        supportTable = self.FINAL_TABLE.getSupports()

        for key in keys:
            for subset in self.SUBSETS:
                if (supportTable[key] / supportTable[subset]) * 100 > self.CONFIDENCE:
                    rules.add(subset)
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

                for line in lines[1:]:
                    # Only grab the transactions from each row in the file
                    row = re.split(r'\t+',line)[-1].rstrip('\r\n').split()
                    self.TRANSACTIONS.append(row) # Add transaction to class transaction list
        except FileNotFoundError:
            print("Couldn't find file:",file,':(')
            exit()
    
    def writeFile(self):
        supportTable = self.FINAL_TABLE.getSupports()
        with open('./MiningResult.txt','w') as f:
            f.write('|FPs| = ' + str(len(self.RULES)) +'\n')
            for rule in self.RULES:
                f.write(str(sorted(list(rule))) + ' : ' + str(supportTable[rule]) + '\n')
Apriori()