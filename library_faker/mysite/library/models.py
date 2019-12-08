from django.db import models

# Create your models here.

class CookieModel(models.Model):
    ip = models.GenericIPAddressField()
    cookies = models.CharField(max_length=128)
    # 存储记录的时间
    last_time = models.BigIntegerField(null=True)
