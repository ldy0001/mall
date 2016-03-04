#_*_coding:utf-8_*_
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
import models,hashlib
from shop.models import Category
from django.template.loader import get_template
import re
# Create your views here.


#购物车类    
class Cart(object):
    def __init__(self, *args, **kwargs):
        self.items = []
        print self.items
        self.total_price = 0.00
        print 'self.total_price的类型是：',type(self.total_price)
    def add_good(self,good):
        print 'good.sale_price的类型是：',type(good.sale_price)
        self.total_price += float(good.sale_price)
        print self.total_price
        for item in self.items:
            if item.good.id == good.id:
                item.count += 1
                return
        self.items.append(models.CartItem(good=good,price=good.sale_price,count=1))
    def chg_good(self,good,num):
         for item in self.items:
            if item.good.id == good.id:
                item.count = num
                return
    def del_good(self,good):
        for item in self.items:
            if item.good.id==good.id:
                print 'goodid',good.id
                print 'item.good.id',item.good.id
                self.items.remove(item)
                self.total_price = self.total_price-float(item.good.sale_price*item.count)
                for i in self.items:
                    print i.good
                return  

def check_session(func):
    def wrapper(request,*args, **kv):
        userinfo=request.session.get('myuser',None) 
        print userinfo
        if not userinfo:
            return HttpResponseRedirect('/login/')
        return func(request,*args, **kv)
    return wrapper

def index(request):
    if request.session.get("cart") is None:
        cart = Cart()
        print 'ccar',cart.items
        request.session["cart"] = cart
    cart = request.session.get("cart")
    if request.session.get("myuser") is  None:
        request.session["myuser"]=''
    user=request.session.get("myuser")
    cate=models.Category.objects.filter(pid=None)
    print cate
    cate2=models.Category.objects.all()
    goods=models.Goods.objects.all()
    return render(request,'index.html',{'cate':cate,'goods':goods,'cate2':cate2,'cart':cart,'user':user},context_instance=RequestContext(request))


def zhuce(request):
    if request.method=='POST':
        username=request.POST.get('username')
        print username
        password=request.POST.get('pwd')
        password_try=request.POST.get('pwd_try')
        if password==password_try:
            try:
                userobj=models.Fuser.objects.get(username=username)
                print userobj
            except Exception,e:     
                email=request.POST.get('email')
                if len(email)>5:
                    if re.match("^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$", email)!=None:
                        userobj=models.Fuser(username=username,password=password,email=email,is_active=True)
                        userobj.save()
                        return render(request,'zhuce.html',{'msg':'注册成功'})
                    else:
                        return render(request,'zhuce.html',{'msg':'邮箱不合法'})
                else:
                    return render(request,'zhuce.html',{'msg':'邮箱不合法'})
            else:
                return render(request,'zhuce.html',{'msg':'用户名已存在'})
        else:
            err="两次密码不一致，请重新输入"
            return render(request,'zhuce.html',{'msg':err})      
    return render(request,'zhuce.html')

