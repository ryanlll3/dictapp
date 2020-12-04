"""
database handling module
design:
build a class of db handling, put the db operations which dict_server need to be here
create function for dict_server
"""
import hashlib
import pymysql

SALT = "#&Aid_"  # encrypt salt

class Database:
    def __init__(self,host='localhost',
                 port = 3306,
                 user = 'ryan',
                 passwd = 'ryan',
                 charset = 'utf8',
                 database = None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_database()  # Connect to database;

    # 连接数据库
    def connect_database(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.passwd,
                                  database = self.database,
                                  charset = self.charset)

    def close(self):
        self.db.close()

    def create_cursor(self):
        self.cur = self.db.cursor()

    def register(self,name,passwd):
        sql = "select * from user where name='%s'"%name
        self.create_cursor()
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False

        hash = hashlib.md5((name+SALT).encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()

        sql = "insert into user (name,passwd) \
        values (%s,%s)"

        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        hash = hashlib.md5((name+SALT).encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()

        sql = "select * from user where name='%s' and passwd = '%s'" % (name,passwd)
        self.create_cursor()
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False


    def query(self,word):
        sql = "select mean from words where word = '%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    def insert_history(self,name,word):
        sql = "insert into hist (name,word) values (%s, %s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)

    def history(self,name):
        sql = "select name,word,time from hist \
        where name = '%s' order by time desc \
        limit 10" % name
        self.cur.execute(sql)
        return self.cur.fetchall()


"""
create table user (name varchar(32) primary key,passwd varchar(8) not null);
"""

"""
create table class_1 (id int primary key auto_increment,
name varchar(32) not null,age int unsigned not null,sex enum('w','m'),
score float default 0.0);

# 创建游标 (操作数据库语句,获取查询结果)
cur = db.cursor()

# 数据库操作
cur.execute("insert into class_1 \
values (6,'Levi',11,'m',98);")

# 向数据库提交 (可以多次execute一次提交,只有写操作需要)
db.commit()

# 关闭游标和数据库
cur.close()
db.close()

"""




