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

    def get_paginated_response(self, data):
        return Response({
            "books": data,
            "status": "success",
            "message": "Books retrieved successfully",
            "pagination": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count
            }
        })

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
    pagination_class = LibraryPagination
    throttle_classes = [BookRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'author', 'availability']

    def get_headers_info(self, request):
        """Get rate limit header information"""
        throttles = self.get_throttles()
        if throttles:
            throttle = throttles[0]
            history = throttle.get_request_history(request, self)
            num_requests = len(history)
            
            if history:
                reset_time = int(history[0] + throttle.duration)
            else:
                reset_time = int(time.time() + 60)

            return {
                "X-RateLimit-Limit": 100,
                "X-RateLimit-Remaining": max(0, 100 - num_requests),
                "X-RateLimit-Reset": reset_time
            }
        return {}

    def finalize_response(self, request, response, *args, **kwargs):
        """Add headers to HTTP response"""
        response = super().finalize_response(request, response, *args, **kwargs)
        headers = self.get_headers_info(request)
        
        # Set HTTP headers
        for key, value in headers.items():
            response[key] = value

        # Add headers to response data
        if hasattr(response, 'data') and isinstance(response.data, dict):
            if not response.data.get('headers'):
                response.data['headers'] = headers

        return response

    def list(self, request):
        """List all books"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "books": serializer.data,
            "status": "success",
            "message": "Books retrieved successfully",
            "headers": self.get_headers_info(request)
        })

    def retrieve(self, request, pk=None):
        """Get a single book"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "book": serializer.data,
            "status": "success",
            "message": "Book details retrieved successfully",
            "headers": self.get_headers_info(request)
        })

    def create(self, request):
        """Create a new book"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "book": serializer.data,
                "status": "success",
                "message": "Book created successfully",
                "headers": self.get_headers_info(request)
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "failed",
            "message": "Invalid data provided",
            "errors": serializer.errors,
            "headers": self.get_headers_info(request)
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update a book"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "book": serializer.data,
                "status": "success",
                "message": "Book updated successfully",
                "headers": self.get_headers_info(request)
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "failed",
            "message": "Invalid data provided",
            "errors": serializer.errors,
            "headers": self.get_headers_info(request)
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a book"""
        instance = self.get_object()
        instance.delete()
        return Response({
            "status": "success",
            "message": "Book deleted successfully",
            "headers": self.get_headers_info(request)
        }, status=status.HTTP_204_NO_CONTENT)

# class LibraryPagination(PageNumberPagination):
#     """
#     Pagination class for books in library
#     """
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 100

#     def get_paginated_response(self, data):
#         return Response({
#             "books": data,
#             "status": "success",
#             "message": "Books retrieved successfully",
#             "pagination": {
#                 "next": self.get_next_link(),
#                 "previous": self.get_previous_link(),
#                 "count": self.page.paginator.count
#             }
#         })


# class BookRateThrottle(AnonRateThrottle):
#     """
#     Throttle class 
#     """
#     rate = '100/minute'

    # def get_request_history(self, request, view):
    #     cache_key = self.get_cache_key(request, view)
    #     if cache_key:
    #         return self.cache.get(cache_key, [])
    #     return []


# class BookViewSet(viewsets.ModelViewSet):
#     """
#     Viewset for the book model
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     pagination_class  = LibraryPagination
#     throttle_classes = [BookRateThrottle]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['genre', 'author', 'availability']


#     def get_throttles(self):
#         throttle_class = super().get_throttles()
#         for throttle in throttle_class:
#             if isinstance(throttle, AnonRateThrottle):
#                 throttle.rate = '100/minute'
#         return throttle_class
    
#     def finalize_response(self, request, response, *args, **kwargs):
#         response = super().finalize_response(request, response, *args, **kwargs)
#         throttles = self.get_throttles()
#         headers = {}
        
#         if throttles:
#             throttle = throttles[0]  # Assume first throttle applies
#             history = throttle.get_request_history(request, self)
#             num_requests = len(history)

           
#             if history:
#                 reset_time = history[0] + throttle.duration
#             else:
#                 reset_time = int(time.time()) + 60
#             headers = {
#                 "X-RateLimit-Limit": 100,
#                 "X-RateLimit-Remaining": max(0, 100 - num_requests),
#                 "X-RateLimit-Reset": reset_time
#             }

#             for key, value in headers.items():
#                 response[key] = value
        
#         if hasattr(response, 'data'):
#             if isinstance(response.data, dict):
#                 if 'book' in response.data:
#                     #add header
#                     response.data['headers'] = headers
#                 elif 'books' in response.data:
#                     response.data['headers'] = headers
#                 else:
#                     response.data = {
#                         "book": response.data,
#                         "status": "success",
#                         "message": self._get_success_message(request.method),
#                         "headers": headers
#                     }
#             elif isinstance(response.data, list):
#                 response.data = {
#                     "books": response.data,
#                     "status": "success",
#                     "message": self._get_success_message(request.method),
#                     "headers": headers
#                 }

#         return response     
#     def _get_success_message(self, method):
#         """
#         Returnn appropriate success messagesb based on the HTTP method
#         """   
#         messages = {
#             "GET": "Book details retrieved successfully",
#             "POST": "Book created successfully",
#             "PUT": "Book updated successfully",
#             "PATCH:": "Book updated successfully",
#             "DELETE": "Book deleted successfully"
#         }
#         return messages.get(method, 'Operation Successful')

    
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.splil(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip


#     def list(self, request):
#         """
#         List of books in the library
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)

#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
        
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def create(self, request):
#         """
#         Enters a book into the library
#         """
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status": "success",
#                 "message": "Book added successfully",
#                 "book": serializer.data
#             }, status=status.HTTP_201_CREATED)
        
#         return Response({
#             "status": "failed",
#             "message": "Invalid data provided",
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
        
#     def update(self, request, pk=None):
#         """
#         Updates a specific book in the library
#         """
#         book = self.get_object()
#         serializer = self.get_serializer(book, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status": "success",
#                 "message": "Book updated successfully",
#                 "book": serializer.data
#             }, status=status.HTTP_200_OK)
        
#         return Response({
#             "status": "failed",
#             "message": "Invalid data provided",
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk=None):
#         """
#         To delete a book in the library
#         """
#         book = self.get_object()
#         book.delete()
#         return Response({
#             "status": "success",
#             "message": "Book deleted successfully"
#         }, status=status.HTTP_204_NO_CONTENT)