def denglu(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.POST:
        username=request.POST.get('username')
        print username
        password=request.POST.get('password')
        print password
        try:
            user=models.Fuser.objects.get(username=username)
        except Exception,e:
            return render(request,'login.html',{'login_err':'用户不存在'})
        else:
            if user is not None:
                if password==user.password:
                    if user.is_active:              
                        request.session['myuser']=username
                        return HttpResponseRedirect('/')
                    else:
                        return render(request,'login.html',{'login_err':'用户名未激活，请联系管理员'})
                else:
                    return render(request,'login.html',{'login_err':'用户名或密码错!'})
            

def zhuxiao(request):
    try:
        request.session['myuser']=''
    except KeyError:
        pass
    return HttpResponseRedirect('/')

@check_session
def profile(request):
    user=request.session.get("myuser")
    try:
        user=models.Fuser.objects.get(username=user)
    except Exception,e:
        print e
    return render(request,'profile.html',{'user':user})

@check_session
def setpwd(request):
    if request.method=="POST":
        pass
    return render(request,'setpwd.html')

def search(request):
    cate=models.Category.objects.filter(pid=None)
    print cate
    cart = request.session.get("cart")
    user=request.session.get("myuser")
    cate2=models.Category.objects.all()
    if request.method=='GET':
        search=request.GET.get('search')
        print search
        result=models.Goods.objects.filter(name__icontains=search)
        print result
        return render(request,'search.html',{'result':result,'cate':cate,'cate2':cate2,'cart':cart,'user':user})

def list(request,id):
    cart = request.session.get("cart")
    user=request.session.get("myuser")
    cates=models.Category.objects.filter(pid=None)
    print cates
    cate2=models.Category.objects.all()
    if request.method=='GET':
        print id
        cate=models.Category.objects.get(id=id)
        result=models.Goods.objects.filter(category=cate)
        print result
        return render(request,'list.html',{'result':result,'cate':cates,'cate2':cate2,'cart':cart,'user':user})

def item(request,id):
    cart = request.session.get("cart")
    user=request.session.get("myuser")
    cate=models.Category.objects.filter(pid=None)
    print cate
    cate2=models.Category.objects.all()    
    good=models.Goods.objects.get(id=id)
    comment=models.Comment.objects.filter(goods=good).order_by('-id')
    return render(request,'item.html',{'good':good,'comment':comment,'cate':cate,'cate2':cate2,'cart':cart,'user':user})
    
def addcart(request):
    id=request.GET.get('goodid')
    print id
    try:
        good=models.Goods.objects.get(id=id) 
        print good
        cart = request.session.get("cart")
        cart.add_good(good)
        #cart = Cart(good)
        request.session["cart"] = cart
        print request.session["cart"]
    except Exception,e:
         print e 
    return HttpResponseRedirect('/cart/')
   
  
def cart(request):
    user=request.session.get("myuser")
    cate=models.Category.objects.filter(pid=None)
    print cate
    cate2=models.Category.objects.all()
    if request.GET.get('dc')=='delcart':
        print request.GET.get('dc')
        del request.session['cart']
        data="OK"
        return HttpResponse(data)
    try:
#        cart = request.session.get("cart",None)
#        print 'session cart---',cart
#        t = get_template('cart.html')    
#        if  not cart:

            #cart = Cart()
            #print 'ccar',cart.items
            #srequest.session["cart"] = cart
            cart = request.session.get("cart")
#            c = RequestContext(request,locals())
            print 'c is------>',cart.items
            for i in cart.items:
                print i.good.name,i.count
#            return HttpResponse(t.render(c))   
    except Exception,e:
        print e
    return render(request,'cart.html',{'cart':cart,'cate':cate,'cate2':cate2,'user':user})    

def delgood(request):
    gid=request.GET.get('gid')
    print gid
    good=models.Goods.objects.get(id=gid)
    cart = request.session.get("cart")
    cart.del_good(good)
    request.session["cart"] = cart
    data="OK"
    return HttpResponse(data)

    
def chgcart(request):
    gid=request.GET.getlist('gid')
    print gid
    num=request.GET.getlist('num')
    print num
    for g in gid:
        good=models.Goods.objects.get('id=gid')
        cart = request.session.get("cart")
        cart.chg_good(good,num)
    #cart = Cart(good)
        request.session["cart"] = cart
    return HttpResponseRedirect('/pay/')  


def orderid(request):
    import datetime  
    import random  
    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S");#生成当前时间  
    randomNum=random.randint(0,100)#生成的随机整数n，其中0<=n<=100  
    if randomNum<=10:  
        orderid=str(0)+str(randomNum)  
    orderid=str(nowTime)+str(randomNum)  
    print orderid
    request.session["orderid"] = orderid
    return HttpResponseRedirect('/pay/') 
    
@check_session    
def pay(request):
    user=request.session.get("myuser")
    pays=models.PayMethod.objects.all()
    cart = request.session.get("cart")
    orderid=request.session.get("orderid")
    conn=models.Consignees.objects.all()
    if request.method=="POST":
        uname=request.session.get("myuser")
        print "用户",uname
        name=request.POST.get('name')
        print "收货人",name
        addr=request.POST.get('addr')
        print "地址",addr
        code=request.POST.get('code')
        print "邮编",code
        tel=request.POST.get('tel')
        print "电话",tel
        beizhu=request.POST.get('beizhu')
        print "备注",beizhu
        payid=request.POST.get('pay')
        print "付款id",payid
        pay=models.PayMethod.objects.get(id=payid)
        user=models.Fuser.objects.get(username=uname)
        print "用户对象",user
        try:
            conobj=models.Consignees.objects.get(user=user,name=name,addr=addr,code=code,tel=tel)
        except Exception,e:
            con=models.Consignees(user=user,name=name,addr=addr,code=code,tel=tel)
            con.save()
            conobj=models.Consignees.objects.get(user=user,name=name,addr=addr,tel=tel)
        
        orderstatus=models.OrderStatus.objects.get(status='等待收货')
        buser=models.Buser.objects.get(id=1)
        order=models.Order(order_serial=orderid,user=user,name=conobj,pay=pay,descriptiont=beizhu,status=orderstatus,operator=buser,amount=cart.total_price)
        order.save()
        orderobj=models.Order.objects.get(order_serial=orderid)
        for item in cart.items:
            good=models.Goods.objects.get(id=item.good.id)
            ordergoodnew=models.OrderGoods(good=good,price=item.price,amount=item.count)
            ordergoodnew.save()
            ordergoodnew.order_id.add(orderobj.id)
        del request.session['cart']
        del request.session['orderid']
        return HttpResponseRedirect('/myorder/')    
        
    return render(request,'pay.html',{'cart':cart,'pays':pays,'oid':orderid,'user':user})

@check_session
def myorder(request):
    user=request.session.get("myuser")
    try:
        user=models.Fuser.objects.get(username=user)
    except Exception,e:
        print e    
    orders=models.Order.objects.filter(user=user)
    ordergoods=models.OrderGoods.objects.all()
    return render(request,'myorder.html',{'orders':orders,'ordergoods':ordergoods,'user':user})

@check_session
def ordersearch(request):
    user=request.session.get("myuser")
    userobj=models.Fuser.objects.get(username=user)
    oid=request.GET.get('orderid')
    try:
        result=models.Order.objects.get(order_serial=oid,user=userobj)
        og=models.OrderGoods.objects.filter(order_id=result)
    except Exception,e:
        return HttpResponseRedirect('/myorder/')
    return render(request,'ordersearch.html',{'result':result,'og':og,'user':user})

def orderinfo(request,id):
    user=request.session.get("myuser")
    userobj=models.Fuser.objects.get(username=user)
    try:
        result=models.Order.objects.get(order_serial=id,user=userobj)
        og=models.OrderGoods.objects.filter(order_id=result)
    except Exception,e:
        return HttpResponseRedirect('/myorder/')
    return render(request,'orderinfo.html',{'result':result,'og':og,'user':user})

@check_session
def comment(request,id):
    username=request.session.get("myuser")
    user=models.Fuser.objects.get(username=username)
    good=models.Goods.objects.get(id=id)
    if request.method=="POST":
        comm=request.POST.get('comment')
        print comm
        cobj=models.Comment(comment=comm,user=user,goods=good)
        cobj.save()
        url="/item/%s/"%(id)
        return HttpResponseRedirect(url)
        
    return render(request,'comment.html',{'good':good,'user':user})


def check_session_hou(func):
    def wrapper(request,*args, **kv):
        userinfo=request.session.get('buser',None) 
        print userinfo
        if not userinfo:
            return HttpResponseRedirect('/houtai/')
        return func(request,*args, **kv)
    return wrapper


def houtai(request):
    if request.method=="GET":
        return render(request,'admin.html')
    if request.POST:
        username=request.POST.get('username')
        print username
        password=request.POST.get('password')
        print password
        try:
            user=models.Buser.objects.get(username=username)
        except Exception,e:
            return render(request,'admin.html',{'login_err':'用户不存在'})
        else:
            if user is not None:
                if password==user.password:
                    if user.is_active:              
                        request.session['buser']=username
                        return HttpResponseRedirect('/manage/')
                    else:
                        return render(request,'admin.html',{'login_err':'用户名未激活，请联系管理员'})
                else:
                    return render(request,'admin.html',{'login_err':'用户名或密码错!'})
            

def tuichu(request):
    try:
        request.session['buser']=''
    except KeyError:
        pass
    return HttpResponseRedirect('/houtai/')
@check_session_hou
def manage(request):
    return render(request,'manage.html')

@check_session_hou
def buser(request):
    buser=models.Buser.objects.all().order_by('-id')
    return render(request,'buser.html',{'buser':buser})

@check_session_hou
def buseradd(request):
    pers=models.Permission.objects.all()
    if request.method=="POST":
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        name=request.POST.get('name')
        key=request.POST.get('key')
        per=request.POST.getlist('per')
        try:
            uobj=models.Buser.objects.get(username=username)
            print uobj
        except Exception,e:
            userobj=models.Buser(username=username,password=pwd,name=name,is_active=key)
            userobj.save()
            for p in per:
                pp=models.Permission.objects.get(id=p)
                userobj.permisson.add(pp)
            return HttpResponseRedirect('/buser/')
        else:
            return render(request,'buseradd.html',{'msg':'用户已存在'})
            
    return render(request,'buseradd.html',{'pers':pers})

@check_session_hou
def chgpwd(request):
    return render(request,'chgpwd.html')

@check_session_hou
def cate(request):
    cate=models.Category.objects.all()
    pcate=models.Category.objects.filter(pid=None)
    if request.method=="POST":
        name=request.POST.get('name')
        print name
        cateid=request.POST.get('cate')
        print cateid
        try:
            cate=models.Category.objects.get(id=cateid)
            print cate
            if not models.Category.objects.filter(name=name):
                catenew=models.Category(name=name,pid=cate)
                catenew.save()
        except Exception,e:
                catenew=models.Category(name=name)
                catenew.save()
            
        return HttpResponseRedirect('/cate/')
        
    return render(request,'cate.html',{'cate':cate,'pcate':pcate})

@check_session_hou
def goodlist(request):
    cate=models.Category.objects.exclude(pid=None)
    goods=models.Goods.objects.all()
    if request.method=="POST":
        cateid=request.POST.get('cate')
        print cateid
        name=request.POST.get('name')
        print name        
        price=request.POST.get('price')
        print price 
        sprice=request.POST.get('sprice')
        print sprice 
        amount=request.POST.get('amount')
        print amount 
        pic=request.POST.get('pic')
        print pic 
        status=request.POST.get('status')
        print status 
        paddr=request.POST.get('paddr')
        print paddr 
        desc=request.POST.get('desc')
        print desc 
        cateobj=models.Category.objects.get(id=cateid)       
        if not models.Goods.objects.filter(name=name):
            goodnew=models.Goods(name=name,category=cateobj,price=price,sale_price=sprice,amount=amount,pic=pic,status=status,paddr=paddr,descriptiont=desc)
            goodnew.save()
        return HttpResponseRedirect('/goodlist/')    
    return render(request,'goodlist.html',{'goods':goods,'cate':cate})

@check_session_hou
def good(request):
    goodid=request.GET.get('gid')
    
    return render(request,'goods.html')

@check_session_hou
def orderlist(request):
    orderlist=models.Order.objects.all().order_by('-id')
    status=models.OrderStatus.objects.all()
    return render(request,'orderlist.html',{'orderlist':orderlist,'status':status})

@check_session_hou
def ordermodify(request):
    return render(request,'ordermodify.html')

@check_session_hou
def fuser(request):
    fuser=models.Fuser.objects.all()
    return render(request,'fuser.html',{'fuser':fuser})
