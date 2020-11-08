from django.shortcuts import render, redirect
from signup.models import *
from signup.views import Pic
from django.core.files.storage import FileSystemStorage
# Create your views here.
class EmailRedirect:

    def __init__(self, service, id, msg, name, pos):
        self.service=service
        self.msg=msg
        self.pos= pos
        self.active=['', '', '', '', '']
        self.id= id
        self.name= name
        self.a={}

    def dic(self):
        self.active[self.pos-1]='active'
        self.a['msg']={self.name:self.msg}
        self.a['active']=self.active

    def main(self):
        if self.service=='catering':
            self.a=dict(SignupCateringService.objects.get(id=self.id))
            self.dic()
            return 'profile/catering.html', self.a

        elif self.service=='catboy':
            self.a=dict(SignupCateringBoy.objects.get(id=self.id))
            self.dic()
            return 'profile/cateringboy.html', self.a
        
        elif self.service=='customer':
            self.a=dict(SignupCustomer.objects.get(id=self.id))
            self.dic()
            return 'profile/customer.html', self.a
        
        else:
            self.a=dict(SignupMahalService.objects.get(id=self.id))
            self.dic()
            return 'profile/mahal.html', self.a

def ServicePage(service):
    if service=='catering':
        return 'editcatering'
    elif service=='catboy':
        return 'editcatboy'
    elif service=='customer':
        return 'editcustomer'
    else:
        return 'editmahal'
        
def editCatering(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupCateringService.objects.get(id=id))
            a['active']=['active', '', '', '', '']
            return render(request, 'profile/catering.html', a)
        else:
            return redirect('login')
    except:
        return redirect('login')

def editCatboy(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupCateringBoy.objects.get(id=id))
            a['active']=['active', '', '', '', '']
            return render(request, 'profile/cateringboy.html', a)
        else:
            return redirect('login')
    except:
        return redirect('login')

def editMahal(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupMahalService.objects.get(id=id))
            a['active']=['active', '', '', '', '']
            return render(request, 'profile/mahal.html', a)
        else:
            return redirect('login')
    except:
        return redirect('login')

def editCustomer(request, id):
    try:
        if request.session[str(id)]:
            a=dict(SignupCustomer.objects.get(id=id))
            a['active']=['active', '', '', '', '']
            if a['gender']=='Female':
                a['female']='checked'
            return render(request, 'profile/customer.html', a)
        else:
            return redirect('login')
    except:
        return redirect('login')

def editDetails(request,service, id):
    if request.method=="POST":
        
        if str(service)=='catering':
            name = request.POST.get('name')
            experience = request.POST.get('experience')
            manager= request.POST.get('manager')
            address = request.POST.get('add')
            city=request.POST.get('city')
            pincode=request.POST.get('pincode')
            SignupCateringService.objects.get(id=id).update(
                name=name, experience=experience, manager=manager,
                address={'street':address,'city':city,'pincode':str(pincode)}
                )
            return redirect('editcatering',id=id)
        
        elif service=='catboy':
            name = request.POST.get('name')
            age= request.POST.get('age')
            address = request.POST.get('add')
            city=request.POST.get('city')
            pincode=request.POST.get('pincode')

            SignupCateringBoy.objects.get(id=id).update(
                name=name, age=age,
                address={'street':address,'city':city,'pincode':str(pincode)}
                )
            return redirect('editcatboy',id=id)

        elif service=='customer':
            name = request.POST.get('name')
            age= request.POST.get('age')
            gender = request.POST.get('gender')
            address = request.POST.get('add')
            city=request.POST.get('city')
            pincode=request.POST.get('pincode')
            SignupCustomer.objects.get(id=id).update(
                name=name, age=age,gender=gender,
                address={'street':address,'city':city,'pincode':str(pincode)}
                )
            return redirect('editcustomer',id=id)

        else:
            name = request.POST.get('name')
            build=request.POST['build']
            manager= request.POST.get('manager')
            address = request.POST.get('add')
            city=request.POST.get('city')
            pincode=request.POST.get('pincode')
            SignupMahalService.objects.get(id=id).update(
                name=name, build_yr=build, manager=manager,
                address={'street':address,'city':city,'pincode':str(pincode)}
                )
            return redirect('editmahal',id=id)
    else:
        redir = ServicePage(service)
        return redirect(redir,id=id)

def editEmail(request, service, id):
    if request.method=="POST":
        email = request.POST.get('email')
        cemail = request.POST.get('cemail')
        if email==cemail:
            if not(UserEmail.objects(pk=email).exists()):


                if str(service)=='catering':
                    obj= UserEmail(email=email, service='catering_service')
                    old=SignupCateringService.objects.get(pk=id)
                    old_email=old.email
                    UserEmail.objects.get(pk=old_email).delete()
                    old.update(email=email)
                    obj.save()
                    return redirect('editcatering',id=id)

                elif service=='catboy':
                    obj= UserEmail(email=email, service='catering_boy')
                    old=SignupCateringBoy.objects.get(pk=id)
                    old_email=old.email
                    UserEmail.objects.get(pk=old_email).delete()
                    old.update(email=email)
                    obj.save()
                    return redirect('editcatboy',id=id)
                
                elif service=='customer':
                    obj= UserEmail(email=email, service='customer')
                    old=SignupCustomer.objects.get(pk=id)
                    old_email=old.email
                    UserEmail.objects.get(pk=old_email).delete()
                    old.update(email=email)
                    obj.save()
                    return redirect('editcustomer',id=id)
                
                else:
                    obj= UserEmail(email=email, service='mahal')
                    old=SignupMahalService.objects.get(pk=id)
                    old_email=old.email
                    UserEmail.objects.get(pk=old_email).delete()
                    old.update(email=email)
                    obj.save()
                    return redirect('editmahal',id=id)

            else:
                msg='Email is Already Exists'
                a, b =EmailRedirect(service, id, msg, 'email',3).main()
                return render(request, a, b)

        else:
            msg='Email is Not matching'
            a, b =EmailRedirect(service, id, msg, 'email', 3).main()
            return render(request, a, b)
    else:
        redir = ServicePage(service)
        return redirect(redir,id=id)

