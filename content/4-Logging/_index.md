---
title : "Session Logs Management"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 4. </b> "
---

# 4. Session Logs Management

This section presents how **Session Logs** are managed in the **Smart Parking IoT System**. Session Logs are used to record the activities of ESP32 devices, Web/App, API Gateway, Lambda, and related AWS services during each data processing session.

Unlike general system logs, which mainly record errors or execution status, Session Logs focus on tracking a specific activity session, such as:

- One time the ESP32 Camera captures and uploads a vehicle image.
- One time the ESP32 sensor sends parking slot status.
- One time a user logs in to the Web/App.
- One time the Web/App calls an API to retrieve parking data.
- One time Lambda processes data and stores the result in DynamoDB.

Managing Session Logs helps administrators check processing flows, detect errors, trace data, and evaluate system stability.

---

## 4.1. Session Logs Overview

Session Logs are records that describe the activities of a session in the system. A session can start when a device or user sends a request to the system and ends when the data is fully processed.

In the Parking IoT system, Session Logs can be divided into three main groups:

| Session Log Type | Description |
| :--- | :--- |
| Device Session Logs | Record activities of ESP32 Camera and ESP32 sensors |
| User Session Logs | Record user login and actions on the Web/App |
| API Session Logs | Record requests, responses, and errors from API Gateway and Lambda |

Example of an ESP32 Camera session:

```text
ESP32 Camera captures image → Requests Presigned URL → Uploads image to S3 → Lambda processes image → Stores result in DynamoDB
```

Example of a user session:

```text
User logs in → Cognito authenticates → Web/App calls API → Lambda queries DynamoDB → Data is returned to the interface
```

Each session should have a unique identifier called `session_id` to make it easier to trace the entire processing flow.

Example Session Log structure:

```json
{
  "session_id": "SESSION001",
  "source": "esp32_camera",
  "action": "upload_image",
  "status": "success",
  "start_time": "2026-04-27T10:30:00",
  "end_time": "2026-04-27T10:30:05",
  "message": "Image uploaded and processed successfully"
}
```

---

## 4.2. Collecting Logs from ESP32 Devices

ESP32 devices are important data sources of the system. Therefore, logs from ESP32 Camera and ESP32 sensors should be collected to check whether the devices operate correctly.

### 4.2.1. Logs from ESP32 Camera

ESP32 Camera needs to record information during the image capture and upload process to Amazon S3.

Processing flow:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

Information that should be logged:

- ESP32 Camera device ID.
- Image capture time.
- Camera location: entrance or exit gate.
- API Gateway request status.
- Presigned URL receiving status.
- Image upload status to S3.
- Image file name.
- Error message if the upload fails.

Example ESP32 Camera log:

```json
{
  "session_id": "CAM_SESSION_001",
  "device_id": "esp32_cam_01",
  "device_type": "camera",
  "gate": "entrance",
  "action": "upload_image",
  "image_name": "esp32_cam_01_20260427_103000.jpg",
  "status": "success",
  "timestamp": "2026-04-27T10:30:00"
}
```

Example error log:

```json
{
  "session_id": "CAM_SESSION_002",
  "device_id": "esp32_cam_01",
  "device_type": "camera",
  "action": "upload_image",
  "status": "failed",
  "error_message": "Failed to get Presigned URL",
  "timestamp": "2026-04-27T10:35:00"
}
```

### 4.2.2. Logs from ESP32 Sensors

ESP32 sensors send parking slot status data to AWS IoT Core through MQTT. Session Logs help check whether the device sends data to the correct topic, with the correct format, and at the correct time.

Processing flow:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Information that should be logged:

- Sensor device ID.
- Parking slot ID.
- Parking slot status: `available` or `occupied`.
- MQTT topic.
- Data sending time.
- Sending status.
- WiFi or MQTT connection errors if any.

Example ESP32 sensor log:

```json
{
  "session_id": "SENSOR_SESSION_001",
  "device_id": "esp32_sensor_01",
  "device_type": "sensor",
  "slot_id": "A01",
  "mqtt_topic": "parking/slot/A01/status",
  "status_value": "occupied",
  "send_status": "success",
  "timestamp": "2026-04-27T10:30:00"
}
```

Example error log:

```json
{
  "session_id": "SENSOR_SESSION_002",
  "device_id": "esp32_sensor_01",
  "device_type": "sensor",
  "slot_id": "A01",
  "send_status": "failed",
  "error_message": "MQTT publish failed",
  "timestamp": "2026-04-27T10:32:00"
}
```

---

## 4.3. Collecting Logs from Web/App and API Gateway

Besides ESP32 devices, the system also needs to record logs from the Web/App and API Gateway to monitor user access and API communication.

### 4.3.1. Logs from Web/App

The Web/App is where users log in, view parking status, search license plates, and check vehicle entry and exit history.

Information that should be logged:

- User ID.
- Login time.
- Accessed function.
- Called API endpoint.
- Request status.
- Displayed error if any.
- Response time.

Example User Session Log:

```json
{
  "session_id": "USER_SESSION_001",
  "user_id": "manager01",
  "role": "Manager",
  "action": "view_parking_slots",
  "api_endpoint": "/parking/slots",
  "status": "success",
  "timestamp": "2026-04-27T10:40:00"
}
```

Example log when a user searches for a license plate:

```json
{
  "session_id": "USER_SESSION_002",
  "user_id": "manager01",
  "action": "search_vehicle",
  "plate_number": "51A-12345",
  "api_endpoint": "/vehicle/search",
  "status": "success",
  "timestamp": "2026-04-27T10:42:00"
}
```

### 4.3.2. Logs from API Gateway

API Gateway is the communication gateway between the Web/App, ESP32 Camera, and Lambda Backend. API Gateway logs help check whether requests reach the correct endpoint and whether the backend returns correct responses.

