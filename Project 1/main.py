# Nick Alvarez, CS 657, PA1, Spring 21
# Python 3.7+ required.

import os
import subprocess
from table import Table

workingDB = None
UserQuery = None
TableList = [None]

def inputCleaner(wordToRemove): # Removes ; and command
  query = UserQuery.replace(";", "")
  return query.replace(wordToRemove, "")

def databaseExistenceCheck(db): # Checks if database exists
  if db not in subprocess.run(['ls', '|', 'grep', db], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

def tableExistenceCheck(t): # Checks if table exists
  if t not in subprocess.run(['ls', workingDB,  '|', 'grep', t], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

#def delimiterCleaner(string):
#  string2 = string.replace("(", " ")
#  string3 = string2.replace(")", " ")
#  return (string3.replace(",", " ")).split()

while (UserQuery != ".EXIT"):
  UserQuery = input("nickQL> ")
  if (';' not in UserQuery and UserQuery != ".EXIT"): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database (working)
  elif ("CREATE DATABASE" in UserQuery):
    dbName = inputCleaner("CREATE DATABASE ")
    if databaseExistenceCheck(dbName):
      os.system('mkdir ' + dbName)
      print(f"Created database {dbName}.")
    else:
      print(f"Could not create database {dbName} because it already exists.")
  
  # Deletes database (working)
  elif ("DROP DATABASE" in UserQuery):
    dbName = inputCleaner("DROP DATABASE ")
    if databaseExistenceCheck(dbName) == 0:
      os.system('rm -r ' + dbName)
      print(f"Removed database {dbName}.")
    else:
      print(f"Could not remove database {dbName} because it does not exist.")
  
  # Sets currently active database (working)
  elif ("USE" in UserQuery):
    workingDB = inputCleaner("USE ")
    #os.system('cd ' + workingDB)
    print(f"Using database {workingDB}.")

  # TODO
  # Creates a table with specified name and attributes
  elif ("CREATE TABLE" in UserQuery):
    # Splits input into separate strings
    tInput = inputCleaner("CREATE TABLE ")
    tName = tInput.split()[0]
    tRest = tInput.replace(tName, "")
    tAttrs0 = tRest[2:]
    tAttrs = tAttrs0[:-1]
    #tAttrs = tAttrs1.split(",")

    if (workingDB != None):
      if tableExistenceCheck(tName):
        os.system('touch ' + workingDB + '/' + tName + '.txt')
        #os.system('cd ' + workingDB)
        filename = workingDB + '/' + tName + '.txt'
        f = open(filename, 'w')
        f.write(f"{tAttrs}|{workingDB}")
        f.close
        print(f"Created table {tName}.")
      else:
        print(f"Could not create table {tName} because it already exists.")
    else:
      print("Please specify which database to use.")

  # Deletes table (working)
  elif ("DROP TABLE" in UserQuery):
    tName = inputCleaner("DROP TABLE ")
    if (workingDB != None):
      if tableExistenceCheck(tName) == 0:
        os.system('rm ' + workingDB + '/' + tName + '.txt')
        print(f"Removed table {tName} from database {workingDB}.")
      else:
        print(f"Could not remove table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  # TODO
  # Returns table elements as specified
  elif ("SELECT *" in UserQuery):
    selection = inputCleaner("SELECT * ")

  # TODO
  # Modifies table by adding attribute
  elif ("ALTER TABLE" in UserQuery):
    alterCmd = inputCleaner("ALTER TABLE ")
  

  elif ("DEL" in UserQuery):
    os.system('rm -r db_1 db_2')

#os.system('rm -r ' + workingDB)
quit()