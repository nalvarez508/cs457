# Nick Alvarez, CS 657, PA2, Spring 21
# Python 3.7+ required.

# Main driver file

import os
import shlex
import subprocess

import dbutils
import tableutils
import queryutils

workingDB = None
UserQuery = None
TableList = [None]

while (UserQuery != ".EXIT"):
  UserQuery = input("nickQL> ")
  if (';' not in UserQuery and UserQuery != ".EXIT"): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database
  elif ("CREATE DATABASE" in UserQuery.upper()):
    dbName = dbutils.inputCleaner("CREATE DATABASE ", UserQuery)
    if dbutils.databaseExistenceCheck(dbName) == 0:
      os.system(f'mkdir {dbName}')
      print(f"Created database {dbName}.")
    else:
      print(f"Could not create database {dbName} because it already exists.")
  
  # Deletes database
  elif ("DROP DATABASE" in UserQuery.upper()):
    dbName = dbutils.inputCleaner("DROP DATABASE ", UserQuery)
    if dbutils.databaseExistenceCheck(dbName):
      os.system(f'rm -r {dbName}')
      print(f"Removed database {dbName}.")
    else:
      print(f"Could not remove database {dbName} because it does not exist.")
  
  # Sets currently active database
  elif ("USE" in UserQuery.upper()):
    workingDB = dbutils.inputCleaner("USE ", UserQuery)
    #os.system('cd ' + workingDB)
    if dbutils.databaseExistenceCheck(workingDB):
      print(f"Using database {workingDB}.")
    else:
      print(f"Could not use database {workingDB} because it does not exist.")

  # Creates a table with specified name and attributes
  elif ("CREATE TABLE" in UserQuery.upper()):
    # Splits input into separate strings
    tInput = dbutils.inputCleaner("CREATE TABLE ", UserQuery)
    tName = tInput.split()[0] # Grabs table name
    tRest = tInput.replace(tName, "")
    tAttrs0 = tRest[2:] # Leaves only string with attributes
    tAttrs1 = tAttrs0[:-1] # See above
    tAttrs = tAttrs1.split(",") # Creates list from attributes

    if (workingDB != None):
      if dbutils.tableExistenceCheck(tName, workingDB) == 0:
        os.system(f'touch {workingDB}/{tName}.txt')
        filename = workingDB + '/' + tName + '.txt'
        f = open(filename, 'w')
        f.write(" |".join(tAttrs)) # Writes list to file with pipe delimiter
        f.close()
        print(f"Created table {tName}.")
      else:
        print(f"Could not create table {tName} because it already exists.")
    else:
      print("Please specify which database to use.")

  # Deletes table
  elif ("DROP TABLE" in UserQuery.upper()):
    tName = dbutils.inputCleaner("DROP TABLE ", UserQuery)
    if (workingDB != None):
      if dbutils.tableExistenceCheck(tName, workingDB):
        os.system(f'rm {workingDB}/{tName}.txt')
        print(f"Removed table {tName} from database {workingDB}.")
      else:
        print(f"Could not remove table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  # Returns table elements as specified
  elif ("SELECT" in UserQuery.upper()):
    if ("SELECT *" in UserQuery.upper()):
      queryutils.queryAll(UserQuery, workingDB)
    else:
      queryutils.querySpecific(UserQuery, workingDB)

  # Modifies table by adding attribute
  elif ("ALTER TABLE" in UserQuery.upper()):
    alter = dbutils.inputCleaner("ALTER TABLE ", UserQuery)
    tName = alter.split()[0] # Grabs table name
    alterCmd = alter.split()[1] # Grabs command (ADD, etc)
    alterRest1 = alter.replace(tName, "")
    alterRest2 = alterRest1.replace(alterCmd, "") # Left with attributes, currently only supports one
    newAttr = alterRest2[2:] # May have issue with leading parentheses

    if workingDB != None:
      if dbutils.tableExistenceCheck(tName, workingDB):
        f = open(f'{workingDB}/{tName}.txt', 'a')
        f.write(f" | {newAttr}") # Appends attribute to file with pipe delimiter
        f.close()
        print(f"Modified table {tName}.")
      else:
        print(f"Could not modify table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  elif ("INSERT INTO" in UserQuery.upper()):
    tableutils.insertTuple(UserQuery, workingDB)
  
  elif ("UPDATE" in UserQuery.upper()):
    tableutils.updateTuple(UserQuery, workingDB)
  
  elif ("DELETE FROM" in UserQuery.upper()):
    tableutils.deleteTuple(UserQuery, workingDB)

  # Testing purposes, deletes databases to start fresh
  elif ("DEL" in UserQuery):
    os.system('rm -r CS457_PA2')
  
  elif (".EXIT" != UserQuery):
    print("I don't know what you want me to do.")

quit()