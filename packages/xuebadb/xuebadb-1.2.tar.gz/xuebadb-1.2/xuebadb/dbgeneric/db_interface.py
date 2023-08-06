try:
    from mysql_interface import MySQLInterface
    from odbc_interface import ODBCInterface
except ImportError:
    from .mysql_interface import MySQLInterface
    from .odbc_interface import ODBCInterface

# Generic class that calls the appropriate DB class based on user's input
class DBInterface(ODBCInterface, MySQLInterface):
    dbtypelist = ['sql_server', 'mysql']
    
    def __init__(self, dbtype, server, username, password, dbname):
        if dbtype not in DBInterface.dbtypelist:
            raise Exception("DB type not supported. Ensure it's one of the following - {}".format(DBInterface.dbtypelist))
            
        self.dbtype = dbtype
        # for MySQL
        if self.dbtype == DBInterface.dbtypelist[0]:
            ODBCInterface.__init__(self, server, username, password, dbname)
        # for SQL Server
        elif self.dbtype == DBInterface.dbtypelist[1]:
            MySQLInterface.__init__(self, server, username, password, dbname)
            
    def querySelect(self, query):
        # for MySQL
        if self.dbtype == DBInterface.dbtypelist[0]:
            return ODBCInterface.select(self, query)
        # for SQL Server
        elif self.dbtype == DBInterface.dbtypelist[1]:
            return MySQLInterface.select(self, query)
