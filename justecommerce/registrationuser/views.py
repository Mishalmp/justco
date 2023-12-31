from django.shortcuts import render,redirect

from django.views.decorators.cache import cache_control,never_cache

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout as dj_logout
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib import messages,auth

# verification email
from .models import UserOTP,Mobile_Otp
import re
import random
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.validators import validate_email
from . import mixin
# Create your views here.





def user_signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    
    
    if request.method == 'POST':

        get_otp=request.POST.get('otp')


        if get_otp:

            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)

            

            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                 # messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.warning(request,f'you Entered a Wrong OTP')
                return render(request,'registration/signup.html')

        #user validation
        else:

            firstname=request.POST['fname']
            lastname=request.POST['lname']
            username=request.POST['username']
            phone=request.POST['phone']
            email=request.POST['email']
            password1=request.POST['password1']    
            password2=request.POST['password2']

            #null values checking 

            check=[username,email,password1,password2,phone,firstname,lastname]

            for values in check:

                if values == '':
                    context ={

                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_email':email,
                        'pre_phone':phone,
                        'pre_password1':password1,
                        'pre_password2':password2
                        

                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'registration/signup.html',context)
                else:
                    pass
            result=validate_username(username)

            if result is not False:
                context={
                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                        

                    }
                messages.info(request,result)
                return render(request,'registration/signup.html',context)
            else:
                pass
            try:
                check_number = int(phone)
                if len(phone) <10 :
                    raise Exception
            except:
                context ={
                       'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                messages.info(request,'Enter valid Mobile number')
                return render(request,'registration/signup.html',context)

            resmail=validateemail(email)


            if resmail is False:
                context={
                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                        

                    }
                messages.info(request,'enter valid email')
               
                return render(request,'registration/signup.html',context)
           
            passw = validatepassword(password1)

            if passw is False:
                context={
                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                        

                    }
                messages.info(request,'Enter strong password')
                return render(request,'registration/signup.html',context)
            else:
                pass

            if password1 == password2:
                try:
                    User.objects.get(phone=phone)
                except:
                    pass
                else:
                    context ={
                         'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                    }
                    messages.error(request,'Mobile number is already registered')
                    return render(request,'registration/signup.html',context)

                try:
                    User.objects.get(email=email)
                except:
                    usr=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password1,phone=phone)
                    usr.is_active=False
                    usr.save()

                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    mess=f'Hello \t{usr.username},\nYour OTP to verify your account for Just Watches is {user_otp}\n Thanks You!'
                    send_mail(
                        "Welcome to Just watches , verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],

                        fail_silently=False


                        )
                    return render(request,'registration/signup.html',{'otp':True,'usr':usr})
                else:
                    context={
                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                        

                    }
                    messages.error(request,'Email already exists')
                    return render(request,'registration/signup.html',context)
            else:
                context={
                        'pre_firstname' :firstname,
                        'pre_lastname':lastname,
                        'pre_username':username,
                        'pre_phone':phone,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2
                        

                    }
                messages.error(request,'passwords mismatch')
                return render(request,'registration/signup.html',context)
    else:

        return render(request,'registration/signup.html')


def validate_username(value):
    if not re.match(r'^[a-zA-Z\s]*$',value):

        return 'Name should only contain alphabets '
    elif value.strip() =='' or value.strip() == " ":
        return 'Name field cannot be empty'
    elif User.objects.filter(username=value).exists():
        return 'Username already exists'
    else:
        return False




def validateemail(email):

    from django.core.validators import validate_email

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validatepassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def user_login(request):

    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')
    
    if  request.user.is_superuser:
        return redirect('dashboard')
    
    if request.method == 'POST':
        usname=request.POST['username']
        passwd=request.POST['password']

        #validation

        if usname.strip() == '' or passwd.strip() == '':
            messages.error(request,"fields can't be blank")
            return redirect('user_login')
        user =authenticate(username=usname,password=passwd)

        if user is not None :

            if user.is_active:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'you account has been blocked')
                return redirect('user_login')

    
        else:
            messages.error(request,'Invalid credentials!!! ')
            return redirect('user_login')

    return render(request,'registration/login.html')
