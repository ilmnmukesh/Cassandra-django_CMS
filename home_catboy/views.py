from django.shortcuts import render, redirect
from signup.models import SignupCateringBoy, SignupCateringService, SignupMahalService, SignupCustomer
from .models import CBorders
from home_catering.models import CateringBoyOrder
import uuid
from django.views.decorators.cache import never_cache
from datetime import time

def home(request, id):
    
    try:
        if request.session[str(id)]:
            a=dict(SignupCateringBoy.objects.get(id=id))   
            
            ordered_obj = CBorders.objects.filter(cbid=id)
            a['empty_acc']=0
            a['empty_comp']=0
            if ordered_obj.exists():
                a['list_pending']=[]
                a['list_accept']=[]
                a['list_complete']=[]
                for obj in ordered_obj:
                    for x in CateringBoyOrder.objects.filter(id=obj.oid,date=obj.date):
                        x=dict(x)
                        ss=str(x['timing']).split(":")
                        x['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                        if obj.status=='pending':
                            a['list_pending'].append(x)
                        elif obj.status=='complete':
                            a['empty_comp']=1
                            a['list_complete'].append(x)
                        else:
                            a['list_accept'].append(x)
                a['list_complete']=a['list_complete']

                if len(a['list_accept'])>0:
                    a['notification']=len(a['list_accept'])
                if len(a['list_accept'])>0 or len(a['list_pending'])>0:
                    a['empty_acc']=1
            
            a['picture']=[]

            for obj in CateringBoyOrder.objects.all():
                if obj.catboy_max>0:
                    if not(CBorders.objects.filter(date=obj.date,cbid=id, oid=obj.id).exists()):
                        if SignupCateringService.objects.filter(pk=obj.cid).exists():
                            x = SignupCateringService.objects.get(pk=obj.cid)
                        elif SignupCateringBoy.objects.filter(pk=obj.cid).exists():
                            x = SignupCateringBoy.objects.get(pk=obj.cid)
                        #x= SignupCateringService.objects.get(pk=obj.cid)
                        elif SignupMahalService.objects.filter(pk=obj.cid).exists():
                            x = SignupMahalService.objects.get(pk=obj.cid)
                        else:
                            x=SignupCustomer.objects.get(pk=obj.cid)            
            
                        dic={'name':x.name, 'venue':obj.venue,'pic':x.prof_img, 'amount':obj.amount,'oid':obj.id,'date':obj.date}
                        ss=str(obj.timing).split(":")
                        dic['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')

                        if CBorders.objects.filter(date=obj.date,cbid=id):
                            dic['msg']='You already Have Request on this date'
                        a['picture'].append(dic)
            a['picture'].sort(key=lambda y:y['date'])
            a['picture1']=a['picture'][:3]
            a['picture2']={'name':''}
            a['picture3']={'name':''}
                
            if len(a['picture'])>3:
                a['picture2']=a['picture'][3:6]
                
                if len(a['picture'])>6:
                    a['picture3']= a['picture'][6:9]
            a['home']=1
            return render(request, 'home_catboy/home.html', a)
        else:
            return redirect('login')

    except:
        return redirect('logout', service=id)

def orderRequest(request, cid, oid, date ):
    id = uuid.uuid4()
    if not(CBorders.objects.filter(date=date,cbid=cid).exists()):
        if not(CBorders.objects.filter(cbid=cid,oid=oid,date=date).exists()):
            CBorders.objects.create(id=id, cbid=cid,oid=oid, date=date, status="pending")

    return redirect('homecatboy', id=cid)    

def orderCancel(request, cid, oid, date):
    x= CBorders.objects.get(cbid=cid,oid=oid,date=date)
    x.delete()
    return redirect('homecatboy', id=cid)

def orderHistory(request, id):
    try:
        if request.session[str(id)]:
            hist_obj= CBorders.objects.filter(cbid=id, status='complete')
            dic={}
            dic['prof_img']=SignupCateringBoy.objects.get(pk =id).prof_img
            dic['complete']=[]
            if hist_obj.exists():
                dic['empty']=1
                for obj in hist_obj:
                    for catering_details in CateringBoyOrder.objects.filter(id=obj.oid,date=obj.date):
                        details=dict(catering_details)
                        if SignupCateringService.objects.filter(pk=details['cid']).exists():
                            details['pic'] = SignupCateringService.objects.get(pk=details['cid']).prof_img
                        elif SignupCateringBoy.objects.filter(pk=details['cid']).exists():
                            details['pic']= SignupCateringBoy.objects.get(pk=details['cid']).prof_img
                        
                        ss=str(details['timing']).split(":")
                        details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                        dic['complete'].append(details)
                dic['complete'].sort(key=lambda xx:xx['date'], reverse=True)
            else:
                dic['empty']=0
            dic['id']=id
            return render(request,'home_catboy/history.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service=id)
    
def orderEarnings(request, id):
    try:
        if request.session[str(id)]:
            hist_obj= CBorders.objects.filter(cbid=id, status='complete')
            dic={}
            dic['prof_img']=SignupCateringBoy.objects.get(pk =id).prof_img
            dic['complete']=[]
            if hist_obj.exists():
                dic['empty']=1
                dic['total']=0
                for obj in hist_obj:
                    for catering_details in CateringBoyOrder.objects.filter(id=obj.oid,date=obj.date):
                        details=dict(catering_details)
                        ss=str(details['timing']).split(":")
                        details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                        dic['total']+=details['amount']
                        dic['complete'].append(details)
                dic['complete'].sort(key=lambda xx:xx['date'])
            else:
                dic['empty']=0
            dic['id']=id
            return render(request,'home_catboy/earning.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service=id)

def catboyOrder(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupCateringBoy.objects.get(id=id))  
            request.session['catboy']=1
            return render(request, 'home_catboy/createorder.html', a)
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
        return redirect('homecatboy', id=id)
    else:
        return redirect('catboyorder', id=id)

def viewCatboyOrder(request, id):
    try:
        if request.session[str(id)]:
            hist_obj= CateringBoyOrder.objects.filter(cid=id)
            dic={}
            dic['complete']=[]
            if hist_obj.exists():
                dic['empty']=1
                for obj in hist_obj:
                    details=dict(obj)                    
                    ss=str(details['timing']).split(":")
                    details['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')
                    if details['catboy_max']<1:
                        details['count_empty']=1
                    dic['complete'].append(details)
                dic['complete'].sort(key=lambda xx:xx['date'])
            else:
                dic['empty']=0
            
            dic['id']=id
            return render(request,'home_catboy/vieworder.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service=id)

def viewCatboyOrderList(request, id, oid):
    try:
        if request.session[str(id)]:
            hist_obj= CBorders.objects.filter(oid=oid)
            dic={}
            dic['list_pending']=[]
            dic['list_accept']=[]
            if hist_obj.exists():
                dic['empty']=1
                for obj in hist_obj:
                    if obj.status=='pending':
                        x=dict(SignupCateringBoy.objects.get(pk=obj.cbid))
                        x['date']=obj.date
                        dic['list_pending'].append(x)
                    else:
                        dic['list_accept'].append(dict(SignupCateringBoy.objects.get(pk=obj.cbid)))

            else:
                dic['empty']=0
            
            dic['id']=id
            dic['oid']=oid
            return render(request,'home_catboy/vieworderlist.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service='catboy')
    
def orderAccept(request, id, cid, oid, date):

    obj_status=CBorders.objects.get(cbid=cid, oid=oid, date=date)
    obj_cbcount= CateringBoyOrder.objects.get(pk=oid)
    
    obj_status.update(status='accept')
    obj_cbcount.update(catboy_max= obj_cbcount.catboy_max -1)
    if obj_cbcount.catboy_max==1:
        for x in CBorders.objects.filter(oid=oid, status='pending'):
            x.delete()

    return redirect('viewcatboyorderlist', id=id,oid = oid)

def viewCatboyOrderAccept(request, id, oid):
    try:
        if request.session[str(id)]:
            hist_obj= CBorders.objects.filter(oid=oid)
            dic={}
            dic['list_accept']=[]
            if hist_obj.exists():
                dic['empty']=1
                for obj in hist_obj:
                    x=dict(SignupCateringBoy.objects.get(pk=obj.cbid))
                    x['date']=obj.date
                    x['complete']=1
                    if obj.status=="complete":
                        x['complete']=0
                    dic['list_accept'].append(x)

            else:
                dic['empty']=0
            
            dic['id']=id
            dic['oid']=oid
            return render(request,'home_catboy/viewacceptorder.html', dic)
        else:
            return redirect('login')
    except:
        return redirect('logout', service=id)
    
def orderComplete(request, id,cid, oid, date):
    obj_status=CBorders.objects.get(cbid=cid, oid=oid, date=date)
    obj_status.update(status='complete')
    return redirect('viewcatboyorderaccept', id=id,oid=oid)

def searchService(request, id):
    try:
        if request.session[str(id)]:
            a={}
            if request.method=="POST" or len(request.session['catboysearch']):
                try:
                    search=request.POST['q']
                    request.session['catboysearch']=search
                except:
                    search=request.session['catboysearch']
                
                a['empty']=0
                search_list=[]
                list_value=CateringBoyOrder.objects.all()
                for value in list_value:
                    if search.lower() in value.venue['location'].lower():
                        search_list.append(value)

                if len(search_list):
                    a['empty']=1
                    a['picture']=[]
                    for obj in search_list:
                        if obj.catboy_max>0:
                            if not(CBorders.objects.filter(date=obj.date,cbid=id, oid=obj.id).exists()):
                                if SignupCateringService.objects.filter(pk=obj.cid).exists():
                                    x = SignupCateringService.objects.get(pk=obj.cid)
                                elif SignupCateringBoy.objects.filter(pk=obj.cid).exists():
                                    x = SignupCateringBoy.objects.get(pk=obj.cid)
                                #x= SignupCateringService.objects.get(pk=obj.cid)
                                
                                dic={'name':x.name, 'venue':obj.venue,'pic':x.prof_img, 'amount':obj.amount,'oid':obj.id,'date':obj.date}
                                ss=str(obj.timing).split(":")
                                dic['time']=time(int(ss[0]),int(ss[1])).strftime('%I:%M %p')

                                if CBorders.objects.filter(date=obj.date,cbid=id):
                                    dic['msg']='You already Have Request on this date'
                                a['picture'].append(dic)
                    a['picture'].sort(key=lambda y:y['date'])
                a['search']=search
            a['id']=id
            return render(request, 'home_catboy/searchlist.html', a)
        else:
            return redirect('login')
    except:
        return redirect('logout', service=id)

def searchOrderRequest(request, cid, oid, date):
    id = uuid.uuid4()
    if not(CBorders.objects.filter(date=date,cbid=cid).exists()):
        if not(CBorders.objects.filter(cbid=cid,oid=oid,date=date).exists()):
            CBorders.objects.create(id=id, cbid=cid,oid=oid, date=date, status="pending")
    return redirect('searchservice', id=cid)    

