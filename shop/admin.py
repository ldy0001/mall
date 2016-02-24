from django.contrib import admin
from shop import models
# Register your models here.
admin.site.register(models.Buser)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Consignees)
admin.site.register(models.Fuser)
admin.site.register(models.Goods)
admin.site.register(models.Order)
admin.site.register(models.OrderGoods)
admin.site.register(models.OrderStatus)
admin.site.register(models.PayMethod)
admin.site.register(models.Permission)
admin.site.register(models.Userstatus)