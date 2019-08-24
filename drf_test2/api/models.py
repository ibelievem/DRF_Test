from django.db import models

# Create your models here.


# 保存用户信息
class UserInfo(models.Model):
    user_type_choices=(
        (1,"普通用户"),
        (2,"VIP"),
        (3,"SVIP"),
    )
    user_type=models.IntegerField(choices=user_type_choices)
    username=models.CharField(max_length=32,unique=True)
    password=models.CharField(max_length=64)


# 保存用户 token
class UserToken(models.Model):
    user=models.OneToOneField(to="UserInfo")
    token=models.CharField(max_length=64)
