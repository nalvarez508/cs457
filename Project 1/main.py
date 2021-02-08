import os
from table import Table

workingDB = None

def inputCleaner(wordToRemove): # Removes ; and command
  UserQuery = UserQuery.replace(";", "")
  return UserQuery.replace(wordToRemove, "")

while (input != ".EXIT"):
  UserQuery = input("$ ")
  if (';' not in UserQuery): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database
  elif ("CREATE DATABASE" in UserQuery):
    dbName = inputCleaner("CREATE DATABASE ")
    os.system('mkdir ' + dbName)
    print(f"Created database {dbName}")
  
  # Deletes database
  elif ("DROP DATABASE" in UserQuery):
    dbName = inputCleaner("DROP DATABASE ")
    os.system('rmdir ' + dbName)
    print(f"Removed database {dbName}")
  
  # Sets currently active database
  elif ("USE" in UserQuery):
    workingDB = inputCleaner("USE ")
    os.system('cd ' + workingDB)
    print(f"Using database {workingDB}")

  # TODO
  # Creates a table with specified name and attributes
  elif ("CREATE TABLE" in UserQuery):
    tName = inputCleaner("CREATE TABLE ")

  # Deletes table
  elif ("DROP TABLE" in UserQuery):
    tName = inputCleaner("DROP TABLE ")
    os.system('rm ' + workingDB + '/' + tName + '.csv')
    print(f"Removed table {tName} from database {workingDB}")
  