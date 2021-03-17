# Nick Alvarez, CS 657, PA2, Spring 21
# Python 3.7+ required.

# Utility file for table value modification

import os
import shlex
import subprocess
import dbutils

def insertTuple(UserQuery, workingDB):
  tInput = dbutils.inputCleaner("insert into ", UserQuery)
  tName = tInput.split()[0] # Grabs table name
  tRest = tInput.replace(tName, "").replace(" values", "")
  tAttrs0 = tRest[2:] # Leaves only string with attributes
  tAttrs1 = tAttrs0[:-1] # See above
  tAttrs = tAttrs1.split(",") # Creates list from attributes
  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'
      f = open(filename, 'a')
      f.write(" |".join(tAttrs)) # Writes list to file with pipe delimiter
      f.close()
      print(f"1 new record inserted into {tName}.")
    else:
      print(f"Could not add values to {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")