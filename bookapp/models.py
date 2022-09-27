from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.contrib.auth.models import User 
# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Author: {self.first_name} {self.last_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return f"{self.name} {self.code}"
    

class Book(models.Model):

    """
    In the slugfield, using the db_index makes it very easy and 
    fast to lookup or search for data in that field. Bu only set db_index 
    to fields you would use most often because setting db_index to every
    field makes it slower because of load.
    """
    title = models.CharField(max_length=70)
    average_rating = models.FloatField(
                    validators=[MinValueValidator(0),
                                MaxValueValidator(5)
                                ], default=0)
    no_reviews = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
    published_countries = models.ManyToManyField(Country)
    category = models.ManyToManyField(Category)
    is_bestselling = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(default='', null=False, db_index=True, editable=False)
    
    class Meta:
        ordering = ["id"]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return f"Title: {self.title},  Author: {self.author}"


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    body = models.TextField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return f"Review by {self.review_user.username} on {self.book.title}"
    
    
    
    