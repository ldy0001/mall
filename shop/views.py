#_*_coding:utf-8_*_
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
import models
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
        
    def add_good(self,good):
        self.total_price += good.sale_price
        print self.total_price
        for item in self.items:
            if item.good.id == good.id:
                item.count += 1
                return
        self.items.append(models.CartItem(good=good,price=good.sale_price,count=1))

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
                if not userobj:
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
            except Exception:
                userobj=models.Fuser(username=username,password=password,is_active=True)
                userobj.save()
                return render(request,'zhuce.html',{'msg':'注册成功'})
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
        user=models.Fuser.objects.get(username=username)
        if user is not None:
            if password==user.password:
                if user.is_active:              
                    request.session['myuser']=username
                    return HttpResponseRedirect('/')
                else:
                    return render(request,'login.html',{'login_err':'用户名未激活，请联系管理员'})
            else:
                return render(request,'login.html',{'login_err':'用户名或密码错!'})
        else:
            return render(request,'login.html',{'login_err':'用户不存在'})

def zhuxiao(request):
    try:
        request.session['myuser']=''
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def profile(request):
    return render(request,'profile.html')

def setpwd(request):
    return render(request,'setpwd.html')

def search(request):
    if request.method=='GET':
        search=request.GET.get('search')
        print search
        result=models.Goods.objects.filter(name__icontains=search)
        print result
        return render(request,'search.html',{'result':result})

def list(request,id):
    if request.method=='GET':
        print id
        cate=models.Category.objects.get(id=id)
        result=models.Goods.objects.filter(category=cate)
        print result
        return render(request,'list.html',{'result':result})

def item(request,id):
    
    return render(request,'item.html')
    
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
    if request.GET.get('delcart')=='del':
        del request.session['cart']
        return HttpResponseRedirect('/cart/')
    return render(request,'cart.html',{'cart':cart})    
    

def pay(request):
    pays=models.PayMethod.objects.all()
    cart = request.session.get("cart")
    return render(request,'pay.html',{'cart':cart,'pays':pays})

def myorder(request):
    return render(request,'myorder.html')

def ordersearch(request):
    return render(request,'ordersearch.html')

def orderinfo(request):
    return render(request,'orderinfo.html')

def comment(request):
    return render(request,'comment.html')

def houtai(request):
    return render(request,'admin.html')

def manage(request):
    return render(request,'manage.html')

def buser(request):
    return render(request,'buser.html')

def buseradd(request):
    return render(request,'buseradd.html')

def chgpwd(request):
    return render(request,'chgpwd.html')

def cate(request):
    return render(request,'cate.html')

def goods(request):
    return render(request,'goods.html')

def ordermodify(request):
    return render(request,'ordermodify.html')

def fuser(request):
    return render(request,'fuser.html')
