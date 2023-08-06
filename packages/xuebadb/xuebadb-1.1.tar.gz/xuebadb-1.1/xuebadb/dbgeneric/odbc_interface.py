import pyodbc
import pandas

class ODBCInterface:
    def __init__(self, server, username, password, dbname):
        self.server = server
        self.username = username
        self.password = password
        self.dbname = dbname
        
    def __connect(self): #private
        try:
            self.cnx = pyodbc.connect("""DRIVER={ODBC Driver 17 for SQL Server};
                                      SERVER=""" + str(self.server) + """;
                                      DATABASE=""" + str(self.dbname) + """;
                                      UID=""" + str(self.username) + """;
                                      PWD=""" + str(self.password))
            return True
        except pyodbc.Error as err:
            print(err)
            return False
            
    def select(self, query):
        if(not self.__connect()):
            return None
        try:
            cursor = self.cnx.cursor()
            cursor.execute(query) 
            output = []
            for row in cursor:
                inner_list = []
                for val in row:
                    inner_list.append(str(val).strip())  #remove trailing white spaces to create a dataframe
                output.append(inner_list)
            cursor.close()
            self.cnx.close()
            return pandas.DataFrame(output)
        except:
            print("Cannot perform the SELECT query.")
            return False
