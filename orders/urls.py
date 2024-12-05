from django.urls import path
from .views import blog_list_view ,blog_detail_view

from .views import LoginView, LogoutView , MilkOrderView , NotificationView , OrderHistoryView , OrderHistoryListView , UserProfileView ,BlogListView, BlogCreateView ,BlogDetailView 


urlpatterns = [
    # Login endpoint for users to authenticate and receive a token
    path('login/', LoginView.as_view(), name='login'),

    # Logout endpoint for users to delete their token and log out
    path('logout/', LogoutView.as_view(), name='logout'),

# Milk Order view (POST for placing an order, GET for retrieving orders)
    path('orders/', MilkOrderView.as_view(), name='milk_order'),
    
    # Order History view (GET to view all past orders)
    path('orders/history/', OrderHistoryView.as_view(), name='order_history'),

     path('orders/notification/', NotificationView.as_view(), name='notification_order'),

    path('orderfilter/', OrderHistoryListView.as_view(), name='Order_History'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # path('blogs/', BlogListView.as_view(), name='blog-list'),      # List all blogs


    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),  # Admin-only blog creation
    
    # path('blogss/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),

    path('blogs/',blog_list_view, name='blog-list-template'),

    path('blogs/<int:blog_id>/', blog_detail_view, name='blog-detail-template'),


]
