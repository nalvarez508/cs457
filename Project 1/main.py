import os
from table import Table

workingDB = None
UserQuery = None
TableList = [None]

def inputCleaner(wordToRemove): # Removes ; and command
  query = UserQuery.replace(";", "")
  return query.replace(wordToRemove, "")

#def delimiterCleaner(string):
#  string2 = string.replace("(", " ")
#  string3 = string2.replace(")", " ")
#  return (string3.replace(",", " ")).split()

while (UserQuery != ".EXIT"):
  UserQuery = input("$ ")
  if (';' not in UserQuery and UserQuery != ".EXIT"): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database (working)
  elif ("CREATE DATABASE" in UserQuery):
    dbName = inputCleaner("CREATE DATABASE ")
    os.system('mkdir ' + dbName)
    print(f"Created database {dbName}")
  
  # Deletes database
  elif ("DROP DATABASE" in UserQuery):
    dbName = inputCleaner("DROP DATABASE ")
    os.system('rm -r ' + dbName)
    print(f"Removed database {dbName}")
  
  # Sets currently active database
  elif ("USE" in UserQuery):
    workingDB = inputCleaner("USE ")
    #os.system('cd ' + workingDB)
    print(f"Using database {workingDB}")

  # TODO
  # Creates a table with specified name and attributes
  elif ("CREATE TABLE" in UserQuery):
    tInput = inputCleaner("CREATE TABLE ")
    tName = tInput.split()[0]
    tRest = tInput.replace(tName, "")
    tAttrs0 = tRest[2:]
    tAttrs = tAttrs0[:-1]
    #tAttrs = tAttrs1.split(",")

    if (workingDB != None):
      os.system('touch ' + workingDB + '/' + tName + '.txt')
      #os.system('cd ' + workingDB)
      filename = workingDB + '/' + tName + '.txt'
      f = open(filename, 'w')
      f.write(f"{tName}|{tAttrs}|{workingDB}")
      f.close

  # Deletes table (working)
  elif ("DROP TABLE" in UserQuery):
    tName = inputCleaner("DROP TABLE ")
    os.system('rm ' + workingDB + '/' + tName + '.txt')
    print(f"Removed table {tName} from database {workingDB}")
  
  # TODO
  # Returns table elements as specified
  elif ("SELECT *" in UserQuery):
    selection = inputCleaner("SELECT * ")

  # TODO
  # Modifies table by adding attribute
  elif ("ALTER TABLE" in UserQuery):
    alterCmd = inputCleaner("ALTER TABLE ")

quit()