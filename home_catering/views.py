from django.shortcuts import render, redirect
from django.http import HttpResponse
from signup.models import SignupCateringService, SignupMahalService, SignupCateringBoy, SignupCustomer
from home_catboy.models import CBorders
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from .models import  *
import uuid, json
from datetime import time, datetime
from django.template.defaulttags import register
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache

@register.filter
def string(value):
    return str(value)

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_pos(value):
    return int( value.split('.')[0][-1])+1

@register.filter
def set_value(value):
    return 0

@register.filter
def incre(value):
    return value+str(1)

@register.filter
def test_range(value):
    return value<=5

@register.filter
def list_to_string(val):
    return  ', '.join(val)

def gallery(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupCateringService.objects.get(pk=id))
            if CateringGallery.objects.filter(id=id).exists():
                dic['gallery']=dict(CateringGallery.objects.get(id=id))
            return render(request, 'home_catering/gallery.html', dic)
        else:
             return redirect('login')
    except:
        return redirect('logout',service=id)

def addgallery(request, id):
    if request.method=="POST":
        try:
            img = request.FILES['imgs']
        
            user_name=SignupCateringService.objects.get(id =id).name
            fs = FileSystemStorage(location='media/gallery/catering/'+user_name)
            ext = img.name.split('.')[-1]

            if not(CateringGallery.objects.filter(pk=id).exists()):
                fs.save(user_name+str(0)+'.'+ext, img)
                pic_insert= '/media/gallery/catering/'+user_name+'/'+user_name+str(0)+'.'+ext
                CateringGallery.objects.create(id=id, gallery_pic=[pic_insert])
            else:
                obj=CateringGallery.objects.get(pk=id)
                len_obj=len(obj.gallery_pic)
                pos_value=[]
                for x in obj.gallery_pic:
                    pos_value.append(int(x.split('.')[0][-1]))

                if len_obj<6:
                    for x in range(len_obj+1):
                        if x not in pos_value:
                            fs.save(user_name+str(x)+'.'+ext, img)
                            pic_insert= '/media/gallery/catering/'+user_name+'/'+user_name+str(x)+'.'+ext
                            break
                    
                    CateringGallery.objects(id=id).update(gallery_pic__append=[pic_insert])
                    
            return redirect('cateringgallery', id=id)
        except:
            return redirect('cateringgallery', id=id)
    else:
        return redirect('cateringgallery', id=id)

def delete(request, id, pos):
    user=SignupCateringService.objects.get(id =id)
    fs = FileSystemStorage(location='media/gallery/catering/'+user.name)
    gallery= CateringGallery.objects.get(id =id)
    pic_img=gallery.gallery_pic
    z=0
    for x in pic_img:
        if pos == int(x.split('.')[0][-1]):
            del_name=x.split('/')[-1]
            pic_img.pop(z)
            break
        z+=1
    gallery.update(gallery_pic=pic_img)
    fs.delete(del_name)
    return redirect('cateringgallery', id=id)

