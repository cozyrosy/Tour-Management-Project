from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from.models import ClientDetails
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'user/base.html')

def Register(request):
    if request.method=='POST':
        f_name=request.POST['c_fname']
        l_name = request.POST['c_lname']
        mail = request.POST['c_email']
        contact = request.POST['c_phone']
        password = request.POST['c_password']
        cpassword = request.POST['c_repassword']
        address = request.POST['c_address']
        photo = request.FILES['c_image']

        if password==cpassword:
            if User.objects.filter(username=mail).exists():
                messages.info(request,'email already exists')

            else:
                user=User.objects.create_user(username=mail,password=password)
                customer=ClientDetails(id=user,first_name=f_name,last_name=l_name,phone=contact,
                                        address=address, photo=photo)
                user.save()
                customer.save()
                return redirect('user:login')
        else:
            messages.info(request,'password mismatch')
    return render(request,'user/Register.html')

def Login(request):

    if request.method=='POST':
        mail=request.POST['c_email']
        password=request.POST['c_password']
        user=auth.authenticate(username=mail,password=password)

        if user is not None and ClientDetails.objects.filter(id=user.id).exists():
            auth.login(request,user)
            return redirect('user/profile')
        else:
            messages.info(request,'invalid credential')
    return render(request,'user/login.html')

def Logout(request):
    auth.logout(request)
    return redirect('user:home')


@login_required(login_url='user/login')
def Customer_Profile(request):
    profile=ClientDetails.objects.get(id=request.user.id)
    return render(request,'user/profile.html', {'profile': profile})