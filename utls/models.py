from django.db import models

class BaseModel(models.Model):
    '''模型基类'''

    #创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    #更改时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    #删除标识,默认不删除
    delete = models.BooleanField(default=False,verbose_name='是否删除')
    class Meta:
        #需要指定基类模型类为抽象的,否则迁移生成表时会出错
        abstract=True