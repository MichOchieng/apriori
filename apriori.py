import re

class Apriori:
    NUM_TRANSACTIONS = int
    TRANSACTION_LIST = []
    SUPPORT = int

    def __init__(self,filename,support) -> None:
        self.SUPPORT = support
        self.readFile(filename)


    def initTable(self):
        pass

    def run(self):
        pass

    def readFile(self,file:str): 
        try:
            with open(file, 'r', encoding='utf-8') as f:
                # Pull lines from file
                lines = f.readlines()
                # Parse Transactions after first line in file
                    # Strip newline from end of string
                    # Split string into list of ints 
                for line in lines[1:]:
                    row = re.split(r'\t+',line)
                    items = row[-1].rstrip('\r\n')
                    itemList = [int(val) for val in items.split()]
                    self.TRANSACTION_LIST.append(itemList)
            print(self.TRANSACTION_LIST)     
        except FileNotFoundError:
            print("Couldn't find",file)

test = Apriori('test.txt',2)