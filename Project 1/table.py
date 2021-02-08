class Table:
  
  def __init__(self, name, attributes, database):
    self.name = None #Name of the table
    self.attr = None #Table attributes
    self.db = None #Database table belongs to
  
  def getName(self):
    return self.name
  
  def getAttributes(self):
    return self.attr
  
  def getDatabase(self):
    return self.db
  
  def setAttributes(self, input):
    self.attr = input
  
  def printTable(self):
    return 0