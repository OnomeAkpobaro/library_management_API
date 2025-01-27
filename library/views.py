from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
import time

class LibraryPagination(PageNumberPagination):
    """
    Pagination class for books in library
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookRateThrottle(AnonRateThrottle):
    """
    Throttle class 
    """
    rate = '100/minute'

    def get_request_history(self, request, view):
        cache_key = self.get_cache_key(request, view)
        if cache_key:
            return self.cache.get(cache_key, [])
        return []


class BookViewSet(viewsets.ModelViewSet):
    """
    Viewset for the book model
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class  = LibraryPagination
    throttle_classes = [BookRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'author', 'availability']


    def get_throttles(self):
        throttle_class = super().get_throttles()
        for throttle in throttle_class:
            if isinstance(throttle, AnonRateThrottle):
                throttle.rate = '100/minute'
        return throttle_class
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        throttles = self.get_throttles()
        
        if throttles:
            throttle = throttles[0]  # Assume first throttle applies
            history = throttle.get_request_history(request, self)
            num_requests = len(history)

           
            response['X-RateLimit-Limit'] = 100
            response['X-RateLimit-Remaining'] = max(0, 100 - num_requests)
            if history:
                reset_time = history[0] + throttle.duration
            else:
                reset_time = int(time.time()) + 60
            response['X-RateLimit-Reset'] = reset_time
        
        return response

    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.splil(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def list(self, request):
        """
        List of books in the library
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Enters a book into the library
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Book added successfully",
                "book": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "failed",
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        """
        Updates a specific book in the library
        """
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Book updated successfully",
                "book": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "failed",
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        To delete a book in the library
        """
        book = self.get_object()
        book.delete()
        return Response({
            "status": "success",
            "message": "Book deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)





