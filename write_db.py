"""
write_db.py
数据库写操作实例 (insert update delete)
"""

import pymysql

# 连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password = '123456',
                     database = 'stu',
                     charset='utf8')

# 创建游标 (操作数据库语句,获取查询结果)
cur = db.cursor()

# 数据库操作
try:
    # 具体写操作
    # name = input("Name:")
    # age = input("Age:")
    # sex = input("Sex:")
    # score = input("Score:")

    # 直接构建sql语句
    # sql="insert into class_1 (name,age,sex,score) \
    # values ('%s',%s,'%s',%s)"%(name,age,sex,score)
    # cur.execute(sql)

    # 通过execute第二个参数列表构建sql语句
    # sql = "insert into class_1 (name,age,sex,score) \
    #  values (%s,%s,%s,%s)"
    # cur.execute(sql,[name,age,sex,score])

    # 修改操作
    # sql = "update interest set price=12800 " \
    #       "where name='Tom'"
    # cur.execute(sql)

    # 删除操作
    sql = "delete from class_1 where score < 80"
    cur.execute(sql)

    db.commit()
except Exception as e:
    db.rollback() # 如果提交异常则回到提交前的状态
    print(e)

# 关闭游标和数据库
cur.close()
db.close()



