# Service Request API

This API allows users to manage service requests, including creating, updating, deleting, and filtering requests based on service type and status. It also supports file attachments for each service request.

## Endpoints

### 1. Ping
- **URL**: `/api/ping/`
- **Method**: `GET`
- **Description**: Check if the API is running.

### 2. List Service Requests
- **URL**: `/api/service-requests/`
- **Method**: `GET`
- **Description**: Retrieve a list of all service requests.

### 3. Create Service Request
- **URL**: `/api/service-requests/create/`
- **Method**: `POST`
- **Description**: Create a new service request with optional file attachments.

### 4. Get Service Request Details
- **URL**: `/api/service-requests/{id}/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific service request by ID.

### 5. Update Service Request Status
- **URL**: `/api/service-requests/{id}/update-status/`
- **Method**: `PATCH`
- **Description**: Update the status of a specific service request.

### 6. Delete Service Request
- **URL**: `/api/service-requests/{id}/delete/`
- **Method**: `DELETE`
- **Description**: Delete a specific service request by ID.

### 7. Filter Service Requests
- **URL**: `/api/service-requests/filter/`
- **Method**: `GET`
- **Description**: Filter service requests by service type and status.

### 8. Create User
- **URL**: `/api/users/create/`
- **Method**: `POST`
- **Description**: Create a new user.

### 9. Get User Details
- **URL**: `/api/users/{user_id}/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific user by ID, including their service requests.

## Request and Response Examples

### Ping
- **Request**:
  ```http
  GET /api/ping/
  ```
- **Response**:
  ```json
  {
    "message": "pong"
  }
  ```

### List Service Requests
- **Request**:
  ```http
  GET /api/service-requests/
  ```
- **Response**:
  ```json
  [
    {
      "id": 1,
      "service_type": "installation",
      "status": "pending",
      "details": "Need a new gas connection installation",
      "submission_date": "2025-02-12T13:17:42.577223Z",
      "resolution_date": null,
      "status_history": {
        "pending": "2025-02-12T13:17:42.577223Z"
      },
      "attachments": []
    }
  ]
  ```

### Create Service Request
- **Request**:
  ```http
  POST /api/service-requests/create/
  Content-Type: multipart/form-data

  service_type: installation
  details: Need a new gas connection installation
  attachments: [file1]
  attachments: [file2]
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "service_type": "installation",
    "status": "pending",
    "details": "Need a new gas connection installation",
    "submission_date": "2025-02-12T13:17:42.577223Z",
    "resolution_date": null,
    "status_history": {
      "pending": "2025-02-12T13:17:42.577223Z"
    },
    "attachments": [
      {
        "id": 1,
        "file": "attachments/1/file1.jpg",
        "file_url": "http://localhost:8000/media/attachments/1/file1.jpg",
        "uploaded_at": "2025-02-12T13:17:42.577223Z"
      }
    ],
    "message": "Service request created successfully"
  }
  ```

### Get Service Request Details
- **Request**:
  ```http
  GET /api/service-requests/1/
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "service_type": "installation",
    "status": "pending",
    "details": "Need a new gas connection installation",
    "submission_date": "2025-02-12T13:17:42.577223Z",
    "resolution_date": null,
    "status_history": {
      "pending": "2025-02-12T13:17:42.577223Z"
    },
    "attachments": [
      {
        "id": 1,
        "file": "attachments/1/file1.jpg",
        "file_url": "http://localhost:8000/media/attachments/1/file1.jpg",
        "uploaded_at": "2025-02-12T13:17:42.577223Z"
      }
    ]
  }
  ```

### Update Service Request Status
- **Request**:
  ```http
  PATCH /api/service-requests/1/update-status/
  Content-Type: application/json

  {
    "status": "in_progress"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Status updated successfully.",
    "current_status": "in_progress",
    "status_history": {
      "pending": "2025-02-12T13:17:42.577223Z",
      "in_progress": "2025-02-12T14:00:00.000000Z"
    }
  }
  ```

### Filter Service Requests
- **Request**:
  ```http
  GET /api/service-requests/filter/?service_type=installation&status=pending
  ```
- **Response**:
  ```json
  [
    {
      "id": 1,
      "service_type": "installation",
      "status": "pending",
      "details": "Need a new gas connection installation",
      "submission_date": "2025-02-12T13:17:42.577223Z",
      "resolution_date": null,
      "status_history": {
        "pending": "2025-02-12T13:17:42.577223Z"
      },
      "attachments": []
    }
  ]
  ```

### Delete Service Request
- **Request**:
  ```http
  DELETE /api/service-requests/1/delete/
  ```
- **Response**:
  ```json
  {
    "message": "Service request deleted successfully."
  }
  ```

### Create User
- **Request**:
  ```http
  POST /api/users/create/
  Content-Type: application/json

  {
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john.doe@example.com",
    "address": "123 Main Street"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "message": "User created successfully"
  }
  ```

### Get User Details
- **Request**:
  ```http
  GET /api/users/1/
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john.doe@example.com",
    "address": "123 Main Street",
    "service_requests": [
      {
        "id": 1,
        "service_type": "installation",
        "status": "pending",
        "details": "Need a new gas connection installation",
        "submission_date": "2025-02-12T13:17:42.577223Z",
        "resolution_date": null,
        "status_history": {
          "pending": "2025-02-12T13:17:42.577223Z"
        },
        "attachments": []
      }
    ]
  }
  ```

## Postman Documentation

For detailed API documentation, please refer to the [Postman Documentation](https://documenter.getpostman.com/view/29960479/2sAYXCjdbn).


