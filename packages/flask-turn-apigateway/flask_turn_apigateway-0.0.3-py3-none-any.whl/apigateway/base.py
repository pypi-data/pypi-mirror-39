import pymysql
from pymysql.cursors import DictCursor
from apigateway.format import SqlStatement

# database setting
# db_host = environ.get('DBHOST', 'localhost')
# db_user = environ.get('DBUSER', 'test')
# db_pass = environ.get('DBPASS', 'test')
# db_name = environ.get('DBNAME', 'hawa')

db_host = "hawa2-django.cl5n467td4ui.rds.cn-northwest-1.amazonaws.com.cn"
db_user = "hawa2"
db_pass = "4oi2IMO48mz9"
db_name = "hawa_admin"


class DB:
    def __init__(self, host=db_host, db=db_name, usr=db_user, pwd=db_pass):
        self.err = None
        self.conn = self.make_connection(host, db, usr, pwd)
        self.cursor = self.conn.cursor()
        self.dict_cursor = self.conn.cursor(DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def make_connection(host, db, usr, pwd):
        return pymysql.connect(host=host, db=db, user=usr, passwd=pwd)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, sql: SqlStatement):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def query_dict(self, sql: SqlStatement):
        self.dict_cursor.execute(sql)
        return self.dict_cursor.fetchone()

    def query_many(self, sql: SqlStatement):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_many_dict(self, sql: SqlStatement):
        self.dict_cursor.execute(sql)
        return self.dict_cursor.fetchall()

    def exe_and_commit(self, sql: SqlStatement):
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, sql: SqlStatement):
        self.exe_and_commit(sql)

    def update(self, sql: SqlStatement):
        self.exe_and_commit(sql)

    def delete(self, sql: SqlStatement):
        self.exe_and_commit(sql)


class Case(DB):
    def __init__(self, host=db_host, db=db_name, usr=db_user, pwd=db_pass):
        super(Case, self).__init__(host=host, db=db, usr=usr, pwd=pwd)

    def query_user(self, username: str):
        """user:id,username,email,phone"""
        sql = f"SELECT id,username,email,phone FROM users WHERE username='{username}'" \
            f" AND role='A'"
        sql = SqlStatement(sql)
        user = self.query(sql)
        return user
