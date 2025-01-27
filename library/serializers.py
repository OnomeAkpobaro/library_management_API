from rest_framework import serializers
from .models import Book
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_date(self, value):
        """
        Validates publication date
        """
        if value > timezone.now().date():
            raise serializers.ValidationError("Publication date can't be in the future.")
        return value
    
    def validate_edition(self, value):
        """
        Validates book edition
        """
        try:
            value = int(value)
        except ValueError:
            raise ValidationError("Edition must be an interger.")
        if value < 1:
            raise ValidationError("Edition must be at least 1.")
        return value
    
    def validate_title(self, value):
        """
        Validates the book title isnt less than 2 characters
        """
        if len(value) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters.")
        return value
    
    def validate_author(self, value):
        """
        Validates the book author isnt less than 2 characters
        """
        if len(value) < 2:
            raise serializers.ValidationError("Author must be at least 2 characters.")
        return value
    
    def validate_summary(self, value):
        """
        Validates that summary exceeds 10 characters
        """
        if len(value) < 10:
            raise serializers.ValidationError("Summary must be at least 10 characters.")
        return value
    
