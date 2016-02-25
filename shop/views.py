from django.shortcuts import render,render_to_response
from django.template import RequestContext
from shop import models
from shop.models import Category
# Create your views here.
def index(request):
    cate=models.Category.objects.filter(pid=None)
    print cate
    cate2=models.Category.objects.all()
    goods=models.Goods.objects.all()
    return render_to_response('index.html',{'cate':cate,'goods':goods,'cate2':cate2},context_instance=RequestContext(request))

def zhuce(request):
    return render(request,'zhuce.html')

def denglu(request):
    return render(request,'login.html')

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

def cart(request):
    return render(request,'cart.html')

def pay(request):
    return render(request,'pay.html')

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
