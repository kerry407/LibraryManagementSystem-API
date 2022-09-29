from rest_framework import serializers 
from bookapp.models import Book, Author, Review, Category


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True, many=True)
    published_countries = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = Book 
        exclude = ["id", "slug"]
    
class AuthorSerializer(serializers.ModelSerializer):
    middle_name = serializers.StringRelatedField(read_only=True)
    books = BookSerializer(many=True, read_only=True)
    # books = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='book-detail', lookup_field='slug') 
    # has_middle_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Author  
        exclude = ["id"]
        
    def get_has_middle_name(self, obj):
        if obj.middle_name:
            return True
        return False 
    
class ReviewSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review 
        exclude = ["id", "book"]
        
    def get_book_title(self, obj):
        return obj.book.title 
    

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category 
        fields = ["name"]
        
        
            
        
    