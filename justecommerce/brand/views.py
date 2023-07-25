from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from categories.models import category
from .models import Brand
from products.models import Offer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# .......................brand....................................
@login_required(login_url='admin_login')
def brands(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    brand_data = Brand.objects.all().order_by('id')
    
    return render(request, 'brand/brand.html',{'brand' : brand_data,'offer' : Offer.objects.all(),})

# Create brand
@login_required(login_url='admin_login')
def createbrands(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        cname = request.POST.get('brand_name', '')
        eimage = request.FILES.get('brand_image', None)
       
        cdescription = request.POST['brand_discription']
        offer = request.POST.get('offer')
        if offer == 'No offer':
            offer_id = None
        else:
            offer_id = Offer.objects.get(id=offer)
        # Validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('brands')

        if not eimage:
            messages.error(request, "Image not uploaded")
            return redirect('brands')
        
        if Brand.objects.filter(brand_name=cname).exists():
            messages.error(request, 'brand name already exists')
            return redirect('brands')

        bran = Brand(
            brand_name=cname,
            brand_image=eimage,
       
            brand_discription=cdescription,
            offer = offer_id
        )
        bran.save()
        return redirect('brands')

    return render(request, 'brand/brand.html')


# Edit Brand
@login_required(login_url='admin_login')
def editbrands(request, editbrands_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        cname = request.POST['brand_name']
     
        cdescription = request.POST['brand_discription']
        offer = request.POST.get('offer')
        if offer == 'No offer':
            offer_id = None
        else:
            offer_id = Offer.objects.get(id=offer)
# validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('brands')
        if Brand.objects.filter(brand_name=cname).exists():
            check = Brand.objects.get(slug = editbrands_id)
            if cname == check.brand_name:
                pass
            else:
                messages.error(request, 'Brand name already exists')
                return redirect('brands')

        try:
            cat = Brand.objects.get(slug=editbrands_id)
            eimage = request.FILES['brand_image']
            cat.brand_image = eimage
            cat.save()
        except:
            pass 

        cat = Brand.objects.get(slug=editbrands_id)
        cat.brand_name = cname
      
        cat.brand_discription = cdescription
        cat.offer = offer_id
        cat.save()
        return redirect('brands')
    cate = Brand.objects.filter(slug=editbrands_id)       
    return render(request, 'brand/editbrands.html', {'catego': cate})

# Delete brand
def deletebrands(request,deletebrands_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    bran = Brand.objects.get(id=deletebrands_id)
    bran.delete()
    return redirect('brands')

#search brand
@login_required(login_url='admin_login')
def search_brand(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            brand = Brand.objects.filter(brand_name__icontains=keyword).order_by('id')
            if brand.exists():
                context = {
                    'brand': brand,
                }
                return render(request, 'brand/brand.html', context)
            else:
                message = "Brand not found."
                return render(request, 'brand/brand.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'brand/brand.html', {'message': message})
    else:
        return render(request, 'error/index.html')