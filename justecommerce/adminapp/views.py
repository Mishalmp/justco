from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from categories.models import category


from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout

# verification email
from registrationuser.models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError


# Create your views here.
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Validation
        if username.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('admin_login')

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('dashboard')
            else:
                messages.error(request, "You are not a superuser")
                return redirect('admin_login')

        messages.error(request, "Invalid email or password")
        return redirect('admin_login')

    return render(request, 'adminapp/adminlogin.html')

# validations
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    elif User.objects.filter(username=value).exists():
        return 'Usename already exist'
    else:
        return False
    
def admin_signup(request):
    # OTP VERIFICATION

    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            usr = User.objects.get(email=get_email)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.is_superuser = True
                usr.save()  # Save the changes to the user object
                auth.login(request, usr)
                messages.success(request, f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('dashboard')
            else:
                messages.warning(request, 'You Entered a wrong OTP')
                return render(request, 'adminapp/adminsignup.html', {'otp': True, 'usr': usr})

        # User registration validation
        else:
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Null values checking
            check = [email, password1, password2]
            for value in check:
                if value == '':
                    context = {
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2,
                    }
                    messages.info(request, 'Some fields are empty')
                    return render(request, 'adminapp/adminsignup.html', context)

            result = validateEmail(email)
            if not result:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.info(request, 'Enter a valid email')
                return render(request, 'adminapp/adminsignup.html', context)

            Pass = ValidatePassword(password1)
            if not Pass:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.info(request, 'Enter a strong password')
                return render(request, 'adminapp/adminsignup.html', context)

            if password1 == password2:
                try:
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    usr = User.objects.create_user(username=email, email=email, password=password1)
                    usr.is_active = False
                    usr.is_superuser = True
                    usr.save()
                    
                    user_otp = random.randint(100000, 999999)
                    UserOTP.objects.create(user=usr, otp=user_otp)
                    mess = f'Hello {usr.username},\nYour OTP to verify your account for just is {user_otp}\nThanks!'
                    send_mail(
                        "Welcome to just watches: Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                    return render(request, 'adminapp/adminsignup.html', {'otp': True, 'usr': usr})
                else:
                    context = {
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2,
                    }
                    messages.error(request, 'Email already exists')
                    return render(request, 'adminapp/adminsignup.html', context)
            else:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.error(request, 'Password mismatch')
                return render(request, 'adminapp/adminsignup.html', context)
    else:
        return render(request, 'adminapp/adminsignup.html')



# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='admin_login')
def dashboard(request):

    return render(request,'adminapp/dashboard.html')


@login_required(login_url='admin_login')
def admin_logout(request):

    logout(request)
    return redirect('admin_login')

def user(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    user_data = User.objects.all().order_by('id')
    return render(request,'adminapp/users.html',{'users': user_data})

# Block User
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('user')

# Search User
def searchuser(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users = User.objects.filter(username__icontains=keyword).order_by('id')
            if users.exists():
                context = {
                    'users': users,
                }
                return render(request, 'adminapp/users.html', context)
            else:
                message = "User not found."
                return render(request, 'adminapp/user.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'adminapp/users.html', {'message': message})
    else:
        return render(request, 'error/index.html')






