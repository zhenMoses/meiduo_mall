from django.db import models

class BaseModel(models.Model):
    """模型基类"""
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',  auto_now=True)

    class Meta:
        abstract = True  # 表示此模型是一个抽象模型,将来迁移建表时,不会对它做迁移建表动作,它只用当其它模型的基类


