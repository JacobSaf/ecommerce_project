from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
import pymysql

pymysql.install_as_MySQLdb()

print("Custom MySQL backend LOADED")


class DatabaseWrapper(MySQLDatabaseWrapper):
    pass