def home(request, id):  
    try:
        if request.session[str(id)]:

            dic=dict(SignupCateringService.objects.get(pk= id))

            dic['names']=json.dumps([x.name for x in SignupCateringBoy.objects.all()])
            dic['home']='home'
            dic['current_catering']=[]
            hist_obj= CateringBoyOrder.objects.filter(cid=id)
            if hist_obj.exists():
                for obj in hist_obj:
                    details=dict(obj)                    
                    ss=str(details['timing']).split(":")
                    details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                    if details['catboy_max']<1:
                        details['count_empty']=1
                    dic['current_catering'].append(details)
                dic['current_catering'].sort(key=lambda xx:xx['date'])
            dic['list_catboy']=list(SignupCateringBoy.objects.all().limit(2))

            dic['current_request']=[]
            for x in CateringServiceOrder.objects.filter(receiver_id=id):
                dic['current_request'].append(x)

            dic['current_request'].sort(key=lambda xx:xx['date'])
            return render(request, 'home_catering/home.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def order(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupCateringService.objects.get(id=id))  
            request.session['catering']=1
            return render(request, 'home_catering/order.html', a)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def createOrder(request, id):
    if request.method=='POST':
        add= request.POST['add']
        city= request.POST['city']
        pincode= request.POST['pincode']
        catboy= request.POST['nocatboy']
        amount= request.POST['amount']
        date= request.POST['date']
        time= request.POST['time']
        mobile=str(request.POST['mobile'])
        phone =str(request.POST['phone'])
        orderid= uuid.uuid4()
        
        CateringBoyOrder.objects.create(id= orderid,cid=id,amount=amount,date=date, timing=time, catboy_max=catboy,
             venue={'address':add+','+city+','+pincode,'mobile':mobile, 'phone':phone, 'location':city},count=catboy,
            )
        return redirect('homecatering', id=id)
    else:
        return redirect('cateringorder', id=id)

def dictProdSum(dic):
    sum_ = 0 
    for list_ in dic:
        prod=1
        for val in list_:
            prod*=val
        sum_+=prod
    return sum_

def foodList(request, id):
    try:
        if request.session[str(id)]:
            dic ={"id":id}
            if CateringBreakfast.objects.filter(pk=id).exists():
                dic['mrng_veg']= CateringBreakfast.objects.get(pk=id).foods
                
                dic['mrng_veg_total']=dictProdSum(dic['mrng_veg'].values())

            if CateringLunchVeg.objects.filter(pk=id).exists():
                dic['lunch_veg']= CateringLunchVeg.objects.get(pk=id).foods
                
                dic['lunch_veg_total']=dictProdSum(dic['lunch_veg'].values())
            
            if CateringLunchNonveg.objects.filter(pk=id).exists():
                dic['lunch_non']= CateringLunchNonveg.objects.get(pk=id).foods
                
                dic['lunch_non_total']=dictProdSum(dic['lunch_non'].values())
            
            if CateringDinnerVeg.objects.filter(pk=id).exists():
                dic['dinner_veg']= CateringDinnerVeg.objects.get(pk=id).foods
                
                dic['dinner_veg_total']=dictProdSum(dic['dinner_veg'].values())
            
            if CateringDinnerNonveg.objects.filter(pk=id).exists():
                dic['dinner_non']= CateringDinnerNonveg.objects.get(pk=id).foods
                
                dic['dinner_non_total']=dictProdSum(dic['dinner_non'].values())

            return render(request, 'home_catering/foodlist.html', dic)

        else:
            return redirect('login')
    except:
        return redirect('logout', service=id)

def addBreakfast(request, id):
    foodname =request.POST['foodname']
    foodprice = request.POST['foodprice']
    foodcount= request.POST['foodcount']

    if not(CateringBreakfast.objects.filter(pk=id).exists()):
        CateringBreakfast.objects.create(id = id, foods={ foodname: [foodprice,foodcount]})
    
    else:
        CateringBreakfast.objects(pk=id).update(foods__add={foodname: [foodprice,foodcount] })
    
    return redirect('createfoodlist', id=id)

def addLunchVeg(request, id):
    foodname =request.POST['foodname']
    foodprice = request.POST['foodprice']
    foodcount= request.POST['foodcount']

    if not(CateringLunchVeg.objects.filter(pk=id).exists()):
        CateringLunchVeg.objects.create(id = id, foods={foodname: [foodprice,foodcount]})
    
    else:
        CateringLunchVeg.objects(pk=id).update(foods__add={foodname: [foodprice,foodcount]})
    
    return redirect('createfoodlist', id=id)

def addLunchNonVeg(request, id):
    foodname =request.POST['foodname']
    foodprice = request.POST['foodprice']
    foodcount= request.POST['foodcount']

    if not(CateringLunchNonveg.objects.filter(pk=id).exists()):
        CateringLunchNonveg.objects.create(id = id, foods={foodname: [foodprice,foodcount]})
    
    else:
        CateringLunchNonveg.objects(pk=id).update(foods__add={foodname: [foodprice,foodcount]})
    
    return redirect('createfoodlist', id=id)

def addDinnerVeg(request, id):
    foodname =request.POST['foodname']
    foodprice = request.POST['foodprice']
    foodcount= request.POST['foodcount']

    if not(CateringDinnerVeg.objects.filter(pk=id).exists()):
        CateringDinnerVeg.objects.create(id = id, foods={foodname: [foodprice,foodcount]})
    
    else:
        CateringDinnerVeg.objects(pk=id).update(foods__add={foodname: [foodprice,foodcount]})
    
    return redirect('createfoodlist', id=id)

def addDinnerNonVeg(request, id):
    foodname =request.POST['foodname']
    foodprice = request.POST['foodprice']
    foodcount= request.POST['foodcount']

    if not(CateringDinnerNonveg.objects.filter(pk=id).exists()):
        CateringDinnerNonveg.objects.create(id = id, foods={foodname: [foodprice,foodcount]})
    
    else:
        CateringDinnerNonveg.objects(pk=id).update(foods__add={foodname: [foodprice,foodcount]})
    
    return redirect('createfoodlist', id=id)

def deleteBreakfast(request, id, value):
    CateringBreakfast.objects(pk=id).update(foods__remove={value})
    return redirect('createfoodlist', id=id)

def deleteLunchVeg(request, id, value):
    CateringLunchVeg.objects(pk=id).update(foods__remove={value})
    return redirect('createfoodlist', id=id)

def deleteLunchNonVeg(request, id, value):
    CateringLunchNonveg.objects(pk=id).update(foods__remove={value})
    return redirect('createfoodlist', id=id)

def deleteDinnerVeg(request, id, value):
    CateringDinnerVeg.objects(pk=id).update(foods__remove={value})
    return redirect('createfoodlist', id=id)

def deleteDinnerNonVeg(request, id, value):
    CateringDinnerNonveg.objects(pk=id).update(foods__remove={value})
    return redirect('createfoodlist', id=id)

def viewOrder(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupCateringService.objects.get(pk=id))
            dic['current_catering']=[]
            hist_obj= CateringBoyOrder.objects.filter(cid=id)
            if hist_obj.exists():
                for obj in hist_obj:
                    details=dict(obj)                    
                    ss=str(details['timing']).split(":")
                    details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                    if details['catboy_max']<1:
                        details['count_empty']=1
                    dic['current_catering'].append(details)
                dic['current_catering'].sort(key=lambda xx:xx['date'])

            dic['service_book']=[]
            for x in CateringServiceOrder.objects.filter(receiver_id=id):
                dic['service_book'].append(x)

            dic['service_book'].sort(key=lambda xx:xx['date'])

            return render(request, 'home_catering/vieworders.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def viewServiceOrder(request, id, cid, type, date):
    try:
        if request.session[str(id)]:
            objects= CateringServiceOrder.objects.get(receiver_id=id ,booker_id =cid,  reg_type=type, date=date)
            dic = {'id': id}
            dic['obj']=dict(objects)
            if SignupMahalService.objects.filter(pk=objects.booker_id).exists():
                dic['rev']=dict(SignupMahalService.objects.get(pk=objects.booker_id))
                
            elif SignupCustomer.objects.filter(pk=objects.booker_id).exists():
                dic['rev']=dict(SignupCustomer.objects.get(pk=objects.booker_id))

            dic['per']=dic['obj']['amount']//dic['obj']['plates']
            return render(request, 'home_catering/viewrequest.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def acceptRequest(request, id, cid, type, date):
    objects= CateringServiceOrder.objects.get(receiver_id=id ,booker_id =cid,  reg_type=type, date=date)
    objects.update(status="accept")
    return redirect('viewcateringrequest', id=id, cid=cid, type=type, date=date)

def cancelRequest(request, id, cid, type, date):
    objects= CateringServiceOrder.objects.get(receiver_id=id ,booker_id =cid,  reg_type=type, date=date)
    objects.update(status="cancel")
    return redirect('viewcateringrequest', id=id, cid=cid, type=type, date=date)

def viewCatboyrequest(request, id, oid):
    try:
        if request.session[str(id)]:
            hist_obj= CBorders.objects.filter(oid=oid)
            dic={}
            dic['list_pending']=[]
            dic['list_accept']=[]
            dic['empty']=0
            if hist_obj.exists():
                dic['empty']=1
                for obj in hist_obj:
                    if obj.status=='pending':
                        x=dict(SignupCateringBoy.objects.get(pk=obj.cbid))
                        x['date']=obj.date
                        dic['list_pending'].append(x)
                    else:
                        x=dict(SignupCateringBoy.objects.get(pk=obj.cbid))
                        x['date']=obj.date
                        x['status']=obj.status
                        dic['list_accept'].append(x)
            
            dic['id']=id
            dic['oid']=oid
            return render(request,'home_catering/viewcatboyrequest.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)
    
def acceptCatboyrequest(request, id, cid, oid, date):
    obj_status=CBorders.objects.get(cbid=cid, oid=oid, date=date)
    obj_cbcount= CateringBoyOrder.objects.get(pk=oid)
    
    obj_status.update(status='accept')
    obj_cbcount.update(catboy_max= obj_cbcount.catboy_max -1)
    if obj_cbcount.catboy_max==1:
        CBorders.objects.filter(oid=oid, status='pending').delete()

    return redirect('viewcatboyrequestbycatering', id=id,oid = oid)

def completeCatboyrequest(request, id, cid, oid, date):
    obj_status=CBorders.objects.get(cbid=cid, oid=oid, date=date)
    
    obj_status.update(status='complete')
    return redirect('viewcatboyrequestbycatering', id=id,oid = oid)

def history(request, id):
    try:
        if request.session[str(id)]:
            hist_catboy= CateringBoyOrder.objects.filter(cid=id)
            dic={'id':id}
            dic['catboy_order']=[]
            
            for hist in hist_catboy:
                details=dict(hist)                    
                ss=str(details['timing']).split(":")
                details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                dic['catboy_order'].append(details)

            hist_request= CateringServiceOrder.objects.filter(receiver_id=id) 
            dic['request']=[] 
            for hist in hist_request:
                if hist.status=="complete":
                    dic['request'].append(hist)
            return render(request,'home_catering/history.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)
    
def earnings(request, id):
    try:
        if request.session[str(id)]:
            dic={'id':id}

            hist_request= CateringServiceOrder.objects.filter(receiver_id=id) 
            total=0
            dic['request']=[] 
            for hist in hist_request:
                if hist.status=="complete":
                    total+=hist.amount
                    dic['request'].append(hist)
            dic['total']=total
            return render(request,'home_catering/earning.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def searchCatboy(search):
    search_list=[]                
    list_value=SignupCateringBoy.objects.all()
    for value in list_value:
        if search.lower() in value.name.lower():
            search_list.append(dict(value))
    return search_list

def searchCatboyList(request,id):
    try:
        if request.session[str(id)]:
            search_list={}
            try:
                search=request.POST['q']
                request.session[str(id)]={'search':search}
            except:
                search=request.session[str(id)]['search']

            
            pag= request.GET.get('page_catering',1)

            pagnator=Paginator(searchCatboy(search),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catering']=des
            
            search_list['id']=id
            search_list['search']=search
            return render(request, 'home_catering/viewcatboy.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def viewCatboyList(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
        
            
            pag= request.GET.get('page_catering',1)

            pagnator=Paginator(SignupCateringBoy.objects.all(),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catering']= des
            search_list['search']=''
            search_list['id']=id
            return render(request, 'home_catering/viewcatboy.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

