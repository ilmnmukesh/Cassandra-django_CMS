from django.shortcuts import render, redirect
from signup.models import *
from .models import MahalGallery, CateringBookingTemp, MahalCalendar
from home_catering.models import *
from home_catboy.models import CBorders
from datetime import time, datetime
from django.template.defaulttags import register
import uuid, random
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.files.storage import FileSystemStorage


@register.filter
def get_current_date(x):
    return str(datetime.date(datetime.now()))

def home(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupMahalService.objects.get(pk=id))
            dic['current_catboy']=[]
            hist_obj= CateringBoyOrder.objects.filter(cid=id)
            if hist_obj.exists():
                for obj in hist_obj:
                    details=dict(obj)                    
                    ss=str(details['timing']).split(":")
                    details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                    if details['catboy_max']<1:
                        details['count_empty']=1
                    dic['current_catboy'].append(details)
                dic['current_catboy'].sort(key=lambda xx:xx['date'])
            
            dic['list_catboy']=list(SignupCateringBoy.objects.all().limit(2))
            
            dic['list_catering']=[]
            for value in SignupCateringService.objects.all().limit(2):
                d=dict(value)
                d['gallery_pic']=''
                if CateringGallery.objects.filter(pk=value.id).exists():
                    gallery = random.choice(CateringGallery.objects.get(pk=value.id).gallery_pic)
                    d['gallery_pic']=gallery
                dic['list_catering'].append(d)
            return render(request,'home_mahal/home.html', dic)

        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def searchCatering(search):
    search_list=[]                
    list_value=SignupCateringService.objects.all()
    if search != '':
        for value in list_value:
            if search.lower() in value.name.lower():
                dic=dict(value)
                dic['gallery_pic']=''
                if CateringGallery.objects.filter(pk=value.id).exists():
                    gallery = random.choice(CateringGallery.objects.get(pk=value.id).gallery_pic)
                    dic['gallery_pic']=gallery
                search_list.append(dic)
    else:
        for value in list_value:
            dic=dict(value)
            dic['gallery_pic']=''
            if CateringGallery.objects.filter(pk=value.id).exists():
                gallery = random.choice(CateringGallery.objects.get(pk=value.id).gallery_pic)
                dic['gallery_pic']=gallery
            search_list.append(dic)
    return search_list

def catboyOrder(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupMahalService.objects.get(id=id))  
            request.session['mahal']=1
            return render(request, 'home_mahal/createcatboyorder.html', a)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def createCatboyOrderByMahal(request, id):
    if request.method=='POST':
        add= request.POST['add']
        city= request.POST['city']
        pincode= request.POST['pincode']
        catboy= request.POST['nocatboy']
        amount= request.POST['amount']
        date= request.POST['date']
        time= datetime.strptime(request.POST['time'],'%H:%M').time()
        
        mobile=str(request.POST['mobile'])
        phone =str(request.POST['phone'])
        
        CateringBoyOrder.objects.create(cid=id,amount=amount,date=date, timing=time, catboy_max=catboy,
             venue={'address':add+','+city+','+pincode,'mobile':mobile, 'phone':phone, 'location':city},count=catboy,
            )
        return redirect('homemahal', id=id)
    else:
        return redirect('catboyorder', id=id)

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
            return render(request, 'home_mahal/viewcatering.html', search_list)
        
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id)

def viewCatboy(request, id):
    try:
        if request.session[str(id)]:
            search_list={}
            pag= request.GET.get('page_catboy',1)
            pagnator=Paginator(SignupCateringBoy.objects.all(),1)
            try:
                des=pagnator.page(pag)
            except PageNotAnInteger:
                des=pagnator.page(1)
            except EmptyPage:
                des=pagnator.page(pagnator.num_pages)

            search_list['catboy']=des
            search_list['id']=id
            return render(request, 'home_mahal/viewcatboy.html', search_list)
        
    
        else:    
            return redirect('login')

    except:
        return redirect('logout', service=id)

