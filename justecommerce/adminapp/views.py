from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from categories.models import category
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.db.models import Sum,Count,Q
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
from checkout.models import Order
from checkout.models import OrderItem
# verification email
from registrationuser.models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError
import csv
import io
from products.models import Product,Offer
from collections import Counter
import datetime
from datetime import datetime, date
from datetime import datetime, timedelta
from brand.models import Brand
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
# from offer.models import Offer
from categories.models import category as Category
from django.db.models.functions import TruncMonth
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
    total_profit = Order.objects.aggregate(total_profit=Sum('total_price'))['total_profit'] or 0

    # Count total orders
    total_orders = Order.objects.count()

    # Count total users
    total_users = User.objects.count()
    brands = Brand.objects.all()

    # Count total products
    total_products = Product.objects.count()
    categories = Category.objects.all()

    order_status_data = Order.objects.filter(Q(od_status='Cancelled') | Q(od_status='Return')).aggregate(total_price=Sum('total_price'))
    cancelled_return_price = order_status_data['total_price'] or 0

    # Calculate the sum of prices for all other orders
    other_orders_price = Order.objects.exclude(Q(od_status='Cancelled') | Q(od_status='Return')).aggregate(total_price=Sum('total_price'))['total_price'] or 0


    # Initialize lists to store category names and sales data
    category_names = []
    category_sales_data = []  # Renamed to avoid conflicts

    # Loop through each category and calculate the total sales
    for category in categories:
        total_sales = Product.objects.filter(category=category).aggregate(total_sales=Sum('orderitem__price'))['total_sales'] or 0
        category_names.append(category.categories)
        category_sales_data.append(total_sales)  # Renamed to avoid conflicts
  
    pro = Product.objects.all()[:5]
    payment_mode_counts = Order.objects.values('payment_mode').annotate(count=Count('id'))

    # Extract the labels and data for the chart
    labels = [pm['payment_mode'] for pm in payment_mode_counts]
    data = [pm['count'] for pm in payment_mode_counts]
    
    order_status_counts = Order.objects.values('od_status').annotate(count=Count('id'))

    # Extract the labels and data for the pie chart
    status_labels = [status['od_status'] for status in order_status_counts]
    status_data = [status['count'] for status in order_status_counts]

    sales_data = Order.objects.values('created_at').annotate(total_sales=Sum('total_price'))

    # Separate the dates and total sales into two lists for the chart
    dates = [data['created_at'].strftime('%Y-%m-%d') for data in sales_data]
    total_sales = [data['total_sales'] for data in sales_data]

    today = datetime.today().date()
    last_week_start = today - timedelta(days=7)
    last_week_end = today - timedelta(days=1)
    last_week_profit = Order.objects.filter(created_at__range=(last_week_start, last_week_end)).aggregate(last_week_profit=Sum('total_price'))['last_week_profit'] or 0

     # Calculate monthly income
 
    # Retrieve product names for the graph
    products = Product.objects.all()

    order_items=OrderItem.objects.all()

    product_sales_counter = Counter(item.product for item in order_items)
    top_5_selling_products = product_sales_counter.most_common(5)
    top_selling_products_data = [{
        'product_name': product.product_name,
        'sales_quantity': sales_quantity,
    } for product, sales_quantity in top_5_selling_products]

    context = {
        'total_profit': total_profit,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'last_week_profit': last_week_profit,
        'products': products,
        'brands': brands,
        'pro': pro,
        'labels': labels,
        'data': data,
        'status_labels': status_labels,
        'status_data': status_data,
        'category_names': category_names,
        'category_sales_data': category_sales_data,  # Renamed to avoid conflicts
        'dates': dates,
        'total_sales': total_sales,
        'cancelled_return_price':cancelled_return_price,
        'other_orders_price':other_orders_price,
        'top_selling_products_data': top_selling_products_data,

      
    }

    return render(request, 'adminapp/dashboard.html', context)




