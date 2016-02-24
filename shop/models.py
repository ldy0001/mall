#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#�û�״̬��
class Userstatus(models.Model):
    status=models.CharField(max_length=20,unique=True)  #״̬����
    def __unicode__(self):
        return self.status
#�û���Ϣ��
class Fuser(models.Model):
    username = models.CharField(max_length=20,unique=True)      #�û���
    password = models.CharField(max_length=256)                 #����
    name = models.CharField(max_length=30,null=True,blank=True) #����
    sex = models.CharField(max_length=2,null=True,blank=True)   #�Ա�
    birthday = models.DateField(null=True,blank=True)           #����
    email = models.EmailField(unique=True)                      #����
    tel = models.CharField(max_length=11,null=True,blank=True)  #�绰
    address = models.CharField(max_length=256,null=True,blank=True)#��ַ
    code = models.IntegerField(null=True,blank=True)            #�ʱ�
    createtime = models.DateTimeField(auto_now_add=True)        #ע��ʱ��
    status = models.ForeignKey('Userstatus')                    #�û�״̬
    def __unicode__(self):
        return self.name

#��Ʒ�����
class Category(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True,unique=True) #�������
    pid = models.ForeignKey('Category',null=True,blank=True)                         #���������
    def __unicode__(self):
        return self.name
    
#��Ʒ��Ϣ��
class Goods(models.Model):
    name = models.CharField(max_length=100,unique=True)                             #��Ʒ����
    category = models.ForeignKey('Category')                                        #��Ʒ��������
    price = models.DecimalField(max_digits=12,decimal_places=2,default='0.00')      #����
    sale_price = models.DecimalField(max_digits=12,decimal_places=2,default='0.00') #���ۼ۸�
    descriptiont = models.TextField(null=True,blank=True)                           #��Ʒ����
    amount = models.IntegerField(null=True,blank=True)                              #�������
    #pic = models.ImageField(null=True,blank=True)                                   #��ƷͼƬ
    status = models.IntegerField(null=True,blank=True)                              #��Ʒ״̬
    addtime = models.DateTimeField(auto_now_add=True)                               #��Ʒ���ʱ��
    paddr = models.CharField(max_length=30)                                         #��Ʒ����
    def __unicode__(self):
        return self.name

#��Ʒ���۱�
class Comment(models.Model):
    comment= models.TextField()                 #��������
    user=models.ForeignKey('Fuser')             #������
    commenttime = models.DateTimeField(auto_now_add=True)#����ʱ��
    goods= models.ForeignKey('Goods')           #���۵���Ʒ
    def __unicode__(self):
        return self.comment
    
#�ջ�����Ϣ��
class Consignees(models.Model):
    user = models.ForeignKey('Fuser')       #�û���
    name = models.CharField(max_length=20)  #�ջ�������
    addr = models.CharField(max_length=100) #�ջ��˵�ַ
    code = models.IntegerField(null=True,blank=True)#�ʱ�
    tel = models.CharField(max_length=11)           #��ϵ�绰
    def __unicode__(self):
        return self.name


#����״̬��
class OrderStatus(models.Model):
    status = models.CharField(max_length=20,unique=True)    #����״̬����
    def __unicode__(self):
        return self.status

#���ʽ
class PayMethod(models.Model):
    pay_name = models.CharField(max_length=20,unique=True)#���ʽ
    def __unicode__(self):
        return self.pay_name
    
#������
class Order(models.Model):
    order_serial = models.IntegerField(unique=True)     #���ɵĶ������
    user = models.ForeignKey('Fuser')                   #�µ���
    name = models.ForeignKey('Consignees')              #�ջ���
    pay = models.ForeignKey('PayMethod')                #���ʽ
    descriptiont = models.TextField(null=True,blank=True)       #��ע
    order_genrate_time = models.DateTimeField(auto_now_add=True)#��������ʱ��
    status = models.ForeignKey('OrderStatus')           #����״̬
    operator = models.ForeignKey('Buser')               #����Ա
    amount = models.DecimalField(max_digits=12,decimal_places=2)        #�����ܽ��
    def __unicode__(self):
        return self.order_serial
#������Ʒ��
class OrderGoods(models.Model):
    good = models.ForeignKey('Goods')          #��Ʒ
    price = models.DecimalField(max_digits=12,decimal_places=2)#����۸�
    amount = models.IntegerField()              #��������
    order_id =models.ForeignKey('Order')        #���ɵĶ������

#��̨�û���
class Buser(models.Model):
    username =models.CharField(max_length=20,unique=True)       #��̨�û���
    password = models.CharField(max_length=256)     #����
    name = models.CharField(max_length=20)          #����
    createtime = models.DateTimeField(auto_now_add=True)#���ʱ��
    permisson = models.ManyToManyField('Permission')#Ȩ��
    status = models.ForeignKey('Userstatus')       #�û�״̬
    def __unicode__(self):
        return self.name

#����Ȩ�ޱ�
class Permission(models.Model):
    name = models.CharField(max_length=100,unique=True)#�û�Ȩ������
    def __unicode__(self):
        return self.name
