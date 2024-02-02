from django.shortcuts import render,redirect
from products.models import Product,ProductReview

from wishlist.models import Wishlist
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from cart.models import Cart,Buynow
# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser

def product_detail(request, product_id):
    try:
        prod = Product.objects.get(slug=product_id)
    except Product.DoesNotExist:
        return redirect('shop')

    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, pk=prod_id)
        product_quantity = prod.quantity
        return JsonResponse({'product_id': product.id, 'product_quantity': product_quantity})

    related = Product.objects.all()
    cart = None  # Set cart as None by default
    buy=None
    product = get_object_or_404(Product, slug=product_id)
    recently_viewed_products = request.session.get('recently_viewed_products', [])

    if product.id in recently_viewed_products:
        recently_viewed_products.remove(product.id)
    recently_viewed_products.insert(0, product.id)

    # Limit the list to store only the last 5 viewed products
    recently_viewed_products = recently_viewed_products[:4]

    # Update the session variable with the updated list
    request.session['recently_viewed_products'] = recently_viewed_products

    reviews = ProductReview.objects.filter(product_id=product.id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    rev_count=ProductReview.objects.filter(product_id=product.id).count()
    # Check if the user is authenticated and not anonymous
    if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
        cart = Cart.objects.filter(user=request.user, product=prod)
        buy=Buynow.objects.filter(user=request.user, product=prod)

    context = {
        'allpro': related,
        'pro_detail': prod,
        'cart': cart,
        'buy':buy,
        'reviews':reviews,
        'average_rating':average_rating ,
        'rev_count':rev_count
    }
    
    return render(request, 'product-detail.html', context)



# def add_buynow(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
           
#             prod_id = request.POST.get('prod_id')
#             add_qty= int(request.POST.get('add_qty'))
#             try:
#                 product_check = Product.objects.get(id=prod_id)
                

#             except Product.DoesNotExist:
#                 return JsonResponse({'status': 'No such product found'})
            
           
        
#             prod_qty = add_qty
            
#             if product_check.quantity >= prod_qty:
#                 Buynow.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                
#                 return JsonResponse({'status': 'Product added successfully'})
#             else:
#                 return JsonResponse({'status': "Only few quantity available"})
#         else:
#             return JsonResponse({'status': 'Login to continue'})
#     return redirect('product_detail')




def add_buynow(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
           
            prod_id = request.POST.get('prod_id')
            add_qty= int(request.POST.get('add_qty'))
            try:
                product_check = Product.objects.get(id=prod_id)
                

            except Product.DoesNotExist:
                return JsonResponse({'status': 'No such product found'})

            if Buynow.objects.filter(user=request.user, product_id=prod_id).exists():
                prod_qty = int(request.POST.get('product_qty'))
                if product_check.quantity > prod_qty:
                    Buynow.objects.filter(user=request.user, product_id=prod_id).update(product_qty=prod_qty + add_qty)
                    return JsonResponse({'status': 'Product quantity increased'})
                else:
                    return JsonResponse({'status': "Only few quantity available"})

            else:
                prod_qty = add_qty
                
                if product_check.quantity >= prod_qty:
                    Buynow.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                 
                    return JsonResponse({'status': 'Product added successfully'})
                else:
                    return JsonResponse({'status': "Only few quantity available"})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('product_detail')



def add_review(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = int(request.POST.get('rating'))
            review_text = request.POST.get('review')
            name = request.POST.get('name')
            email = request.POST.get('email')
            product_id = request.POST.get('product_id')

            print(rating,review_text,name,email,product_id,'111111111111')

            # Get the product instance based on the product_id
            product = get_object_or_404(Product, id=product_id)

            if rating == 0:
                return JsonResponse({'status': 'Please Select Stars'})
          




            if request.user.email == email:
            # Create and save the product review associated with the product
                review = ProductReview.objects.create(
                product=product,
                rating=rating,
                review_text=review_text,
                name=name,
                email=email
            )
                return JsonResponse({'status': 'Review added successfully'})
            else:
                return JsonResponse({'status': 'Invalid email! Please log in with the correct email'})
    

           

    
        else:
            return JsonResponse({'status': 'Login to continue'})
    
    # If the request method is not POST, return an error response
    return JsonResponse({'error': 'Invalid request method'}, status=400)