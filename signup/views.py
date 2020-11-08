from django.shortcuts import render
from .models import *

from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.


class Pic:
    def __init__(self, name, img, service):
        self.name = name
        self.image = img
        self.service = service
        self.loc = ''
        self.pos=0

    def location(self):
        return "/media/profile/"+self.service
    
    def FileInsert(self):
        return  FileSystemStorage(location='media/profile/'+self.service) 
    
    def Model(self, loc_img):
        if self.service=="catering_service":
            x = SignupCateringService.objects.filter(prof_img = loc_img)
        elif self.service=="catering_boy":
            x = SignupCateringBoy.objects.filter(prof_img = loc_img)
        elif self.service == "customer":
            x = SignupCustomer.objects.filter(prof_img = loc_img)
        elif self.service =="mahal":
            x = SignupMahalService.objects.filter(prof_img = loc_img)
        else:
            x=''
        return x
    
    def main(self):
        loc_img=''
        if self.image!='':
            ext = [x for x in self.image.name.split('.')][1]
            self.loc= self.location()
            file_insert = self.FileInsert()
            loc_img = self.loc+'/'+self.name+str(self.pos)+'.'+ext
            while True:
                for x in self.Model(loc_img):
                    self.pos=int(x.prof_img.split('.')[0][-1])+1
                    loc_img = self.loc+'/'+self.name+str(self.pos)+'.'+ext
                if not(self.Model(loc_img).exists()):
                    break
            file_insert.save(self.name+str(self.pos)+'.'+ext, self.image)
        return loc_img

def SignupMain(request):
    return render(request, 'signup.html')

def SignupCatBoy(request):
    if request.method == "POST":
        current_service="catering_boy"
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('add')
        try:
            img = request.FILES['image']

        except:
            img = ''

        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        password = request.POST.get('password') 
        cpassword = request.POST.get('cpassword')

        if password==cpassword:
            if UserEmail.objects(pk=email).exists():
                field = UserEmail.objects.get(pk=email).service
                return render(request, 'signup/cateringboy.html', {
                    'name':name, 'age':age, 'add':address, 'city':city,
                    'pincode':pincode,'phone':phone,
                    'msg':'EmailId Already exists for '+ field 
                })
            
            else:
                loc_img =Pic(name,img, current_service).main()
                
                user=UserEmail(email=email, service=current_service)
                SignupCateringBoy.objects.create(
                    name=name, email=email, 
                    age=age, address={'street':address,'city':city,'pincode':str(pincode)},
                    prof_img=loc_img, ph_numb=phone, password=password
                )
                user.save()
                request.session.flush()
                return render(request, 'login.html', {'msg':'Accounts Create Succesfully','email':email, 'img':loc_img})
        else:
            return render(request, 'signup/cateringboy.html', {
                'name':name, 'age':age,'email':email,'add':address,
                 'city':city, 'pincode':pincode, 'phone':phone, 'msg':'Password Miss Match'
                })

    return render(request, 'signup/cateringboy.html')

def SignupCatering(request):
    if request.method == "POST":
        current_service="catering_service"
        name = request.POST.get('name')
        experience = request.POST.get('experience')
        manager= request.POST.get('manager')
        email = request.POST.get('email')
        address = request.POST.get('add')
        try:
            img = request.FILES['image']

        except:
            img = ''

        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password') 
        cpassword = request.POST.get('cpassword')

        if password==cpassword:
            if UserEmail.objects(pk=email).exists():
                field = UserEmail.objects.get(pk=email).service
                return render(request, 'signup/catering.html', {
                    'name':name, 'experience':experience, 'manager':manager,
                'add':address, 'city':city, 'pincode':pincode, 'mobile':mobile, 'phone':phone,
                 'msg':'EmailId Already exists for '+ field 
                })
            
            else:
                
                loc_img =Pic(name,img, current_service).main()
                
                user=UserEmail(email=email, service=current_service)
                SignupCateringService.objects.create(
                    name=name, manager=manager, email=email, 
                    experience=experience,address={'street':address,'city':city,'pincode':str(pincode)},
                    prof_img=loc_img, contact=[mobile,phone], password=password
                )
                user.save()
                request.session.flush()
                return render(request, 'login.html', {'msg':'Accounts Create Succesfully','email':email, 'img':loc_img})
        else:
            return render(request, 'signup/catering.html', {
                'name':name, 'experience':experience, 'manager':manager, 'email':email,
                'add':address, 'city':city, 'pincode':pincode, 'mobile':mobile, 'phone':phone, 'msg':'Password Miss Match'
                })

    return render(request, 'signup/catering.html')

def SignupMahal(request):
    if request.method == "POST":
        current_service="mahal"
        name = request.POST.get('name')
        build = request.POST.get('build')
        manager= request.POST.get('manager')
        email = request.POST.get('email')
        address = request.POST.get('add')
        try:
            img = request.FILES['image']

        except:
            img = ''

        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password') 
        cpassword = request.POST.get('cpassword')

        if password==cpassword:
            if UserEmail.objects(pk=email).exists():
                field = UserEmail.objects.get(pk=email).service
                return render(request, 'signup/mahal.html', {
                    'name':name, 'build':build, 'manager':manager,
                'add':address, 'city':city, 'pincode':pincode, 'mobile':mobile, 'phone':phone,
                 'msg':'EmailId Already exists for '+ field 
                })
            
            else:
                
                loc_img =Pic(name,img, current_service).main()
                
                user=UserEmail(email=email, service=current_service)
                SignupMahalService.objects.create(
                    name=name, manager=manager, email=email, 
                    build_yr=build,address={'street':address,'city':city,'pincode':str(pincode)},
                    prof_img=loc_img, contact=[mobile,phone], password=password
                )
                user.save()
                request.session.flush()
                return render(request, 'login.html', {'msg':'Accounts Create Succesfully','email':email, 'img':loc_img})
        else:
            return render(request, 'signup/mahal.html', {
                'name':name, 'build':build, 'manager':manager, 'email':email,
                'add':address, 'city':city, 'pincode':pincode, 'mobile':mobile, 'phone':phone, 'msg':'Password Miss Match'
                })
    return render(request, 'signup/mahal.html')

def SignupCust(request):
    if request.method == "POST":
        female=''
        current_service="customer"
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST['gender']
        if gender=='Female':
            female='checked'
        email = request.POST.get('email')
        address = request.POST.get('add')
        try:
            img = request.FILES['image']

        except:
            img = ''

        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        password = request.POST.get('password') 
        cpassword = request.POST.get('cpassword')

        if password==cpassword:
            if UserEmail.objects(pk=email).exists():
                field = UserEmail.objects.get(pk=email).service
                return render(request, 'signup/customer.html', {
                    'name':name,'gender':female, 'age':age, 'add':address, 'city':city,
                    'pincode':pincode,'phone':phone,
                    'msg':'EmailId Already exists for '+ field 
                })
            
            else:
                loc_img =Pic(name,img, current_service).main()
                
                user=UserEmail(email=email, service=current_service)
                SignupCustomer.objects.create(
                    name=name, email=email, gender=gender,
                    age=age,address={'street':address,'city':city,'pincode':str(pincode)},
                    prof_img=loc_img, ph_numb=phone, password=password
                )
                user.save()
                request.session.flush()
                return render(request, 'login.html', {'msg':'Accounts Create Succesfully','email':email, 'img':loc_img})
        else:
            return render(request, 'signup/customer.html', {
                'name':name, 'age':age,'email':email,'add':address,'gender':female,
                 'city':city, 'pincode':pincode, 'phone':phone, 'msg':'Password Miss Match'
                })

    return render(request, 'signup/customer.html')