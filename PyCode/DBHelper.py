from msilib.schema import Error
import sqlite3 as sql


class DBManger:
    
    def __init__(self, db):
        self.db_name = db
    
    def insertStatement(self, table, **col):
        
        self.connect()
        id = 0
    
        try:
            
            self.cur.execute(f'''
                             INSERT INTO {table}({", ".join(col.keys())})
                             VALUES({", ".join(col.values())})
                             ''')
            id =  self.cur.lastrowid
            print("row added")
        except sql.Error as e:
            print(e)            
        finally:
            self.save()
            self.close()
            
            return id

    def updateStatement(self, table, condition=None, **col):
        colList = []
        for key, value in col.items():
            cond = f"{key} = {value}"
            colList.append(cond)
        column = ", ".join(colList)
        
        self.connect()
        try:
            self.cur.execute(f'''
                             update {table}
                             SET {column}
                             WHERE {condition}
                             ''')
            print("row updated")
        except sql.Error as e:
            print(e)
        finally:
            self.save()
            self.close()
    def deleteStatement(self, table, condition):       
        self.connect()
        try:
            self.cur.execute(f'''
                             DELETE FROM {table}
                             WHERE {condition}
                             ''')
            print("row deleted")
        except sql.Error as e:
            print(e)
        finally:
            self.save()
            self.close()
    def selectStatement(self, table, condition, columns) -> list:
        self.connect()
        try:
            self.cur.execute(f'''
                             SELECT {columns} FROM {table}
                             WHERE {condition}
                             ''')
            result = self.cur.fetchall()
            return result
        except sql.Error as e:
            print(e)
        finally:
            self.close()
    #########################################

    
    #########################################
    def connect(self):
        try:
            self.db = sql.connect(self.db_name)
            self.cur = self.db.cursor()
        except sql.Error as e:
            print(f"connectaion faild\n{e}")
            
    def close(self):
        if self.db:
            self.db.close()
    def save(self):
        self.db.commit()
        
    def backup(self):
        pass
    def rollBack(self):
        pass