from django.db import models
from django.urls import reverse
from categories.models import category
from django.utils.text import slugify
from justeco.settings import *
# from django_resized import ResizedImageField
# from image_cropping.fields import ImageRatioField, ImageCropField
# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill
# from sorl.thumbnail import ImageField, get_thumbnail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from PIL import Image


# Create your models here.


# Price Filter
class PriceFilter(models.Model):
    FILTER_CHOICES = (
       
       
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
        ('50000 and above', '50000 and above'),
    )
    price_range = models.CharField(choices=FILTER_CHOICES, max_length=60)
    
    def __str__(self):
        return self.price_range
    
class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_amount = models.PositiveIntegerField()
    start_date = models.DateField(default=timezone.now)  # Use DateField instead of DateTimeField
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.offer_name

    def is_offer_expired(self):
        return timezone.now().date() >= self.end_date


# Signal handler to update start_date and end_date before saving the Offer model
# @receiver(pre_save, sender=Offer)
# def update_offer_time(sender, instance, **kwargs):
#     if instance.start_date and instance.end_date:
#         # Ensure the end_date is later than the start_date
#         if instance.start_date >= instance.end_date:
#             raise ValueError("End date must be later than the start date.")
#     else:
#         raise ValueError("Start date and end date must be specified.")


# product
class Product(models.Model):
    from brand.models import Brand

    
    product_name = models.CharField(unique=True,max_length=50)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='photos/product',default='No image available',null=True)
    product_image2 = models.ImageField(upload_to='photos/product',default='No image available',null=True)
    product_image3 = models.ImageField(upload_to='photos/product',default='No image available',null=True)
    
    
    price_range = models.ForeignKey(PriceFilter, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
   
    is_available = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250,unique=True)
    quantity = models.IntegerField(default=10)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True )
    created_at = models.DateTimeField(auto_now_add=True,null=True)

  


    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('single',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    def get_offer(self):
        product_offer = self.offer
        brand_offer = self.brand.offer

        if product_offer and brand_offer:
            # If both product and brand have offers, choose the maximum discount
            max_discount = max(product_offer.discount_amount, brand_offer.discount_amount)
            percentage_discount = (max_discount / 100) * self.product_price

            discounted=self.product_price-percentage_discount
            return discounted
        elif product_offer:
            # If only product has an offer
            percentage_discount = (product_offer.discount_amount / 100) * self.product_price
            discounted=self.product_price-percentage_discount
            return discounted
        elif brand_offer:
            # If only brand has an offer
            percentage_discount = (brand_offer.discount_amount / 100) * self.product_price

            discounted=self.product_price-percentage_discount
            return discounted
        else:
            # If neither product nor brand has an offer, return the original price
            return self.product_price



class ProductReview(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)













class Color(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color

# Variations
class Variations(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    image1 = models.ImageField(upload_to='photos/variations')
    image2 = models.ImageField(upload_to='photos/variations')
    image3 = models.ImageField(upload_to='photos/variations')
    def __str__(self) -> str:
        return f"{self.product, self.color}"
    


