from django.shortcuts import render, redirect
from django.http import HttpResponse
from signup.models import *
import uuid

# Create your views here.
def Login(request):
    if request.method=='POST':
        email= request.POST['email']
        password = request.POST['password']
        obj_email=UserEmail.objects.filter(pk= email)
        if obj_email.exists():
            for obj in obj_email:
                service = obj.service

            if service=="catering_service":
                obj = SignupCateringService.objects.get(email=email)
                db_password=obj.password
                db_name=obj.name
                db_pic = obj.prof_img   
                db_id=str(obj.id)

                if db_password==password:
                    request.session[db_id]=1
                    return redirect('homecatering',id=db_id) 

                else:
                    return render(request, 'login.html', {'msg': 'Entered Password Not Match', 'email':email})          

            elif service=="catering_boy":
                obj = SignupCateringBoy.objects.get(email=email)
                db_password=obj.password
                db_name=obj.name
                db_pic = obj.prof_img 
                db_id=str(obj.id)  

                if db_password==password:
                    request.session[db_id]=1
                    return redirect('homecatboy',id=db_id)  

                else:
                    return render(request, 'login.html', {'msg': 'Entered Password Not Match', 'email':email})        

            elif service == "customer":
                obj = SignupCustomer.objects.get(email=email)
                db_password=obj.password
                db_name=obj.name
                db_pic = obj.prof_img 
                db_id=str(obj.id)
                
                if db_password==password:
                    request.session[db_id]=1
                    return redirect('homecustomer',id=db_id)  

                else:
                    return render(request, 'login.html', {'msg': 'Entered Password Not Match', 'email':email})    

            elif service =="mahal":
                obj = SignupMahalService.objects.get(email=email)
                db_password=obj.password
                db_name=obj.name
                db_pic = obj.prof_img 
                db_id=str(obj.id)
            
                if db_password==password:
                    request.session[db_id]=1
                    
                    return redirect('homemahal',id=db_id)  
                else:
                    return render(request, 'login.html', {'msg': 'Entered Password Not Match', 'email':email})

        else:
            return render(request, 'login.html', {'msg': 'E-Mail Does not Exists'})
    
    return render(request, 'login.html')

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def logout(request, service):
    a=dict(request.session)
    print(a)
    request.session.flush()
    
    for x in a.keys():
        if is_valid_uuid(x) and x != str(service):
            request.session[x]=1
    a=dict(request.session)
    print(a)
    return redirect('login')

def home(request):
    return render(request, 'home.html')