def searchCatboy(search):
    search_list=[]                
    list_value=SignupCateringBoy.objects.all()
    for value in list_value:
        if search.lower() in value.name.lower():
            search_list.append(dict(value))
    return search_list

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
            return render(request, 'home_mahal/viewcatboy.html', search_list)
    
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

            return render(request, 'home_mahal/viewcatering.html', search_list)
    
        else:
            
            return redirect('login')
    except:
        return redirect('logout', service=id) 

def gallery(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupMahalService.objects.get(pk=id))
            if MahalGallery.objects.filter(id=id).exists():
                dic['gallery']=dict(MahalGallery.objects.get(id=id))

            return render(request, 'home_mahal/gallery.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service= id)

def addgallery(request, id):
    if request.method=="POST":
        try:
            img = request.FILES['imgs']
        
            user_name=SignupMahalService.objects.get(id =id).name
            fs = FileSystemStorage(location='media/gallery/Mahal/'+user_name)
            ext = img.name.split('.')[-1]

            if not(MahalGallery.objects.filter(pk=id).exists()):
                fs.save(user_name+str(0)+'.'+ext, img)
                pic_insert= '/media/gallery/Mahal/'+user_name+'/'+user_name+str(0)+'.'+ext
                MahalGallery.objects.create(id=id, gallery_pic=[pic_insert])
            else:
                obj=MahalGallery.objects.get(pk=id)
                len_obj=len(obj.gallery_pic)
                pos_value=[]
                for x in obj.gallery_pic:
                    pos_value.append(int(x.split('.')[0][-1]))

                if len_obj<6:
                    for x in range(len_obj+1):
                        if x not in pos_value:
                            fs.save(user_name+str(x)+'.'+ext, img)
                            pic_insert= '/media/gallery/Mahal/'+user_name+'/'+user_name+str(x)+'.'+ext
                            break
                    
                    MahalGallery.objects(id=id).update(gallery_pic__append=[pic_insert])
                    
            return redirect('mahalgallery', id=id)
        except:
            return redirect('mahalgallery', id=id)
    else:
        return redirect('mahalgallery', id=id)

def delete(request, id, pos):
    user = SignupMahalService.objects.get(id =id)
    fs = FileSystemStorage(location='media/gallery/Mahal/'+user.name)
    gallery= MahalGallery.objects.get(id =id)
    pic_img=gallery.gallery_pic
    z=0
    del_name=''
    for x in pic_img:
        if pos == int(x.split('.')[0][-1]):
            del_name=x.split('/')[-1]
            pic_img.pop(z)
            break
        z+=1
    gallery.update(gallery_pic=pic_img)
    fs.delete(del_name)
    return redirect('mahalgallery', id=id)

def dictProdSum(dic):
    sum_ = 0 
    for list_ in dic:
        prod=1
        for val in list_:
            prod*=val
        sum_+=prod
    return sum_

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
            
            return render(request, 'home_mahal/viewcateringuser.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service= id)

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
            for obj in  CateringBookingTemp.objects.filter(pk=id):
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

            return render(request, 'home_mahal/bookcatering.html', dic)
        else:    
            return redirect('login')
    except:
        return redirect('logout', service=id)

def addToCart(request, id, cid, type, name, rate, count,veg):
    CateringBookingTemp.objects.create(id=id, cid=cid, reg_type=type, foodname=name, amount=[rate, count],veg_non=veg)
    return redirect('bookcateringbymahal',id= id,cid=cid)

def deleteToCart(request, id, cid, type, name):
    CateringBookingTemp.objects(id=id, cid=cid, reg_type=type, foodname=name).delete()
    return redirect('bookcateringbymahal',id= id,cid=cid)

def bookOrder(request, id, cid):
    dinner={'veg':[], 'non_veg':[]}
    lunch={'veg':[], 'non_veg':[]}
    mrng=[]
    dinner_amt, lunch_amt, mrng_amt=0, 0, 0
    temp_data=CateringBookingTemp.objects(id=id, cid=cid)
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
    return redirect('viewcateringuserbymahal', id=id, cid=cid)

def calendar(request, id):
    dic={'id':id, 'calendar': []}
    dic['calendar'] = list(MahalCalendar.objects.filter(id=id, from_date__gte=datetime.date(datetime.now())))
    dic['amt']=SignupMahalService.objects.get(pk=id).rent_amount
    return render(request, 'home_mahal/calendar.html', dic)

def blockCalendar(request, id):
    if request.method=="POST":
        from_date=request.POST['from']
        to_date=request.POST['to']
        time = datetime.strptime(to_date,'%Y-%m-%d' ) - datetime.strptime(from_date, '%Y-%m-%d')
        time= str(time/60).split(':')[1]
        MahalCalendar.objects.create(id=id, cid=id, from_date=from_date, to_date =to_date,booker_name='User', status="blocked", amount=0, rent_hr=int(time)+24)

    return redirect('mahalcalendar',id)

def rentUpdate(request, id):
    if request.method=="POST":
        amt =request.POST['amt']
        SignupMahalService.objects(pk=id).update(rent_amount=amt)
    return redirect('mahalcalendar',id)

def viewOrder(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupMahalService.objects.get(pk=id))
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
            dic['calendar'] = list(MahalCalendar.objects.filter(id=id, from_date__gte=datetime.date(datetime.now())))
            
            return render(request, 'home_mahal/vieworders.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def viewServiceOrder(request, id, cid, type, date):
    try:
        if request.session[str(id)]:
            objects= CateringServiceOrder.objects.get(receiver_id=cid ,booker_id =id,  reg_type=type, date=date)
            dic = {'id': id}
            dic['obj']=dict(objects)
            if SignupCateringService.objects.filter(pk=objects.receiver_id).exists():
                dic['rev']=dict(SignupCateringService.objects.get(pk=objects.receiver_id))
            dic['per']=dic['obj']['amount']//dic['obj']['plates']
            return render(request, 'home_mahal/viewordercatering.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def completeCateringRequest(request, id, cid, type, date):
    objects= CateringServiceOrder.objects.get(receiver_id=cid ,booker_id =id,  reg_type=type, date=date)
    objects.update(status="complete")
    return redirect('viewcateringrequestbymahal', id=id, cid=cid, type=type, date=date)

def cancelCateringRequest(request, id, cid, type, date):
    objects= CateringServiceOrder.objects.get(receiver_id=cid ,booker_id =id,  reg_type=type, date=date)
    objects.update(status="cancel")
    return redirect('viewcateringrequestbymahal', id=id, cid=cid, type=type, date=date)

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
            return render(request,'home_mahal/viewordercatboy.html', dic)
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
            dic=dict(SignupMahalService.objects.get(pk=id))
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
            for x in MahalCalendar.objects.filter(id=id, from_date__gte=datetime.date(datetime.now())):
                if x.status=="complete" or x.status =="blocked":
                    dic['calendar'].append(x)
            
            return render(request, 'home_mahal/history.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def earning(request, id):
    try:
        if request.session[str(id)]:
            dic=dict(SignupMahalService.objects.get(pk=id))
            dic['total']=0
            dic['calendar'] =[]
            for x in MahalCalendar.objects.filter(id=id):
                if x.status=="complete":
                    dic['total']+=x.amount
                    dic['calendar'].append(x)
                elif x.status=="blocked":
                    dic['calendar'].append(x)
                
            return render(request, 'home_mahal/earning.html', dic)
        else:    
            return redirect('login')

    except:
        return redirect('logout', service=id)

def viewOurOrder(request, id, cid,fdate, tdate):
    try:
        if request.session[str(id)]:
            objects= MahalCalendar.objects.get(id=id, cid =cid, from_date=fdate, to_date=tdate)
            dic = {'id': id}
            dic['obj']=dict(objects)
            if SignupCustomer.objects.filter(pk=objects.cid).exists():
                dic['rev']=dict(SignupCustomer.objects.get(pk=objects.cid))

            dic['per']=dic['obj']['amount']//dic['obj']['rent_hr']
            return render(request, 'home_mahal/vieworderuser.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout',service=id)

def updateOurOrder(request, id, cid,fdate, tdate, status):
    MahalCalendar.objects.get(id=id, cid =cid, from_date=fdate, to_date=tdate).update(status=status)
    return redirect('viewcustomerorderbymahal', id, cid, fdate, tdate)

    