# Nick Alvarez, CS 657, PA1, Spring 21
# Python 3.7+ required.

import os
import shlex
import subprocess

workingDB = None
UserQuery = None
TableList = [None]

def inputCleaner(wordToRemove): # Removes ; and command
  query = UserQuery.replace(";", "")
  return query.replace(wordToRemove, "")

def databaseExistenceCheck(db): # Checks if database exists
  if db in subprocess.run(['ls', '|', 'grep', db], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

def tableExistenceCheck(t): # Checks if table exists
  if t in subprocess.run(['ls', workingDB,  '|', 'grep', t], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

while (UserQuery != ".EXIT"):
  UserQuery = input("nickQL> ")
  if (';' not in UserQuery and UserQuery != ".EXIT"): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database
  elif ("CREATE DATABASE" in UserQuery):
    dbName = inputCleaner("CREATE DATABASE ")
    if databaseExistenceCheck(dbName) == 0:
      os.system(f'mkdir {dbName}')
      print(f"Created database {dbName}.")
    else:
      print(f"Could not create database {dbName} because it already exists.")
  
  # Deletes database
  elif ("DROP DATABASE" in UserQuery):
    dbName = inputCleaner("DROP DATABASE ")
    if databaseExistenceCheck(dbName):
      os.system(f'rm -r {dbName}')
      print(f"Removed database {dbName}.")
    else:
      print(f"Could not remove database {dbName} because it does not exist.")
  
  # Sets currently active database
  elif ("USE" in UserQuery):
    workingDB = inputCleaner("USE ")
    #os.system('cd ' + workingDB)
    if databaseExistenceCheck(workingDB):
      print(f"Using database {workingDB}.")
    else:
      print(f"Could not use database {workingDB} because it does not exist.")

  # Creates a table with specified name and attributes
  elif ("CREATE TABLE" in UserQuery):
    # Splits input into separate strings
    tInput = inputCleaner("CREATE TABLE ")
    tName = tInput.split()[0] # Grabs table name
    tRest = tInput.replace(tName, "")
    tAttrs0 = tRest[2:] # Leaves only string with attributes
    tAttrs1 = tAttrs0[:-1] # See above
    tAttrs = tAttrs1.split(",") # Creates list from attributes

    if (workingDB != None):
      if tableExistenceCheck(tName) == 0:
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
  elif ("DROP TABLE" in UserQuery):
    tName = inputCleaner("DROP TABLE ")
    if (workingDB != None):
      if tableExistenceCheck(tName):
        os.system(f'rm {workingDB}/{tName}.txt')
        print(f"Removed table {tName} from database {workingDB}.")
      else:
        print(f"Could not remove table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  # Returns table elements as specified
  elif ("SELECT *" in UserQuery):
    selection = inputCleaner("SELECT * FROM ")
    #cmd = shlex.split(f"cat {workingDB}/{selection}.txt")
    #subprocess.Popen(cmd)
    if workingDB != None:
      if tableExistenceCheck(selection):
        f = open(f'{workingDB}/{selection}.txt', 'r')
        print(f.read())
        f.close()
      else:
        print(f"Could not query table {selection} because it does not exist.")
    else:
      print("Please specify which database to use.")

  # Modifies table by adding attribute
  elif ("ALTER TABLE" in UserQuery):
    alter = inputCleaner("ALTER TABLE ")
    tName = alter.split()[0] # Grabs table name
    alterCmd = alter.split()[1] # Grabs command (ADD, etc)
    alterRest1 = alter.replace(tName, "")
    alterRest2 = alterRest1.replace(alterCmd, "") # Left with attributes, currently only supports one
    newAttr = alterRest2[2:] # May have issue with leading parentheses

    if workingDB != None:
      if tableExistenceCheck(tName):
        f = open(f'{workingDB}/{tName}.txt', 'a')
        f.write(f" | {newAttr}") # Appends attribute to file with pipe delimiter
        f.close()
        print(f"Modified table {tName}.")
      else:
        print(f"Could not modify table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  # Testing purposes, deletes databases to start fresh
  #elif ("DEL" in UserQuery):
  #  os.system('rm -r db_1 db_2')

quit()