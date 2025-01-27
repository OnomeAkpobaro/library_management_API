from django.db import models


class Book(models.Model):
    """
    Represents a book in the library

    Has: Genre_Choices, Availability_choices and model attributes
    """


    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Classic Fiction', 'Classic Fiction'),
        ('Thriller', 'Thriller'),
        ('Dystopian', 'Dystopian'),
        ('Memoir', 'Memoir'),
        ('Biography', 'Biography'),
        ('Self-Help', 'Self-Help'),
        ('Cookbook', 'Cookbook'),
        ('Poetry', 'Poetry'),
        ('History', 'History'),
        ('Science', 'Science'),
        ('Math', 'Math'),
        ('Art', 'Art'),
        ('Music', 'Music'),
        ('Film', 'Film'),
        ('Travel', 'Travel'),
        ('Sports', 'Sports'),
        ('Health', 'Health'),
        ('Crafts', 'Crafts'),
        ('Other', 'Other'),
    ]

    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Checked Out', 'Checked Out'),
        ('Lost', 'Lost'),
        ('Damaged', 'Damaged'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    publication_date = models.DateField()
    availability = models.CharField(max_length=100, choices=AVAILABILITY_CHOICES)
    edition = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self):
        return f"{self.title} by {self.author}"     #string representation of the model
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Books'