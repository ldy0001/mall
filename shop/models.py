#_*_coding:utf-8_*_
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib

# Create your models here.
#用户状态表
class Userstatus(models.Model):
    status=models.CharField(max_length=20,unique=True)  #状态名称
    def __unicode__(self):
        return self.status
#用户信息表
class Fuser(models.Model):
    username = models.CharField(max_length=20,unique=True)      #用户名
    password = models.CharField(max_length=256)                 #密码
    name = models.CharField(max_length=30,null=True,blank=True) #姓名
    sex = models.CharField(max_length=2,null=True,blank=True)   #性别
    birthday = models.DateField(null=True,blank=True)           #生日
    email = models.EmailField(unique=True)                      #邮箱
    tel = models.CharField(max_length=11,null=True,blank=True)  #电话
    address = models.CharField(max_length=256,null=True,blank=True)#地址
    code = models.IntegerField(null=True,blank=True)            #邮编
    createtime = models.DateTimeField(auto_now_add=True)        #注册时间
    is_active = models.BooleanField() 
    def __unicode__(self):
        return unicode(self.username)                   
    #def save(self,*args,**kwargs):
    #    self.password = hashlib.sha1(self.passwd+self.user).hexdigest()
    #    super(Fuser,self).save(*args,**kwargs)  
    class Meta:  
        db_table = "fuser"  

#商品分类表
class Category(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True,unique=True) #类别名称
    pid = models.ForeignKey('Category',null=True,blank=True)                         #父级类别编号
    def __unicode__(self):
        return self.name
    
#商品信息表
class Goods(models.Model):
    name = models.CharField(max_length=100,unique=True)                             #商品名称
    category = models.ForeignKey('Category')                                        #商品所属分类
    price = models.DecimalField(max_digits=12,decimal_places=2,default='0.00')      #单价
    sale_price = models.DecimalField(max_digits=12,decimal_places=2,default='0.00') #销售价格
    descriptiont = models.TextField(null=True,blank=True)                           #商品描述
    amount = models.IntegerField(null=True,blank=True)                              #库存数量
    pic = models.ImageField(null=True,blank=True)                                   #商品图片
    status = models.IntegerField(null=True,blank=True)                              #商品状态
    addtime = models.DateTimeField(auto_now_add=True)                               #商品添加时间
    paddr = models.CharField(max_length=30)                                         #商品产地
    def __unicode__(self):
        return self.name

#商品评论表
class Comment(models.Model):
    comment= models.TextField()                 #评论内容
    user=models.ForeignKey('Fuser')             #评论人
    commenttime = models.DateTimeField(auto_now_add=True)#评论时间
    goods= models.ForeignKey('Goods')           #评论的商品
    def __unicode__(self):
        return self.comment
    
#收货人信息表
class Consignees(models.Model):
    user = models.ForeignKey('Fuser')       #用户名
    name = models.CharField(max_length=20)  #收货人姓名
    addr = models.CharField(max_length=100) #收货人地址
    code = models.IntegerField(null=True,blank=True)#邮编
    tel = models.CharField(max_length=11)           #联系电话
    def __unicode__(self):
        return self.name


#订单状态表
class OrderStatus(models.Model):
    status = models.CharField(max_length=20,unique=True)    #订单状态名称
    def __unicode__(self):
        return self.status

#付款方式
class PayMethod(models.Model):
    pay_name = models.CharField(max_length=20,unique=True)#付款方式
    def __unicode__(self):
        return self.pay_name
    
#订单表
class Order(models.Model):
    order_serial = models.CharField(max_length=32,unique=True)     #生成的订单编号
    user = models.ForeignKey('Fuser')                   #下单人
    name = models.ForeignKey('Consignees')              #收货人
    pay = models.ForeignKey('PayMethod')                #付款方式
    descriptiont = models.TextField(null=True,blank=True)       #备注
    order_genrate_time = models.DateTimeField(auto_now_add=True)#订单生成时间
    status = models.ForeignKey('OrderStatus')           #订单状态
    operator = models.ForeignKey('Buser')               #操作员
    amount = models.DecimalField(max_digits=12,decimal_places=2)        #订单总金额
    def __unicode__(self):
        return self.order_serial
#订单商品表
class OrderGoods(models.Model):
    good = models.ForeignKey('Goods')          #商品
    price = models.DecimalField(max_digits=12,decimal_places=2)#购买价格
    amount = models.IntegerField()              #购买数量
    order_id =models.ManyToManyField('Order')        #生成的订单编号
    def __unicode__(self):
        return self.good
#后台用户表
class Buser(models.Model):
    username =models.CharField(max_length=20,unique=True)       #后台用户名
    password = models.CharField(max_length=256)     #密码
    name = models.CharField(max_length=20)          #姓名
    createtime = models.DateTimeField(auto_now_add=True)#添加时间
    permisson = models.ManyToManyField('Permission')#权限
    is_active = models.BooleanField()       #用户状态 
    def __unicode__(self):
        return self.name  
    class Meta:  
        db_table = "buser"  

#操作权限表
class Permission(models.Model):
    name = models.CharField(max_length=100,unique=True)#用户权限名称
    def __unicode__(self):
        return self.name
#购物车条目
class CartItem(models.Model):
    good = models.ForeignKey('Goods')
    price = models.DecimalField(max_digits=8,decimal_places=2)
    count = models.IntegerField()