# def mobile_login(request):
#     if request.method == 'POST':
#         get_otp = request.POST.get('otp')

#         if get_otp:
#             phone = request.POST.get('phone')
#             try:
#                 usr = User.objects.get(phone=phone)
#             except User.DoesNotExist:
#                 context = {'pre_phone': phone}
#                 messages.error(request, 'Entereddddd mobile number is not registered')
#                 return render(request, 'registration/mobile_login.html', context)

#             last_otp = Mobile_Otp.objects.filter(user=usr).last()
#             if last_otp is not None and int(get_otp) == last_otp.otp:
#                 usr.is_active = True
#                 usr.save()
#                 login(request, usr)
#                 last_otp.delete()
#                 return redirect('home')
#             else:
#                 messages.warning(request, 'You entered a wrong OTP')
#                 return render(request, 'registration/mobile_login.html')

#         phone = request.POST.get('phone')
#         user = request.user
#         otp = random.randint(100000, 999999)
#         c_phone = '+91' + phone

#         try:
#             user = User.objects.get(phone=int(phone))
#         except User.DoesNotExist:
#             context = {'pre_phone': phone}
#             messages.error(request, 'Entered mobile number is not registered')
#             return render(request, 'registration/mobile_login.html', context)

#         mobile_otp = Mobile_Otp(user=user, otp=otp)
#         mobile_otp.save()
#         mixin.send_otp_on_phone(c_phone,otp)

#         return render(request, 'registration/mobile_login.html', {'otp': True, 'user': user})

#     return render(request, 'registration/mobile_login.html')
def mobile_login(request):
   
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_phone=request.POST.get('phone')
            user=User.objects.get(phone=get_phone)
            if int(get_otp)==Mobile_Otp.objects.filter(user=user).last().otp:
                auth.login(request,user)
                Mobile_Otp.objects.filter(user=user).delete()
                return redirect('home')   
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'registration/mobile_login.html',{'otp':True,'user':user})  
        else:
        
            phone=request.POST['phone']
        
            if phone.strip()=='':
                messages.error(request,'field cannot empty!')
                return redirect('mobile_login')
        
    
            if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phone):   
                messages.error(request,'phone number should only contain numeric!')  
                
                return render(request,'registration/mobile_login.html')
                    
            if User.objects.filter(phone=phone):
                user=User.objects.get(phone=phone)
                user_otp=random.randint(100000,999999)
                Mobile_Otp.objects.create(user=user,otp=user_otp)
                c_phone = '+91' + phone
                mixin.send_otp_on_phone(c_phone,user_otp)
            
                return render (request,'registration/mobile_login.html',{'otp':True,'user':user}) 
            else:
                messages.error(request,'phone  does not exist!')
                return render(request,'registration/mobile_login.html')
    return render (request,'registration/mobile_login.html')  

def forgot_password(request):

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                user = User.objects.get(email = get_email)
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                Pass = validatepassword(password1)
                if password1 == password2:
                    if Pass is False:
                        context ={
                                'pre_otp':get_otp,
                            }
                        messages.info(request,'Enter Strong Password')
                        return render(request,'registration/forgotpassword.html',context)
                    user.set_password(password1)
                    user.save()
                    UserOTP.objects.filter(user=usr).delete()
                    return redirect('user_login')
                else:
                    messages.error(request,"Password dosn't match")
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'registration/forgot.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            email = request.POST['email']
            # null values checking
            check = [email]
            for values in check:
                if values == '':
                    context ={
                       'pre_email':email,
                    }
                    return render(request,'registration/forgot.html',context)
                else:
                    pass

            result = validateemail(email)
            if result is False:
                context ={
                        'pre_email':email,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'registration/forgot.html',context)
            else:
                pass
            
            if User.objects.filter(email = email).exists():
                usr = User.objects.get(email=email) 
                user_otp=random.randint(100000,999999)
                UserOTP.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to verify your account for JUST watches is {user_otp}\nThanks!'
                send_mail(
                        "welcome to JUST watches Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                return render(request,'registration/forgot.html',{'otp':True,'usr':usr})
            else:
                messages.info(request,'You have not an account')
                return render (request, 'registration/forgot.html')
    return render (request, 'registration/forgot.html')



