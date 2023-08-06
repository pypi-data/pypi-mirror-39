import sqlite3 as sqlite



class SQLiteReader(ReportReader):
    def __init__(self, file_name, table_name = None, sheet_name = None):
        if table_name and sheet_name and (table_name != sheet_name):
            raise IOError, 'Redundant arguments: at most one of table_name and sheet_name can be specified.'
        
        self.file_name = file_name
        self.con = sqlite.connect(file_name)
        
        
        