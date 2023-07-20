from django.shortcuts import render,redirect
from .models import banner
from django.contrib import messages
# Create your views here.


def banners(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    bans = banner.objects.all().order_by('id')
    return render(request, 'banner/banner.html',{'banner' : bans})

def createbanners(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        cname = request.POST.get('banner_name', '')
        eimage = request.FILES.get('banner_image', None)
       
        cdescription = request.POST['banner_discription']

        # Validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('banners')

        if not eimage:
            messages.error(request, "Image not uploaded")
            return redirect('banners')
        
        if banner.objects.filter(banner=cname).exists():
            messages.error(request, 'banner name already exists')
            return redirect('banners')

        ban = banner(
            banner=cname,
            banner_image=eimage,
       
            caption=cdescription,
        )
        ban.save()
        return redirect('banners')

    return render(request, 'banner/banner.html')

def editbanner(request, editbanner_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        cname = request.POST['banner_name']
     
        cdescription = request.POST['banner_discription']
# validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('banners')
        if banner.objects.filter(banner=cname).exists():
            check = banner.objects.get(id = editbanner_id)
            if cname == check.banner:
                pass
            else:
                messages.error(request, 'Banner name already exists')
                return redirect('banners')

        try:
            cat = banner.objects.get(id=editbanner_id)
            eimage = request.FILES['banner_image']
            cat.banner_image = eimage
            cat.save()
        except:
            pass 

        cat = banner.objects.get(id=editbanner_id)
        cat.banner = cname
      
        cat.caption = cdescription
        cat.save()
        return redirect('banners')
    bans = banner.objects.filter(id=editbanner_id)       
    return render(request, 'banner/banner.html', {'banners': bans})

# Delete brand
def deletebanner(request,deletebanner_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    bran = banner.objects.get(id=deletebanner_id)
    bran.delete()
    return redirect('banners')