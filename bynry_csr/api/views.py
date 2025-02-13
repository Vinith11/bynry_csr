from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import ServiceRequest, ServiceRequestAttachment, User
from .serializers import ServiceRequestSerializer, ServiceRequestAttachmentSerializer, UserSerializer
from django.utils import timezone
import shutil
import os
from django.conf import settings

@api_view(['GET'])
def ping(request):
    return Response({"message": "pong"})


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "id": user.id,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_details(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def create_service_request(request):
    required_fields = ['user', 'service_type', 'details']
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"'{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    data = {
        'user': request.data['user'],
        'service_type': request.data['service_type'],
        'details': request.data['details'],
    }
    
    serializer = ServiceRequestSerializer(data=data)
    if serializer.is_valid():
        service_request = serializer.save()  #

        files = request.FILES.getlist('attachments')
        if not files:
            return Response({"error": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        attachments = []
        for file in files:
            attachment = ServiceRequestAttachment.objects.create(
                service_request=service_request,
                file=file
            )
            attachment_serializer = ServiceRequestAttachmentSerializer(attachment, context={'request': request})
            attachments.append(attachment_serializer.data)
        
        updated_serializer = ServiceRequestSerializer(service_request, context={'request': request})
        response_data = updated_serializer.data
        response_data['message'] = "Service request created successfully"
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_service_requests(request):
    requests = ServiceRequest.objects.all()
    serializer = ServiceRequestSerializer(requests, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_service_request_details(request, pk):
    try:
        service_request = ServiceRequest.objects.get(pk=pk)
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ServiceRequestSerializer(service_request, context={'request': request})
    return Response(serializer.data)

@api_view(['PATCH'])
def update_service_request_status(request, pk):
    try:
        service_request = ServiceRequest.objects.get(pk=pk)
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if 'status' not in request.data:
        return Response({"error": "'status' field is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    new_status = request.data['status']
    current_status = service_request.status
    
    if current_status == 'resolved':
        return Response({"error": "Cannot change status of a resolved request."}, status=status.HTTP_400_BAD_REQUEST)
    elif current_status == 'in_progress' and new_status == 'pending':
        return Response({"error": "Cannot change status from in_progress to pending."}, status=status.HTTP_400_BAD_REQUEST)
    elif current_status == 'pending' and new_status not in ['in_progress', 'resolved']:
        return Response({"error": "From pending, status can only change to in_progress or resolved."}, status=status.HTTP_400_BAD_REQUEST)
    elif current_status == 'in_progress' and new_status != 'resolved':
        return Response({"error": "From in_progress, status can only change to resolved."}, status=status.HTTP_400_BAD_REQUEST)
    
    service_request.status = new_status
    service_request.status_history[new_status] = timezone.now().isoformat()

    if new_status == 'resolved':
        service_request.resolution_date = timezone.now()
    
    service_request.save()
    return Response({
        "message": "Status updated successfully.",
        "current_status": service_request.status,
        "status_history": service_request.status_history
    })

@api_view(['DELETE'])
def delete_service_request(request, pk):
    try:
        service_request = ServiceRequest.objects.get(pk=pk)

        folder_path = os.path.join(settings.MEDIA_ROOT, 'attachments', str(pk))
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        service_request.delete()
        return Response({"message": "Service request and associated files deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def filter_service_requests(request):
    service_type = request.query_params.get('service_type', '')
    status = request.query_params.get('status', '')

    if service_type and status:
        requests = ServiceRequest.objects.filter(service_type=service_type, status=status)
    elif service_type:
        requests = ServiceRequest.objects.filter(service_type=service_type)
    elif status:
        requests = ServiceRequest.objects.filter(status=status)
    else:
        requests = ServiceRequest.objects.all()

    serializer = ServiceRequestSerializer(requests, many=True, context={'request': request})
    return Response(serializer.data)