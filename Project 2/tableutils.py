# Nick Alvarez, CS 657, PA2, Spring 21
# Python 3.7+ required.

# Utility file for table value modification

import os
import subprocess
import dbutils

# Inserts a record into the table
def insertTuple(UserQuery, workingDB):
  tInput = dbutils.inputCleaner("insert into ", UserQuery)

  tName = tInput.split()[0] # Grabs table name
  tRest = tInput.replace(tName, "").replace(" values", "")#.replace('\t', "").replace(" ", "")
  tAttrs0 = tRest[1:] # Leaves only string with attributes
  tAttrs1 = tAttrs0[:-1] # See above
  tAttrs = tAttrs1.split(",") # Creates list from attributes

  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'
      f = open(filename, 'a')
      f.write('\n')
      f.write(" |".join(tAttrs)) # Writes list to file with pipe delimiter
      f.close()
      print(f"1 new record inserted into {tName}.")
    else:
      print(f"Could not add values to {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")

# Updates a record in the table
def updateTuple(UserQuery, workingDB):
  tInput = dbutils.inputCleaner("update ", UserQuery)

  tName = tInput.split()[0] # Grabs table name
  setColumn = tInput.split()[2] # Gets "set" column
  setRecord = tInput.split()[4]#.replace("'", "") # Gets "set" record
  whereColumn = tInput.split()[6] # Gets "where" column
  whereRecord = tInput.split()[8]#.replace("'", "") # Gets "where" record

  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'

      # No way to modify middle of file, so we recreate it
      f = open(filename, 'r')
      tempFile = f.readlines()
      f.close()

      count = 0
      mods = 0
      setColumnNum = 0
      whereColumnNum = 0
      for line in tempFile:
        if (count == 0): # Headers
          columnList = line.split()
          del columnList[1::3]
          setColumnNum = columnList.index(setColumn)
          whereColumnNum = columnList.index(whereColumn)
        if (count > 0): # Values
          tupleDetails = line.split()
          if (tupleDetails[whereColumnNum] == whereRecord):
            if ((setColumnNum+2) > len(tupleDetails)):
              tupleDetails[setColumnNum] = f'{setRecord}\n'
            else:
              tupleDetails[setColumnNum] = setRecord
            tempFile[count] = ' '.join(tupleDetails)
            mods += 1
        count += 1
      
      os.system(f'truncate -s 0 {workingDB}/{tName}.txt')

      f = open(filename, 'w')
      for line in tempFile:
        f.write(line)
      f.close()

      print(f"{mods} record(s) modified in {tName}.")
    else:
      print(f"Could not update values in {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")

# Removes a record from the table
def deleteTuple(UserQuery, workingDB):
  tInput = dbutils.inputCleaner("delete from ", UserQuery)

  tName = tInput.split()[0] # Grabs table name
  whereColumn = tInput.split()[2] # Gets "where" column
  whereRecord = tInput.split()[4]#.replace("'", "") # Gets "where" record

  operand = dbutils.getOperand(tInput.split()[3])

  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'

      # No way to modify middle of file, so we recreate it
      f = open(filename, 'r')
      tempFile = f.readlines()
      f.close()

      count = 0
      mods = 0
      whereColumnNum = 0
      for line in tempFile:
        if (count == 0): # Headers
          columnList = line.split()
          del columnList[1::3]
          whereColumnNum = columnList.index(whereColumn)
        if (count > 0): # Values
          tupleDetails = line.split()
          def deleteTupleHelper(mods):
            if (operand == 0): # Equality
              # The type checking here handles strings and numbers separately
              # Ex. 150 or 150.00 would not find 150.00 or 150, respectively
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  tempFile[count] = None
                  mods += 1
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  tempFile[count] = None
                  mods += 1
            elif (operand == 1): # Greater than
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                tempFile[count] = None
                mods += 1
            elif (operand == -1): # Less than
              if (float(tupleDetails[whereColumnNum]) < float(whereRecord)):
                tempFile[count] = None
                mods += 1
            #TODO
            # Add != action
            return mods
          mods = deleteTupleHelper(mods)
        count += 1
      
      os.system(f'truncate -s 0 {workingDB}/{tName}.txt')

      f = open(filename, 'w')
      for line in tempFile:
        if (line != None):
          f.write(line)
      f.close()

      print(f"{mods} record(s) removed in {tName}.")
    else:
      print(f"Could not remove values in {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")