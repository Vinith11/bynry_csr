from django.urls import path
from .views import ping, list_service_requests, create_service_request, get_service_request_details, update_service_request_status, delete_service_request, filter_service_requests, create_user, get_user_details
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ping/', ping),
    path('service-requests/', list_service_requests, name='list_service_requests'),
    path('service-requests/create/', create_service_request, name='create_service_request'),
    path('service-requests/<int:pk>/', get_service_request_details, name='get_service_request_details'),
    path('service-requests/<int:pk>/update-status/', update_service_request_status, name='update_service_request_status'),
    path('service-requests/<int:pk>/delete/', delete_service_request, name='delete_service_request'),
    path('service-requests/filter/', filter_service_requests, name='filter_service_requests'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:user_id>/', get_user_details, name='get_user_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)