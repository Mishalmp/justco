from django.db import models
from django.urls import reverse
from categories.models import category
from django.utils.text import slugify

# Create your models here.
class brand(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_image = models.ImageField(upload_to='photos/brand',default='No image available')
  
    brand_discription = models.TextField(max_length=200)
    slug = models.SlugField(max_length=250,unique=True)

    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.brand_name)
        super(brand, self).save(*args, **kwargs)

        def get_url(self):
            return reverse('product_by_brand', args={self.slug} )
    
    def __str__(self):
        return self.brand_name