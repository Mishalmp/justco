from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from PIL import Image

# # Create your models here.
# class Offer(models.Model):
#     offer_name = models.CharField(max_length=100)
#     discount_amount = models.PositiveIntegerField()
#     start_date = models.DateField(default=timezone.now)  # Use DateField instead of DateTimeField
#     end_date = models.DateField(default=timezone.now)

#     def __str__(self):
#         return self.offer_name

#     def is_offer_expired(self):
#         return timezone.now().date() >= self.end_date