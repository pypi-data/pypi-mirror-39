# coding=utf-8
import sqlite3

try:
    from . import mod_logger as logger
except Exception:
    import mod_logger as logger


class DataBase(object):

    def __init__(self, db):
        self._db = db

    def connect_sqlite(self):
        """
        连接数据库
        :return: 返回数据库链接
        """
        conn = False
        try:
            conn = sqlite3.connect(self._db)
        except Exception as data:
            logger.error("connect database failed, %s" % data)
            conn = False
        return conn

    def fetch_all(self, sql):
        """
        数据库查询
        :param sql: sql命令
        :return: 查询结果
        """
        res = ''
        if self._conn:
            try:
                self._cur.execute(sql)
                res = self._cur.fetchall()
            except Exception as data:
                res = False
                logger.error("query database exception, %s \n %s" % (data, sql))
        return res

    def update(self, sql):
        """
        数据库更新
        :param sql: sql命令
        :return: 提交成功或失败
        """
        flag = False
        if self._conn:
            try:
                self._cur.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as data:
                flag = False
                logger.error("updata database exception, %s \n %s" % (data, sql))
        return flag

    def close(self):
        """
        关闭数据库链接
        :return:
        """
        if self._conn:
            try:
                if (type(self._cur) == "object"):
                    self._cur.close()
                if (type(self._conn) == "object"):
                    self._conn.close()
            except Exception as data:
                logger.error("close database exception, %s, %s, %s" %(
                    data, type(self._cur), type(self._conn)
                ))
    def __enter__(self):
        self._conn = self.connect_sqlite()
        if self._conn:
            self._cur = self._conn.cursor()
        return self._cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            try:
                if isinstance(self._cur, sqlite3.Cursor):
                    self._cur.close()
                if isinstance(self._conn, sqlite3.Connection):
                    self._conn.close()
            except Exception as data:
                logger.error("close database exception, %s, %s, %s" %(
                    data, type(self._cur), type(self._conn)
                ))


if __name__ == '__main__':
    d = DataBase("monkey.db")
    with d:
        d.update("create table cloudperformence (action text, cpu text, mem text, activity text)")
        d.update('INSERT into cloudperformence values ("swipe", "0%", "174168", "com.cubic.autohome/com.autohome.plugin.assistant.mvp.ui.activity.FaceCameraActivity")')
        # d.update('insert into books values ("from beginner to master", "laoqi", "python")')
        print("haha")
