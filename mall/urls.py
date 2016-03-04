"""mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from shop import views
urlpatterns = [
    url(r'^admin/',admin.site.urls),          
    url(r'^houtai/',views.houtai,name='houtai'),
    url(r'^$', views.index),
    url(r'^zhuce/$', views.zhuce,name='zhuce'),
    url(r'^login/$', views.denglu,name='login'),
	url(r'^zhuce/$', views.zhuce,name='zhuce'),
    url(r'^logout/$', views.zhuxiao,name='logout'),
    url(r'^profile/$', views.profile,name='profile'),
    url(r'^setpwd/$', views.setpwd,name='setpwd'),
    url(r'^search/$', views.search,name='search'),
    url(r'^list/(?P<id>[\d]+)/$', views.list),
    url(r'^item/(?P<id>[\d]+)/$', views.item),
    url(r'^cart/$', views.cart,name='cart'),
    url(r'^addcart/$', views.addcart,name='addcart'),
    url(r'^chgcart/$', views.chgcart,name='chgcart'),
    url(r'^delgood/$', views.delgood,name='delgood'),
    url(r'^orderid/$', views.orderid,name='orderid'),
    url(r'^pay/$', views.pay,name='pay'),
    url(r'^myorder/$', views.myorder,name='myorder'),
    url(r'^ordersearch/$', views.ordersearch,name='ordersearch'),
    url(r'^orderinfo/(?P<id>[\d]+)/$', views.orderinfo),
    url(r'^comment/(?P<id>[\d]+)/$', views.comment),
    url(r'^admin/$', views.houtai,name='admin'),
    url(r'^tuichu/$', views.tuichu,name='tuichu'),
    url(r'^manage/$', views.manage,name='manage'),
    url(r'^buser/$', views.buser,name='buser'),
    url(r'^buseradd/$', views.buseradd,name='buseradd'),
    url(r'^chgpwd/$', views.chgpwd,name='chgpwd'),
    url(r'^cate/$', views.cate,name='cate'),
    url(r'^goodlist/$', views.goodlist,name='goodslist'),
    url(r'^good/$', views.good,name='good'),
    url(r'^ordermodify/$', views.ordermodify,name='ordermodify'),
    url(r'^orderlist/$', views.orderlist,name='orderlist'),
    url(r'^fuser/$', views.fuser,name='fuser'),
    
]
