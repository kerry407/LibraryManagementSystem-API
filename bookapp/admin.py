from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_bestselling"]
    list_filter = ["title", "author"]
    readonly_fields = ["slug"]
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    list_filter = ["first_name", "last_name"]
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["review_user", "rating", "book"]
    list_filter = ["book", "rating"]
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    