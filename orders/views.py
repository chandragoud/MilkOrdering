from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import MilkOrder, Notification
from .serializers import MilkOrderSerializer, NotificationSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import generics
from django.utils.dateparse import parse_date
from django.db.models import Q

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Login view to generate token
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Logout view to delete token and log out user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token to log out
            request.user.auth_token.delete()
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({'detail': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)


class MilkOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user.id  # Associate order with the logged-in user
        serializer = MilkOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Create a notification
            Notification.objects.create(
                user=request.user,
                message=f"Milk order placed successfully for {serializer.data['timeslot']} slot.",
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        orders = MilkOrder.objects.filter(user=request.user)
        serializer = MilkOrderSerializer(orders, many=True)
        return Response(serializer.data)

class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the order history for the logged-in user
        orders = MilkOrder.objects.filter(user=request.user).order_by('-created_at')
        serializer = MilkOrderSerializer(orders, many=True)
        return Response(serializer.data)
    

from django.utils.dateparse import parse_datetime

class OrderHistoryListView(generics.ListAPIView):
    serializer_class = MilkOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = MilkOrder.objects.filter(user=user).order_by('-order_date')

        # Filter by order type (Morning/Evening)
        order_type = self.request.query_params.get('order_type')
        if order_type:
            queryset = queryset.filter(order_type=order_type)

        # Filter by start and end date
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(order_date__gte=parse_datetime(start_date))
        if end_date:
            queryset = queryset.filter(order_date__lte=parse_datetime(end_date))

        return queryset


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure the profile being retrieved or updated belongs to the authenticated user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


from rest_framework import generics, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer

# View to list all blogs
class BlogListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view blogs

# View to allow only admin users to create blogs
class BlogCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can create blogs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view a blog's details


from django.shortcuts import render
from .models import BlogPost



def blog_list_view(request):
        blogs = BlogPost.objects.all().order_by('-created_at')
        return render(request, 'orders/blog_list.html', {'blogs': blogs})


from django.shortcuts import render
from .models import BlogPost
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import BlogPostSerializer
from django.shortcuts import render, get_object_or_404
from .models import BlogPost

# View to display an individual blog post
def blog_detail_view(request, blog_id):
    """
    Displays the details of a specific blog post based on its ID.
    """
    blog = get_object_or_404(BlogPost, id=blog_id)  # Fetch the blog post or 404 if not found
    return render(request, 'orders/blog_detail.html', {'blog': blog})