Information that should be logged:

- HTTP method.
- API endpoint.
- Request ID.
- Status code.
- Response time.
- Request source or IP if needed.
- 4xx or 5xx errors.

Example API Gateway log:

```json
{
  "request_id": "REQ001",
  "session_id": "USER_SESSION_001",
  "method": "GET",
  "endpoint": "/parking/slots",
  "status_code": 200,
  "response_time_ms": 120,
  "timestamp": "2026-04-27T10:40:01"
}
```

Example API error log:

```json
{
  "request_id": "REQ002",
  "session_id": "USER_SESSION_003",
  "method": "GET",
  "endpoint": "/vehicle/logs",
  "status_code": 401,
  "error_message": "Unauthorized request",
  "timestamp": "2026-04-27T10:45:00"
}
```

---

## 4.4. Storing and Querying Session Logs

After being collected, Session Logs need to be stored for checking, querying, and analysis. In the Parking IoT system, **Amazon CloudWatch Logs, Amazon DynamoDB, and Amazon S3** can be used together.

### 4.4.1. Storing Session Logs in CloudWatch Logs

CloudWatch Logs is used to store execution logs from Lambda, API Gateway, and system errors.

Log storage flow:

```text
API Gateway / Lambda / IoT Rule → CloudWatch Logs
```

CloudWatch Logs is suitable for:

- Checking Lambda errors.
- Viewing API Gateway requests.
- Monitoring payloads from IoT Core.
- Tracing errors when the system behaves abnormally.

Example log checking flow:

```text
CloudWatch → Log Groups → Select Lambda Function → View Log Stream
```

### 4.4.2. Storing Session Logs in DynamoDB

DynamoDB can be used to store important Session Logs that need to be queried quickly on the Web/App or admin dashboard.

Example `SessionLogs` table:

| Attribute | Description |
| :--- | :--- |
| session_id | Session identifier |
| source | Log source: ESP32, Web/App, API Gateway |
| action | Performed action |
| status | Processing status |
| timestamp | Log time |
| error_message | Error message if any |

Example data in the `SessionLogs` table:

```json
{
  "session_id": "SESSION001",
  "source": "api_gateway",
  "action": "get_parking_slots",
  "status": "success",
  "timestamp": "2026-04-27T10:40:00",
  "response_time_ms": 120
}
```

### 4.4.3. Long-term Storage in Amazon S3

Amazon S3 can be used for long-term log storage, especially for old logs that do not need frequent querying.

Example S3 log storage structure:

```text
parking-session-logs/
├── 2026/
│   ├── 04/
│   │   ├── 27/
│   │   │   ├── device-logs.json
│   │   │   ├── user-logs.json
│   │   │   └── api-logs.json
```

Storing logs in S3 provides several benefits:

- Reduces long-term log storage costs.
- Supports data backup.
- Allows querying with Athena if needed.
- Suitable for reports and post-demo checking.

---

## 4.5. Analyzing Session Logs

After Session Logs are stored, the system can use them to analyze activities and detect errors.

### 4.5.1. Device Activity Analysis

Session Logs help administrators understand whether ESP32 devices operate stably.

Metrics that can be analyzed:

- Number of successful image uploads from ESP32 Camera.
- Number of failed image uploads from ESP32 Camera.
- Number of data messages sent by ESP32 sensors.
- Devices that frequently lose connection.
- Parking slots with abnormal status updates.

Example analysis:

```text
ESP32 Sensor A01 sent data 120 times during the day.
ESP32 Sensor B03 has not sent data for the last 2 hours.
ESP32 Camera at the entrance gate failed to upload images 3 times.
```

### 4.5.2. User Activity Analysis

User Session Logs help check what users have done in the system.

Information that can be analyzed:

- When users logged in.
- Which functions users accessed most frequently.
- Whether users encountered API errors.
- Whether abnormal access behavior occurred.

Example:

```text
Manager01 logged in at 08:00 and viewed vehicle history 5 times.
User02 called the /admin/users API but was rejected because the user did not have permission.
```

### 4.5.3. API and Lambda Error Analysis

API Session Logs help detect errors when the Web/App or ESP32 devices call APIs.

Common errors:

| Error Type | Meaning |
| :--- | :--- |
| 400 | Invalid request format |
| 401 | Unauthenticated request |
| 403 | Access denied |
| 404 | Incorrect endpoint |
| 500 | Lambda Backend error |
| 504 | Request timeout |

Example error analysis:

```text
The /parking/slots API has an average response time of 120ms.
The /vehicle/logs API returned error 500 three times recently.
The /admin/users API was blocked because the user did not have Admin permission.
```

### 4.5.4. System Performance Analysis

Session Logs can support system performance evaluation by measuring the processing time of each step.

Important metrics include:

- Time taken by ESP32 to upload images to S3.
- Lambda image processing time.
- Rekognition call duration.
- API Gateway response time.
- DynamoDB query time.
- Success and failure rate of requests.

Example:

```text
Average image upload time: 2.5 seconds.
Average Lambda image processing time: 1.8 seconds.
Average API response time to Web/App: 120ms.
```

Based on this information, the team can optimize the system if any processing step takes too long.

---

## 4.6. Conclusion

Session Logs play an important role in operating the Parking IoT system. Recording logs by session helps administrators track the activities of ESP32 devices, Web/App, API Gateway, Lambda, and related AWS services in detail.

Through Session Logs, the system can trace data from the moment a device sends information until the data is processed and stored in DynamoDB. In addition, Session Logs support error detection, performance analysis, user activity tracking, and system stability evaluation.

By combining CloudWatch Logs, DynamoDB, and Amazon S3, the system can monitor logs in real time while also storing logs for long-term checking, reporting, and future optimization.