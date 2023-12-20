from django.db import models

# Create your models here.



class Permissions(models.Model):
    permission_level = models.CharField(verbose_name='权限', max_length=32)
    def __str__(self):
        return self.permission_level


class Admin(models.Model):
    """管理员"""
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    Admin_level = models.ForeignKey(verbose_name='管理员权限', to='Permissions', to_field='id', on_delete=models.CASCADE,default=2)


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名' ,max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    account = models.CharField(verbose_name='账户余额', max_length=10, default=0)
    create_time = models.DateField(verbose_name='入职时间')

    # 级联删除， 如果部门被删除了，在这个部门下的员工一并被删除
    # 对于外键，django会自动加上_id 也就是depart = depart_id
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)

    # 创建了一个元组

    # 目的是为了节省存储空间
    # 在django中会自动帮助我们寻找对应元组的映射
    # obj.get_gender_display() 那么django会自动寻找gender_choices对应的映射
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name='性别')
    User_level = models.ForeignKey(verbose_name='员工权限', to='Permissions', to_field='id', on_delete=models.CASCADE, default=3)


class PrettyNum(models.Model):
    """手机号管理"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )

    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)