def editContact(request, service, id):
    if request.method=="POST":
        if service=='catering':
            ph = request.POST['phone']
            mob = request.POST['mobile']
            SignupCateringService.objects.get(pk=id).update(contact=[mob, ph])
            return redirect('editcatering',id=id)
        
        elif service=='catboy':
            ph = request.POST['phone']
            SignupCateringBoy.objects.get(pk=id).update(ph_numb=ph)
            return redirect('editcatboy',id=id)
        
        elif service=='customer':
            ph = request.POST['phone']
            SignupCustomer.objects.get(pk=id).update(ph_numb=ph)
            return redirect('editcustomer',id=id)
        
        else:
            ph = request.POST['phone']
            mob = request.POST['mobile']
            SignupMahalService.objects.get(pk=id).update(contact=[mob, ph])
            return redirect('editmahal',id=id)
    else:
        redir = ServicePage(service)
        return redirect(redir,id=id)

def editPassword(request, service, id):
    if request.method=="POST":
        old_pwd = request.POST['opass']
        pwd = request.POST['pass']
        conf_pwd = request.POST['cpass']
        if pwd==conf_pwd:
            if service=='catering':
                obj=SignupCateringService.objects.get(id=id)
                if obj.password==old_pwd:
                    obj.update(password=pwd)
                    return redirect('editcatering',id=id)

                else:
                    msg='Old Password Not Found'
                    a, b =EmailRedirect(service, id, msg,'password', 5).main()
                    return render(request, a, b)

            elif service=='catboy':
                obj=SignupCateringBoy.objects.get(id=id)
                if obj.password==old_pwd:
                    obj.update(password=pwd)
                    return redirect('editcatboy',id=id)

                else:
                    msg='Old Password Not Found'
                    a, b =EmailRedirect(service, id, msg,'password', 5).main()
                    return render(request, a, b)

            elif service=='customer':
                obj=SignupCustomer.objects.get(id=id)
                if obj.password==old_pwd:
                    obj.update(password=pwd)
                    return redirect('editcustomer',id=id)

                else:
                    msg='Old Password Not Found'
                    a, b =EmailRedirect(service, id, msg,'password', 5).main()
                    return render(request, a, b)

            else:
                obj=SignupMahalService.objects.get(id=id)
                if obj.password==old_pwd:
                    obj.update(password=pwd)
                    return redirect('editmahal',id=id)

                else:
                    msg='Old Password Not Found'
                    a, b =EmailRedirect(service, id, msg,'password', 5).main()
                    return render(request, a, b)
            
        else:
            msg='Password Missmatch'
            a, b =EmailRedirect(service, id, msg,'password', 5).main()
            return render(request, a, b)

    else:
        redir = ServicePage(service)
        return redirect(redir,id=id)

def editPicture(request, service, id):
    if request.method=='POST':
        try:
            img=request.FILES['image']
        except:
            img=''
        
        if service=="catering":
            obj=SignupCateringService.objects.get(pk=id)
        
            if obj.prof_img!='':
                name=obj.prof_img.split('/')[-1]
                FileSystemStorage(location='media/profile/catering_service').delete(name)
            loc_img=Pic(obj.name, img, 'catering_service').main()
            obj.update(prof_img = loc_img)
            return redirect('editcatering',id=id)

        elif service=="catboy":
            obj=SignupCateringBoy.objects.get(pk=id)
        
            if obj.prof_img!='':
                name=obj.prof_img.split('/')[-1]
                FileSystemStorage(location='media/profile/catering_boy').delete(name)
            loc_img=Pic(obj.name, img, 'catering_boy').main()
            obj.update(prof_img = loc_img)
            return redirect('editcatboy',id=id)
        
        elif service=="customer":
            obj=SignupCustomer.objects.get(pk=id)
        
            if obj.prof_img!='':
                name=obj.prof_img.split('/')[-1]
                FileSystemStorage(location='media/profile/customer').delete(name)
            loc_img=Pic(obj.name, img, 'customer').main()
            obj.update(prof_img = loc_img)
            return redirect('editcustomer',id=id)

        else:
            obj=SignupMahalService.objects.get(pk=id)
        
            if obj.prof_img!='':
                name=obj.prof_img.split('/')[-1]
                FileSystemStorage(location='media/profile/mahal').delete(name)
            loc_img=Pic(obj.name, img, 'mahal').main()
            obj.update(prof_img = loc_img)
            return redirect('editmahal',id=id)
        

    else:
        redir = ServicePage(service)
        return redirect(redir,id=id)
