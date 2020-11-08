from django.shortcuts import render, redirect
from signup.models import *
from home_catering.models import *
from home_catboy.models import CBorders
from .models import CustomerBookingTemp
from home_mahal.models import *
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
import random, uuid

from datetime import time, datetime

def home(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupCustomer.objects.get(id=id)) 
            dic['catering']=[]
            for value in SignupCateringService.objects.all().limit(2):
                d=dict(value)
                d['gallery_pic']=''
                if CateringGallery.objects.filter(pk=value.id).exists():
                    gallery = random.choice(CateringGallery.objects.get(pk=value.id).gallery_pic)
                    d['gallery_pic']=gallery
                dic['catering'].append(d)

            dic['mahal']=[]

            for value in SignupMahalService.objects.all()[:2]:
                d=dict(value)
                d['gallery_pic']=''
                if MahalGallery.objects.filter(pk=value.id).exists():
                    gallery = random.choice(MahalGallery.objects.get(pk=value.id).gallery_pic)
                    d['gallery_pic']=gallery
                dic['mahal'].append(d)
            
            dic['catboy']=list(SignupCateringBoy.objects.all()[:2])
            return render(request, 'home_customer/home.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('login')
    
def searchMahal(search):
    search_list=[]                
    list_value=SignupMahalService.objects.all()
    for value in list_value:
        if search.lower() in value.name.lower():
            d=dict(value)
            d['gallery_pic']=''
            if MahalGallery.objects.filter(pk=value.id).exists():
                gallery = random.choice(MahalGallery.objects.get(pk=value.id).gallery_pic)
                d['gallery_pic']=gallery
            search_list.append(d)
    return search_list

def searchCatering(search):
    search_list=[]                
    list_value=SignupCateringService.objects.all()
    for value in list_value:
        if search.lower() in value.name.lower():
            d=dict(value)
            d['gallery_pic']=''
            if CateringGallery.objects.filter(pk=value.id).exists():
                gallery = random.choice(CateringGallery.objects.get(pk=value.id).gallery_pic)
                d['gallery_pic']=gallery
            search_list.append(d)
    return search_list

def searchCatboy(search):
    search_list=[]                
    list_value=SignupCateringBoy.objects.all()
    for value in list_value:
        if search.lower() in value.name.lower():
            search_list.append(dict(value))
    return search_list

def search(request, id):
    try:
        if request.session[str(id)]:
            if request.method=="POST" or len(request.session['customersearch']):
                try:
                    search=request.POST['q']
                    request.session['customersearch']=search
                except:
                    search=request.session['catboysearch']
                

                search_list={'catering':'', 'catboy':'', 'mahal':''}
                search_list['search']=search
            
                search_list['catboy']=searchCatboy(search)[:20]
                search_list['catering']=searchCatering(search)[:20]
                search_list['mahal']=searchMahal(search)[:20]
               

                search_list['id']=id
                return render(request,'home_customer/search.html', search_list)
            else:
                return redirect('homecustomer', id)

        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def searchListCatboy(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            try:
                search=request.POST['q']
                request.session['viewcatboysearch']=search
            except:
                search= request.session['viewcatboysearch']
            
            pag= request.GET.get('page_catboy',1)

            pagnator=Paginator(searchCatboy(search),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catboy']=des
            search_list['id']=id
            search_list['search']=search
            return render(request, 'home_customer/viewcatboy.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def searchListMahal(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            try:
                search=request.POST['q']
                request.session['viewmahalsearch']=search
            except:
                search= request.session['viewmahalsearch']
            
            pag= request.GET.get('page_mahal',1)

            pagnator=Paginator(searchMahal(search),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['mahal']=des
            search_list['id']=id
            search_list['search']=search
            return render(request, 'home_customer/viewmahal.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id) 

def searchListCatering(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            try:
                search=request.POST['q']
                request.session['viewcateringsearch']=search
            except:
                search= request.session['viewcateringsearch']
            
            pag= request.GET.get('page_cat',1)

            pagnator=Paginator(searchCatering(search),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catering']=des
            search_list['id']=id
            search_list['search']=search

            return render(request, 'home_customer/viewcatering.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id) 

def viewCatering(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            pag= request.GET.get('page_cat',1)
            pagnator=Paginator(searchCatering(''),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catering']=des
            search_list['id']=id
            return render(request, 'home_customer/viewcatering.html', search_list)
        
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def viewCatboy(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            pag= request.GET.get('page_catboy',1)
            pagnator=Paginator(searchCatboy(''),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catboy']=des
            search_list['id']=id
            return render(request, 'home_customer/viewcatboy.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def viewMahal(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            pag= request.GET.get('page_mahal',1)
            pagnator=Paginator(searchMahal(''),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['mahal']=des
            search_list['id']=id
            return render(request, 'home_customer/viewmahal.html', search_list)
        
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def dictProdSum(dic):
    sum_ = 0 
    for list_ in dic:
        prod=1
        for val in list_:
            prod*=val
        sum_+=prod
    return sum_

def bookCatering(request, id, cid):
    try:
        if request.session[str(id)]:
            dic ={"id":id, 'cid':cid}
            dic['address']=SignupCateringService.objects.get(pk=cid).address
            if CateringBreakfast.objects.filter(pk=cid).exists():
                dic['mrng_veg']= CateringBreakfast.objects.get(pk=cid).foods
                
                dic['mrng_veg_total']=dictProdSum(dic['mrng_veg'].values())

            if CateringLunchVeg.objects.filter(pk=cid).exists():
                dic['lunch_veg']= CateringLunchVeg.objects.get(pk=cid).foods
                
                dic['lunch_veg_total']=dictProdSum(dic['lunch_veg'].values())
            
            if CateringLunchNonveg.objects.filter(pk=cid).exists():
                dic['lunch_non']= CateringLunchNonveg.objects.get(pk=cid).foods
                
                dic['lunch_non_total']=dictProdSum(dic['lunch_non'].values())
            
            if CateringDinnerVeg.objects.filter(pk=cid).exists():
                dic['dinner_veg']= CateringDinnerVeg.objects.get(pk=cid).foods
                
                dic['dinner_veg_total']=dictProdSum(dic['dinner_veg'].values())
            
            if CateringDinnerNonveg.objects.filter(pk=cid).exists():
                dic['dinner_non']= CateringDinnerNonveg.objects.get(pk=cid).foods
                
                dic['dinner_non_total']=dictProdSum(dic['dinner_non'].values())

            temp_list_dinner=[]
            temp_list_lunch=[]
            temp_list_mrng=[]
            disable_list={
                'dinner':[],
                'lunch':[],
                'mrng':[]
            }
            dic['mrng_add_total'],dic['lunch_add_total'],dic['dinner_add_total']=0,0,0
            for obj in  CustomerBookingTemp.objects.filter(pk=id):
                if obj.reg_type=="dinner":
                    temp_list_dinner.append(dict(obj))
                    dic['dinner_add_total']+=obj.amount[0] * obj.amount[1]
                    disable_list['dinner'].append(obj.foodname)

                elif obj.reg_type=="lunch":
                    temp_list_lunch.append(dict(obj))
                    dic['lunch_add_total']+=obj.amount[0] * obj.amount[1]
                    disable_list['lunch'].append(obj.foodname)
                
                else:
                    temp_list_mrng.append(dict(obj))
                    dic['mrng_add_total']+=obj.amount[0] * obj.amount[1]
                    disable_list['mrng'].append(obj.foodname)
            
            dic['dinner_add']=temp_list_dinner
            dic['lunch_add']=temp_list_lunch
            dic['mrng_add']=temp_list_mrng
            dic['disabled']=disable_list

            return render(request, 'home_customer/bookcatering.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service= id)

def deleteTemp(request, id, cid):
    CustomerBookingTemp.objects(id=id, cid=cid).delete()
    return redirect('viewcateringuserbycustomer',id= id,cid=cid)

def addToCart(request, id, cid, type, name, rate, count,veg):
    CustomerBookingTemp.objects.create(id=id, cid=cid, reg_type=type, foodname=name, amount=[rate, count],veg_non=veg)
    return redirect('bookcateringbycustomer',id= id,cid=cid)

def deleteToCart(request, id, cid, type, name):
    CustomerBookingTemp.objects(id=id, cid=cid, reg_type=type, foodname=name).delete()
    return redirect('bookcateringbycustomer',id= id,cid=cid)

def bookOrder(request, id, cid):
    try:
        if request.session[str(id)]:
            dinner={'veg':[], 'non_veg':[]}
            lunch={'veg':[], 'non_veg':[]}
            mrng=[]
            dinner_amt, lunch_amt, mrng_amt=0, 0, 0
            temp_data=CustomerBookingTemp.objects(id=id, cid=cid)
            for list_book in temp_data:
                if list_book.reg_type=="dinner":
                    dinner_amt += list_book.amount[0] * list_book.amount[1]
                    if list_book.veg_non=='veg':
                        dinner['veg'].append(list_book.foodname)
                    else:
                        dinner['non_veg'].append(list_book.foodname)
                
                elif list_book.reg_type=="lunch":
                    lunch_amt += list_book.amount[0] * list_book.amount[1]
                    if list_book.veg_non=='veg':
                        lunch['veg'].append(list_book.foodname)
                    else:
                        lunch['non_veg'].append(list_book.foodname)
                else:
                    mrng_amt += list_book.amount[0] * list_book.amount[1]
                    mrng.append(list_book.foodname)

            address= request.POST['add'] 
            date= request.POST['date']   
            if dinner["veg"]!=[] or dinner['non_veg']!= []:
                plates=int( request.POST['dinnerInput'])
                
                amount=plates*dinner_amt
                CateringServiceOrder.objects.create(
                    receiver_id=cid, booker_id=id,  reg_type='dinner', amount=amount,  foodlist= dinner, plates=plates, status="pending", address=address,
                    date=date
                )
            
            if lunch["veg"]!=[] or lunch['non_veg']!=[]:
                plates= int(request.POST['lunchInput'])
                amount=plates*lunch_amt

                CateringServiceOrder.objects.create(
                    receiver_id=cid, booker_id=id,  reg_type='lunch', amount=amount,  foodlist=lunch, plates=plates, status="pending", address=address,
                    date=date
                )

            if mrng!=[]:
                plates= int(request.POST['mrngInput'])
                amount=plates*mrng_amt

                CateringServiceOrder.objects.create(
                    receiver_id=cid, booker_id=id,  reg_type='mrng', amount=amount,  foodlist=lunch, plates=plates, status="pending", address=address,
                    date=date
                )
            
            temp_data.delete()
            return redirect('viewcateringuserbycustomer', id=id, cid=cid)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def viewCateringUser(request, id, cid):
    try:
        if request.session[str(id)]:
            dic={'id':id}
            dic['object']=dict(SignupCateringService.objects.get(pk =cid))
            if CateringGallery.objects.filter(pk=cid).exists():
                dic['catering_gallery']=list(CateringGallery.objects.get(pk=cid).gallery_pic)
            
            dic['mrng_veg_total'] ,dic['dinner_non_total'], dic['dinner_veg_total'], dic['lunch_veg_total'], dic['lunch_non_total']=0, 0, 0, 0, 0
            
            if CateringBreakfast.objects.filter(pk=cid).exists():
                val= CateringBreakfast.objects.get(pk=cid).foods
                
                dic['mrng_veg_total']=dictProdSum(val.values())

            if CateringLunchVeg.objects.filter(pk=cid).exists():
                val= CateringLunchVeg.objects.get(pk=cid).foods
                
                dic['lunch_veg_total']=dictProdSum(val.values())

            if CateringLunchNonveg.objects.filter(pk=cid).exists():
                val= CateringLunchNonveg.objects.get(pk=cid).foods
                
                dic['lunch_non_total']=dictProdSum(val.values())

            if CateringDinnerVeg.objects.filter(pk=cid).exists():
                val= CateringDinnerVeg.objects.get(pk=cid).foods
                
                dic['dinner_veg_total']=dictProdSum(val.values())

            if CateringDinnerNonveg.objects.filter(pk=cid).exists():
                val= CateringDinnerNonveg.objects.get(pk=cid).foods
                
                dic['dinner_non_total']=dictProdSum(val.values())
            
            dic['pass']=0

            if dic['mrng_veg_total'] or dic['dinner_non_total'] or dic['dinner_veg_total']  or  dic['lunch_veg_total'] or dic['lunch_non_total']:
                dic['pass'] =1
            
            return render(request, 'home_customer/viewcateringuser.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service= id)

def viewMahalUser(request, id, cid):
    try:
        if request.session[str(id)]:
            dic={'id':id}
            dic['object']=dict(SignupMahalService.objects.get(pk =cid))
            if MahalGallery.objects.filter(pk=cid).exists():
                dic['mahal_gallery']=list(MahalGallery.objects.get(pk=cid).gallery_pic)

            return render(request, 'home_customer/viewmahaluser.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def bookMahal(request, id, cid):    
    try:
        if request.session[str(id)]:
            msg=''
            rent_empty=0
            amt=SignupMahalService.objects.get(pk=cid).rent_amount
            user=SignupCustomer.objects.get(pk=id).name
            print(amt)
            if amt != None:
                if request.method=="POST":
                    from_date=request.POST['from']
                    to_date = request.POST['to']
                    rent = int(request.POST['rent'])
                    datef= datetime.strptime(from_date, '%Y-%m-%d').date()
                    datet= datetime.strptime(to_date, '%Y-%m-%d').date()
                    for x in MahalCalendar.objects.filter(pk=cid):
                        if x.from_date.date() <= datef <=x.to_date.date():
                            msg="Date "+str(datef)+" is Not Availble"
                            break
                        elif x.from_date.date() <= datet <=x.to_date.date():
                            msg=" Date "+str(datet) +" is Not Availble"
                            break
                    
                    if msg=='':
                        MahalCalendar.objects.create(
                            id=cid, cid=id, from_date=from_date, to_date=to_date, amount=rent*amt, rent_hr=rent, booker_name=user
                            )
                        return redirect('viewmahalbycustomer', id, cid)
            else:
                rent_empty=1
            print(rent_empty)
            dic={'id':id, 'cid':cid, 'msg':msg, 'book_btn':rent_empty}
            dic['amt']=amt
            return render(request, 'home_customer/bookmahal.html', dic)
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
        mobile=str(request.POST['phone'])
        phone =''
        orderid= uuid.uuid4()
        
        CateringBoyOrder.objects.create(id= orderid,cid=id,amount=amount,date=date, timing=time, catboy_max=catboy,
             venue={'address':add+','+city+','+pincode,'mobile':mobile, 'phone':phone, 'location':city},count=catboy,
            )
        return redirect('homecustomer', id=id)
    else:
        dic=dict(SignupCustomer.objects.get(pk=id))

        return render(request, 'home_customer/bookcatboy.html',dic)

def viewCatboyUser(request, id, cid):
    try:
        if request.session[str(id)]:
            dic={'id':id}
            dic['object']=dict(SignupCateringBoy.objects.get(pk =cid))
            return render(request, 'home_mahal/viewcatboyuser.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service= id)

def viewOrder(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupCustomer.objects.get(pk=id))
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
            for x in CateringServiceOrder.objects.filter(booker_id=id):
                dic['service_book'].append(x)

            dic['service_book'].sort(key=lambda xx:xx['date'])
            dic['calendar'] = list(MahalCalendar.objects.filter(cid=id, from_date__gte=datetime.date(datetime.now())))
            
            return render(request, 'home_customer/vieworders.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

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
            return render(request,'home_customer/viewordercatboy.html', dic)
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

    return redirect('viewcatboyrequestbycustomer', id=id,oid = oid)

def completeCatboyrequest(request, id, cid, oid, date):
    obj_status=CBorders.objects.get(cbid=cid, oid=oid, date=date)
    
    obj_status.update(status='complete')
    return redirect('viewcatboyrequestbycustomer', id=id,oid = oid)

def viewOurOrder(request, id, cid,fdate, tdate):
    try:
        if request.session[str(id)]:
            objects= MahalCalendar.objects.get(id=cid, cid =id, from_date=fdate, to_date=tdate)
            dic = {'id': id}
            dic['obj']=dict(objects)
            if SignupMahalService.objects.filter(pk=objects.id).exists():
                dic['rev']=dict(SignupMahalService.objects.get(pk=objects.id))
            dic['per']=dic['obj']['amount']//dic['obj']['rent_hr']
            return render(request, 'home_customer/vieworderuser.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def updateOurOrder(request, id, cid,fdate, tdate, status):
    MahalCalendar.objects.get(id=cid, cid =id, from_date=fdate, to_date=tdate).update(status=status)
    return redirect('viewcustomerorderbycustomer', id, cid, fdate, tdate)

def viewServiceOrder(request, id, cid, type, date):
    try:
        if request.session[str(id)]:
            objects= CateringServiceOrder.objects.get(receiver_id=cid ,booker_id =id,  reg_type=type, date=date)
            dic = {'id': id}
            dic['obj']=dict(objects)
            if SignupCateringService.objects.filter(pk=objects.receiver_id).exists():
                dic['rev']=dict(SignupCateringService.objects.get(pk=objects.receiver_id))
            dic['per']=dic['obj']['amount']//dic['obj']['plates']
            return render(request, 'home_customer/viewordercatering.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def completeCateringRequest(request, id, cid, type, date):
    objects= CateringServiceOrder.objects.get(receiver_id=cid ,booker_id =id,  reg_type=type, date=date)
    objects.update(status="complete")
    return redirect('viewcateringrequestbycustomer', id=id, cid=cid, type=type, date=date)

def cancelCateringRequest(request, id, cid, type, date):
    objects= CateringServiceOrder.objects.get(receiver_id=cid ,booker_id =id,  reg_type=type, date=date)
    objects.update(status="cancel")
    return redirect('viewcateringrequestbycustomer', id=id, cid=cid, type=type, date=date)

def history(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupCustomer.objects.get(pk=id))
            dic['current_catering']=[]
            hist_obj= CateringBoyOrder.objects.filter(cid=id, date__lt=datetime.date(datetime.now()))
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
            for x in CateringServiceOrder.objects.filter(booker_id=id):
                if x.status=="complete":
                    dic['service_book'].append(x)

            dic['service_book'].sort(key=lambda xx:xx['date'])
            dic['calendar'] =[]
            for x in MahalCalendar.objects.filter(cid=id, from_date__gte=datetime.date(datetime.now())):
                if x.status=="complete" or x.status =="blocked":
                    dic['calendar'].append(x)
            
            return render(request, 'home_customer/history.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)



