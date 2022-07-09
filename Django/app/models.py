from django.db import models

# 表管理
# 类名相当于表名
# 更新表结构时，执行python manage.py makemigrations  和   python manage.py migrate
# ############### 新建数据 ###############
"""
UserInfo.objects.create(userID=1806100072,
                        name="王添",
                        password="alvin",
                        age=21)
本质转译SQL: insert into app_UserInfo values(1806100072, "王添", "alvin", 21)
"""

# ############### 删除数据 ###############
"""
UserInfo.objects.filter(id=1).delete()
"""

# ############### 获取数据 ###############
"""
data_list[] = UserInfo.objects.all()
# data_list[] = [行(对象,封装了一行数据), 行(对象), 行(对象)] QuerySet类型

# 获取行对象数据:
for obj in data_list:
    print(obj.usrID, obj.name, obj.xxx)
    
# 直接获取第一行数据 (若预先知道该键值对应的行唯一) 
row_obj = UserInfo.objects.filter(id=1).first()
print (row_obj.name, row_obj.userID, xxx)
"""

# ############### 更新数据 ###############
"""
UserInfo.objects.all().update(password="123456")
UserInfo.objects.filter(id=2).update(password="123456")
UserInfo.objects.filter(name="王添").update(password="123456")
"""


# Create your models here.

class UserInfo(models.Model):
    userID = models.CharField(max_length=10)  # 学工号
    name = models.CharField(max_length=32)  # 姓名
    password = models.CharField(max_length=64)  # 密码
    age = models.IntegerField()


"""
create table app_userinfo(
    id big_int auto_increment primary key,
    name varchar (32),
    password varchar (64),
    age int,
)
"""
