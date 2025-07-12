from django.db import models
from django.db.models import Avg

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0.0)

    def update_average_rating(self):
        self.average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        self.save()

    def __str__(self):
        return self.name