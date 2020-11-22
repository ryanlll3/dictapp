"""
图片存储
create table images (id int primary key auto_increment,filename varchar(32),image mediumblob);
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

# 存储图片
# with open('timg.jpeg','rb') as f:
#     data = f.read()
#
# try:
#     sql = "insert into images values (1,'jd',%s)"
#     cur.execute(sql,[data])
#     db.commit()
# except:
#     db.rollback()

# 提取图片
sql = "select image from images where filename='jd'"
cur.execute(sql)
data = cur.fetchone()
with open('jd.jpeg','wb') as f:
    f.write(data[0])

# 关闭游标和数据库
cur.close()
db.close()

