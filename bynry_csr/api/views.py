from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from django.utils import timezone

@api_view(['GET'])
def ping(request):
    return Response({"message": "pong"})

@api_view(['POST'])
def create_service_request(request):
    required_fields = ['service_type', 'details']
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"'{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ServiceRequestSerializer(data=request.data)
    if serializer.is_valid():
        service_request = serializer.save()
        return Response({"id": service_request.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_service_requests(request):
    requests = ServiceRequest.objects.all()
    data = [{"id": req.id, "service_type": req.service_type, "status": req.status} for req in requests]
    return Response(data)

@api_view(['GET'])
def get_service_request_details(request, pk):
    try:
        service_request = ServiceRequest.objects.get(pk=pk)
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ServiceRequestSerializer(service_request)
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
    
    # Validate status flow
    if current_status == 'resolved':
        return Response({"error": "Cannot change status of a resolved request."}, status=status.HTTP_400_BAD_REQUEST)
    elif current_status == 'in_progress' and new_status == 'pending':
        return Response({"error": "Cannot change status from in_progress to pending."}, status=status.HTTP_400_BAD_REQUEST)
    elif current_status == 'pending' and new_status not in ['in_progress', 'resolved']:
        return Response({"error": "From pending, status can only change to in_progress or resolved."}, status=status.HTTP_400_BAD_REQUEST)
    elif current_status == 'in_progress' and new_status != 'resolved':
        return Response({"error": "From in_progress, status can only change to resolved."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update status and status history
    service_request.status = new_status
    service_request.status_history[new_status] = timezone.now().isoformat()
    
    # Set resolution date if status is changed to resolved
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
        service_request.delete()
        return Response({"message": "Service request deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)