@login_required(login_url='admin_login')
def sales_report(request):

    if 'all_sales' in request.GET:
        # Get all orders without specifying a date range
        orders = Order.objects.all()
    else:
    # Handle form submission
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            # Filter orders based on the selected date range
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date > end_date:
                messages.error(request, "Start date must be before end date.")
                return redirect('sales_report')
            if end_date > date.today():
                messages.error(request, "End date cannot be in the future.")
                return redirect('sales_report')

            orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
            recent_orders = orders.order_by('-created_at')
        else:
            # If no date range is selected, fetch recent 10 orders
            recent_orders = Order.objects.order_by('-created_at')[:10]
            orders = Order.objects.all()
  
    # Calculate total sales and total orders
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    # Calculate sales by status
    sales_by_status = {
        'Pending': orders.filter(od_status='Pending').count(),
        'Processing': orders.filter(od_status='Processing').count(),
        'Shipped': orders.filter(od_status='Shipped').count(),
        'Delivered': orders.filter(od_status='Delivered').count(),
        'Cancelled': orders.filter(od_status='Cancelled').count(),
        'Return': orders.filter(od_status='Return').count(),
    }

    # Prepare data for CSV export
    csv_data = [
        ['Order ID', 'Tracking Number', 'Total Price', 'Status', 'Created At']
    ]
    for order in orders:
        csv_data.append([order.id, order.tracking_no, order.total_price, order.od_status, order.created_at])

    # Handle CSV export
    if 'export_csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date}_{end_date}.csv"'

        writer = csv.writer(response)
        for row in csv_data:
            writer.writerow(row)

        return response

    # Prepare data for rendering the template
    sales_report = {
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_status': sales_by_status,
        'recent_orders': recent_orders,
    }

    return render(request, 'adminapp/sales_report.html', {'sales_report': sales_report})







import csv
from itertools import groupby
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no', 'Orderd at', 'product_name', 'product_price', 'product_quantity'])

    orders = Order.objects.all()
    for order in orders:
        order_items = OrderItem.objects.filter(order=order).select_related('product')  # Use select_related to optimize DB queries
        grouped_order_items = groupby(order_items, key=lambda x: x.order_id)
        for order_id, items_group in grouped_order_items:
            items_list = list(items_group)
            for order_item in items_list:
                writer.writerow([
                    order.user if order_item == items_list[0] else "",
                    order.total_price if order_item == items_list[0] else "",
                    order.payment_mode if order_item == items_list[0] else "",
                    order.tracking_no if order_item == items_list[0] else "",
                    order.created_at if order_item == items_list[0] else "",  # Only include date in the first row
                    order_item.product.product_name,  # Replace 'product_name' with the actual attribute in your Product model
                    order_item.price,
                    order_item.quantity,
                ])

    return response





def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.pdf'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    styles = getSampleStyleSheet()

    # Header Information
    elements.append(Paragraph('Order Details Report', styles['Heading1']))
    elements.append(Paragraph(str(datetime.now()), styles['Normal']))

    # Table Data
    data = [['User', 'Total Price', 'Payment Mode', 'Tracking No', 'Ordered At', 'Product Name', 'Product Price', 'Product Quantity']]

    orders = Order.objects.all()
    for order in orders:
        order_items = OrderItem.objects.filter(order=order).select_related('product')
        for order_item in order_items:
            data.append([
                order.user.username if order_item == order_items[0] else "",
                order.total_price if order_item == order_items[0] else "",
                order.payment_mode if order_item == order_items[0] else "",
                order.tracking_no if order_item == order_items[0] else "",
                str(order.created_at.date()) if order_item == order_items[0] else "",
                order_item.product.product_name,
                order_item.price,
                order_item.quantity,
            ])

    # Create Table
    table = Table(data, hAlign='CENTER')
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), 'grey'),
                               ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), 'beige'),
                               ('GRID', (0, 0), (-1, -1), 1, 'black')]))

    elements.append(table)
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response







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
@login_required(login_url='admin_login')
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
@login_required(login_url='admin_login')
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






