import mysql.connector
import pandas as pd

class MySQLInterface:    
    def __init__(self, server, username, password, dbname):
        self.server = server
        self.username = username
        self.password = password
        self.dbname = dbname
        
    def __connect(self):        
        try:
            self.cnx = mysql.connector.connect(user=self.username, password=self.password, host=self.server, database=self.dbname)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
            
    def select(self, query):
        if(not self.__connect()):
            return None
        try:
            output = []
            cursor = self.cnx.cursor()
            cursor.execute(query)
            for row in cursor:
                inner_list = []
                for val in row:
                    inner_list.append(str(val).strip())
                output.append(inner_list)
            cursor.close()
            self.cnx.close()
            return pd.DataFrame(output)
        except:
            print("Cannot perform the SELECT query.")
            return False
