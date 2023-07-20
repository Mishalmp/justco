from django.db import models

# Create your models here.
class banner(models.Model):
    banner = models.CharField(max_length=200)
    banner_image = models.ImageField(upload_to='photos/brand',default='No image available')
    caption=models.TextField(max_length=200)
  

    def __str__(self):
        return self.banner