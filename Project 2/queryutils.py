# Nick Alvarez, CS 657, PA2, Spring 21
# Python 3.7+ required.

# Utility file for table queries

import os
import subprocess
import dbutils

def queryAll(UserQuery, workingDB):
  selLower = dbutils.inputCleaner("SELECT * FROM ", UserQuery)
  selection = dbutils.inputCleaner("select * from ", selLower)
  if workingDB != None:
    if dbutils.tableExistenceCheck(selection, workingDB):
      f = open(f'{workingDB}/{selection}.txt', 'r')
      print(f.read())
      f.close()
    else:
      print(f"Could not query table {selection} because it does not exist.")
  else:
    print("Please specify which database to use.")

def querySpecific(UserQuery, workingDB):
  selLower = dbutils.inputCleaner("SELECT ", UserQuery)
  selection = dbutils.inputCleaner("select ", selLower)

  selectColumns = selection.replace(",", "").split()
  selectColumns = selectColumns[:selectColumns.index("from")]

  tName = selection.split()[len(selectColumns)+1]

  whereColumn = selection.split()[len(selectColumns)+3]
  whereRecord = selection.split()[len(selectColumns)+5]
  operand = dbutils.getOperand(selection.split()[len(selectColumns)+4])

  if workingDB != None:
    if dbutils.tableExistenceCheck(tName, workingDB):
      f = open(f'{workingDB}/{tName}.txt', 'r')
      tempFile = f.readlines()
      f.close()

      selectColumnNums = []
      columnNameString = ""
      listToReturn = []
      count = 0
      for line in tempFile:
        if (count == 0): # Headers
          # Finding the indexes of select and where columns
          columnList = line.split()
          del columnList[1::3]
          columnCount = 0
          for word in columnList:
            if word in selectColumns:
              selectColumnNums.append(columnCount)
            if (word == whereColumn):
              whereColumnNum = columnCount
            columnCount += 1

          # Creating a table header for the selected columns
          for index in selectColumnNums:
            columnNameString += columnList[index]
            columnNameString += " | "
          queryHeader = columnNameString[:-3]
          listToReturn.append(queryHeader)

        if (count > 0): # Values
          tupleDetails = line.split()
          def querySpecificHelper():
            def queryStringMaker():
              queryString = ""
              for index in selectColumnNums:
                queryString += tupleDetails[index]
                queryString += " | "
              queryResult = queryString[:-3]
              listToReturn.append(queryResult)
            if (operand == 0): # Equality
              # The type checking here handles strings and numbers separately
              # Ex. 150 or 150.00 would not find 150.00 or 150, respectively
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  queryStringMaker()
            elif (operand == 1): # Greater than
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                queryStringMaker()
            elif (operand == -1): # Less than
              if (float(tupleDetails[whereColumnNum]) < float(whereRecord)):
                queryStringMaker()
            elif (operand == -3): # Inequality
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] != whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) != float(whereRecord)):
                  queryStringMaker()
          querySpecificHelper()
        count += 1
      for line in listToReturn:
        print(line)

    else:
      print(f"Could not query table {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")