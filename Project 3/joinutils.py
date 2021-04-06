import dbutils
import os

def joinTableOpener(UserQuery, workingDB):
  joinType = 0
  if ('LEFT OUTER JOIN' in UserQuery.upper()):
    joinType = 1
  
  selLower = dbutils.inputCleaner("SELECT * FROM ", UserQuery)
  selection = dbutils.inputCleaner("select * from ", selLower)
  selection = selection.replace("inner join", "").replace("left outer join", "")
  commandWords = selection.replace(",","").split()
  # Employee E, Sales S where E.id = S.employeeID;
  # Employee E inner join Sales S on E.id = S.employeeID;

  ##### Grabbing values from commands
  table1Name = commandWords[0]
  table1Var = commandWords[1]
  table2Name = commandWords[2]
  table2Var = commandWords[3]

  table1Column = commandWords[5].split(".")[1]
  table2Column = commandWords[7].split(".")[1]
  comparisonOperator = dbutils.getOperand(commandWords[6])

  #### Importing tables into lists
  Table_1 = []
  Table_2 = []
  TableListNames = ['Table_1', 'Table_2']
  if workingDB != None:
    for x in TableListNames:
      if dbutils.tableExistenceCheck(x, workingDB):
        f = open(f'{workingDB}/{x}.txt', 'r')
        for line in f:
          x.append(line) #Turning tables into list of lines
        f.close()
      else:
        print(f"Could not query table {x} because it does not exist.")
  else:
    print("Please specify which database to use.")

  def joinOperandFunction():
    if (comparisonOperator == 0): #Equality
      if (type(t2.split()[t2.index(table2Column)]) is str):
        if (t2.split()[t2.index(table2Column)] == colValue):
          Table_Join.append(f'{t1} | {t2}')
      else:
        if (float(t2.split()[t2.index(table2Column)]) == float(colValue)):
          Table_Join.append(f'{t1} | {t2}')
    if (comparisonOperator == 1): #Greater than
      if (t2.split()[t2.index(table2Column)] > colValue):
        Table_Join.append(f'{t1} | {t2}')
    if (comparisonOperator == -1): #Less than
      if (t2.split()[t2.index(table2Column)] < colValue):
        Table_Join.append(f'{t1} | {t2}')
    if (comparisonOperator == -3): #Inequality
      if (t2.split()[t2.index(table2Column)] != colValue):
        Table_Join.append(f'{t1} | {t2}')

  if (joinType == 0):
    # Performs inner join, dropping values with no correspondence in other table
    def innerJoin():
      Table_Join = []
      for t1 in range(1, len(Table_1)):
        colValue = t1.split()[t1.index(table1Column)]
        for t2 in range(1, len(Table_2)):
          joinOperandFunction()
      for myTuple in Table_Join:
        print(myTuple)

    innerJoin()
  elif (joinType == 1):
    # Performs left outer join, keeping values without any correspondence
    def leftOuterJoin():
      Table_Join = []

    leftOuterJoin()