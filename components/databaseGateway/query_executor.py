import mysql.connector # pip install mysql-connector-python
from mysql_db import DBConfig


class QueryExecutor:
    def __init__(self, logging_manager):
        self.CFG = DBConfig()
        self.LOG_MGR = logging_manager
    
    
    def execute_query(self, query):
        self.LOG_MGR.set_log_type("db")
        
        cnx = None
        cursor = None
        try:
            # Establish a connection to the database
            cnx = mysql.connector.connect(user=self.CFG.user, 
                                          password=self.CFG.password,
                                          host=self.CFG.host,
                                          database=self.CFG.database)

            # Create a cursor object
            cursor = cnx.cursor()

            # Execute the query
            cursor.execute(query)
            
            return_data = {
                "status": None,
                "status_message": "OK",
                "rows": None,
                "num_rows": None,
                "affected_rows": None
            }
            
            # If the query was an INSERT, UPDATE, or DELETE query, commit the changes
            if query.lstrip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                cnx.commit()
                return_data["affected_rows"] = cursor.rowcount
            else:
                # Fetch all the rows
                return_data["rows"] = cursor.fetchall()
                return_data["num_rows"] = cursor.rowcount
            
            # Return the result
            return return_data
        
        except mysql.connector.Error as err:
            self.LOG_MGR.log(f"DB Connection error: {err}")
            return_data = {
                "status": "ERROR",
                "status_message": err,
                "rows": None,
                "num_rows": None,
                "affected_rows": None
            }
            
            return return_data
                
        finally:
            # Executed this whether an exception is raised or not
            if cursor is not None:
                cursor.close()
            if cnx is not None:
                cnx.close()
    
    
    def clean_database(self):
        cnx = None
        try:
            # Establish a connection to the database
            cnx = mysql.connector.connect(user=self.CFG.user, 
                                          password=self.CFG.password,
                                          host=self.CFG.host,
                                          database=self.CFG.database)

            # Create a cursor object
            cursor = cnx.cursor()

            # Get all table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            # Truncate each table
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table[0]}")
                
            return True
        except mysql.connector.Error as err:
            self.LOG_MGR.log(f"DB Connection error: {err}")
            # If an exception was raised, the connection was not successful
            return False
        finally:
            cursor.close()
            # Close the connection if it was opened
            if cnx is not None:
                cnx.close()
        

    def test_connection(self):
        cnx = None
        try:
            # Attempt to establish a connection to the database
            cnx = mysql.connector.connect(user=self.CFG.user, 
                                          password=self.CFG.password,
                                          host=self.CFG.host,
                                          database=self.CFG.database)
            
            # If no exception was raised, the connection was successful
            return True
        except mysql.connector.Error as err:
            self.LOG_MGR.log(f"DB Connection error: {err}")
            # If an exception was raised, the connection was not successful
            return False
        finally:
            # Close the connection if it was opened
            if cnx is not None:
                cnx.close()
                
                
# Use the function
# query = 'SELECT * FROM your_table'
# result = query_database(query)
# for row in result:
#     print(row)