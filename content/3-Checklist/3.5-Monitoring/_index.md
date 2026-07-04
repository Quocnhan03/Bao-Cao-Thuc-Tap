---
title : "Monitoring and Management"
date :  "`r Sys.Date()`" 
weight : 5
chapter : false
pre : " <b> 3.5. </b> "
---

# 3.5. Monitoring and Management

This section describes how to monitor, log, detect errors, and manage the **Smart Parking IoT System** after deployment. Since the system uses multiple AWS services such as **Lambda, API Gateway, AWS IoT Core, Amazon S3, Amazon DynamoDB, Amazon Rekognition, and Amazon Bedrock**, monitoring is important to ensure stable operation, detect errors quickly, and control costs.

The main services used for monitoring and management include:

- **Amazon CloudWatch:** records logs, monitors errors, and tracks system performance.
- **AWS Budgets:** monitors AWS costs and sends cost alerts.
- **AWS CloudTrail:** records activities and actions in the AWS account.
- **IAM:** manages access permissions and security administration.
- **DynamoDB Console / S3 Console:** checks stored data and storage resources.

---

## 3.5.1. System Monitoring Objectives

System monitoring ensures that all components in the Parking IoT architecture operate correctly, data is processed properly, and administrators can detect problems in time.

The main objectives include:

- Monitor the operating status of Lambda functions.
- Check requests from the Web/App to API Gateway.
- Monitor data sent from ESP32 sensors to AWS IoT Core.
- Check image upload from ESP32 Camera to Amazon S3.
- Monitor image processing and license plate recognition.
- Check whether data is written to DynamoDB correctly.
- Detect errors during data processing.
- Monitor AWS costs to avoid exceeding the budget.
- Track user and service activities in the AWS account.

---

## 3.5.2. Monitoring with Amazon CloudWatch

Amazon CloudWatch is the main service used for logging and monitoring system activities. Services such as Lambda, API Gateway, AWS IoT Core, and DynamoDB can send logs or metrics to CloudWatch.

General monitoring flow:

```text
API Gateway / Lambda / AWS IoT Core / DynamoDB / Rekognition → Amazon CloudWatch
```

CloudWatch supports:

- Logging Lambda executions.
- Logging requests from API Gateway.
- Monitoring Lambda processing errors.
- Tracking Lambda execution duration.
- Monitoring the number of API requests.
- Checking errors when writing data to DynamoDB.
- Creating alarms when abnormal system behavior occurs.

Examples of logs to monitor:

| Component | Information to Monitor |
| :--- | :--- |
| Lambda Backend | Requests from Web/App and API processing errors |
| Lambda Image Processing | S3 image reading errors and Rekognition errors |
| Lambda Sensor Processing | MQTT payloads and DynamoDB write errors |
| API Gateway | Requests, responses, and 4xx/5xx errors |
| AWS IoT Core | MQTT data from ESP32 devices |
| DynamoDB | Data writing or query errors |

---

## 3.5.3. Monitoring AWS Lambda

AWS Lambda is the main processing component of the system, so Lambda functions must be monitored carefully to ensure stable operation.

The Lambda functions that need monitoring include:

| Lambda Function | Function |
| :--- | :--- |
| Lambda API Backend | Handles requests from the Web/App |
| Lambda Presigned URL | Creates upload URLs for ESP32 Camera |
| Lambda Image Processing | Processes images and calls Rekognition |
| Lambda Sensor Processing | Processes sensor data from AWS IoT Core |
| Lambda AI Service | Connects to Amazon Bedrock for AI queries |

Important metrics to monitor:

- **Invocations:** the number of times Lambda is called.
- **Errors:** the number of Lambda execution errors.
- **Duration:** Lambda execution time.
- **Throttles:** the number of times Lambda is throttled.
- **Memory Usage:** memory usage level.
- **Timeout:** errors caused by Lambda running longer than the configured timeout.

Example Lambda error checking flow:

```text
CloudWatch → Log Groups → Select Lambda Function → View Log Stream → Check Errors
```

When an error is detected, the administrator should check the log details to identify the cause, such as IAM permission errors, invalid input data, DynamoDB connection issues, or Rekognition call errors.

---

## 3.5.4. Monitoring Amazon API Gateway

Amazon API Gateway is the communication gateway between the Web/App, ESP32 Camera, and Lambda Backend. If API Gateway has issues, users or IoT devices may not be able to send requests to the system.

Items to monitor include:

- Number of requests to the API.
- Successful request rate.
- 4xx errors caused by invalid requests or missing permissions.
- 5xx errors caused by backend Lambda failures.
- API response time.
- Requests from the Web/App and ESP32 Camera.

Common API errors:

| Error Code | Meaning |
| :--- | :--- |
| 400 | Invalid request format |
| 401 | Unauthenticated request |
| 403 | Access denied |
| 404 | Incorrect endpoint |
| 500 | Lambda Backend error |
| 504 | Request timeout |

API monitoring flow:

```text
API Gateway → CloudWatch Logs → Check Requests and Responses
```

Monitoring API Gateway helps detect connection problems between the Web/App interface and the backend system.

---

## 3.5.5. Monitoring AWS IoT Core

AWS IoT Core is used to receive data from ESP32 sensors through MQTT. Therefore, the process of sending data from devices to AWS must be monitored.

Items to check include:

- Whether ESP32 can connect to AWS IoT Core.
- Whether the MQTT topic has the correct format.
- Whether the payload contains complete data.
- Whether the IoT Rule triggers Lambda correctly.
- Whether Lambda writes data to DynamoDB successfully.

Example MQTT topic:

```text
parking/slot/A01/status
```

Example valid payload:

```json
{
  "device_id": "esp32_sensor_01",
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

Common errors in the IoT flow:

| Error | Possible Cause |
| :--- | :--- |
| Device cannot connect | Incorrect endpoint, certificate error, or WiFi disconnection |
| No data received | Incorrect MQTT topic or device not publishing |
| IoT Rule not triggered | Incorrect rule condition or missing permission to invoke Lambda |
| Lambda cannot write to DynamoDB | Missing IAM permission or invalid data format |

Sensor data monitoring flow:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda → CloudWatch Logs
```

---

## 3.5.6. Monitoring Amazon S3 and Image Processing

Amazon S3 is used to store vehicle images from ESP32 Camera. When a new image is uploaded, S3 generates an ObjectCreated event to trigger the image processing Lambda function.

Image processing flow:

```text
ESP32 Camera → Amazon S3 → S3 ObjectCreated → Lambda Image Processing → Rekognition → DynamoDB
```

Items to check include:

- Whether the image is uploaded to S3 successfully.
- Whether the image is stored in the correct `entrance/` or `exit/` folder.
- Whether the S3 ObjectCreated event triggers Lambda.
- Whether Lambda can read the image from S3.
- Whether Lambda can call Rekognition successfully.
- Whether the recognition result is written to DynamoDB.

Example S3 image folder structure:

```text
parking-image-bucket/
├── entrance/
│   └── esp32_cam_01_20260427_103000.jpg
└── exit/
    └── esp32_cam_02_20260427_110000.jpg
```

Common errors:

| Error | How to Check |
| :--- | :--- |
| Image upload fails | Check Presigned URL and S3 permissions |
| S3 does not trigger Lambda | Check S3 Event Notification |
| Lambda cannot read image | Check Lambda IAM Role |
| Rekognition error | Check image format and Rekognition permission |
| Result is not stored | Check DynamoDB write permission |

---

## 3.5.7. Monitoring Amazon DynamoDB

Amazon DynamoDB is the main data storage service of the system. Data such as parking slot status, vehicle entry and exit history, and license plate recognition results are stored here.

Tables to monitor:

| Table | Stored Data |
| :--- | :--- |
| ParkingSlots | Latest status of each parking slot |
| VehicleLogs | Vehicle entry and exit history |
| SensorData | Sensor data over time |
| DeviceStatus | Device operating status if available |

Items to check include:

- Whether data is written to the correct table.
- Whether parking slot status is updated with the latest value.
- Whether vehicle entry and exit data contains license plate, timestamp, and image information.
- Whether Lambda has errors when writing data.
- Whether the primary key and query design need optimization.

Example data in the `ParkingSlots` table:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "updated_at": "2026-04-27T10:30:00",
  "device_id": "esp32_sensor_01"
}
```

Example data in the `VehicleLogs` table:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "direction": "in",
  "image_url": "s3://parking-image-bucket/entrance/car_001.jpg",
  "timestamp": "2026-04-27T10:30:00",
  "confidence": 92.5
}
```

---

## 3.5.8. Monitoring Amazon Rekognition and AI Service

Amazon Rekognition is used to analyze vehicle images and support license plate recognition. Amazon Bedrock can be used for the AI Service, allowing users to query parking data using natural language.

### Monitoring Rekognition

Items to check include:

- Whether Rekognition is called successfully by Lambda.
- Whether the input image has the correct format.
- Whether the recognition result has a high confidence score.
- Whether failed recognition cases are logged.

Example recognition result:

```json
{
  "plate_number": "51A-12345",
  "confidence": 92.5,
  "status": "recognized"
}
```

### Monitoring AI Service

AI Service flow:

```text
Web/App → API Gateway → Lambda AI Service → DynamoDB → Amazon Bedrock → Web/App
```

Items to check include:

- Whether users can send questions successfully.
- Whether Lambda AI Service can retrieve data from DynamoDB.
- Whether Amazon Bedrock returns a proper response.
- Whether response time is too long.
- Whether high cost occurs due to too many AI requests.

---

## 3.5.9. Error Alerts with CloudWatch Alarm

CloudWatch Alarm is used to send alerts when the system shows abnormal behavior. Alerts help administrators detect problems early and respond quickly.

Recommended alarms:

| Service | Alarm Condition |
| :--- | :--- |
| Lambda | Errors greater than 0 within 5 minutes |
| API Gateway | High 5xx error rate |
| IoT Core | No data received from devices for a long time |
| DynamoDB | Data write errors |
| CloudWatch Logs | Critical error logs appear |
| AWS Budgets | Cost exceeds the allowed threshold |

Example Lambda alarm:

```text
If Lambda Image Processing has Errors > 0 within 5 minutes → send an alert to the administrator.
```

Alerts can be sent through:

- Email.
- Amazon SNS.
- Admin dashboard.
- CloudWatch Alarm notification.

---

## 3.5.10. Cost Management with AWS Budgets

AWS Budgets is used to monitor AWS costs and send alerts when costs exceed a defined threshold. This is important because services such as Rekognition, Bedrock, S3, API Gateway, and CloudWatch may generate costs when used frequently.

Services that should be monitored for cost:

- Amazon S3.
- AWS Lambda.
- Amazon API Gateway.
- AWS IoT Core.
- Amazon DynamoDB.
- Amazon Rekognition.
- Amazon Bedrock.
- Amazon CloudWatch.
- Amazon CloudFront.

Example budget configuration:

```text
Monthly budget: 10 USD
Alert 1: When cost reaches 50%
Alert 2: When cost reaches 80%
Alert 3: When cost reaches 100%
```

Benefits of AWS Budgets:

- Avoid unexpected costs.
- Monitor monthly spending.
- Detect services that are being used too heavily.
- Support budget management for demo or learning environments.

---

## 3.5.11. Security Management with IAM and CloudTrail

IAM and CloudTrail help administrators control access permissions and track activities in the AWS account.

### IAM

IAM is used to manage access permissions between AWS services. The system should apply the **Least Privilege** principle, meaning each component only has the permissions it needs.

Example permissions:

| Component | Required Permission |
| :--- | :--- |
| Lambda Image Processing | Read S3, call Rekognition, write to DynamoDB |
| Lambda Sensor Processing | Write to DynamoDB |
| Lambda AI Service | Read DynamoDB, call Bedrock |
| API Gateway | Invoke Lambda |
| IoT Rule | Trigger Lambda |

### CloudTrail

AWS CloudTrail records activities in the AWS account, such as:

- Who created or deleted a Lambda function.
- Who changed an IAM Policy.
- Who created an S3 Bucket.
- Who changed API Gateway configuration.
- Who accessed or modified important resources.

CloudTrail improves transparency and supports investigation when security incidents occur.

---

## 3.5.12. System Administration Dashboard

Administrators can build a dashboard to monitor the overall Parking IoT system.

Information that should be displayed on the dashboard includes:

- Total number of parking slots.
- Number of available slots.
- Number of occupied slots.
- Number of vehicles entering today.
- Number of vehicles exiting today.
- List of recent errors.
- ESP32 device status.
- Number of images uploaded to S3.
- Number of Lambda errors.
- Current AWS cost.

Example dashboard metrics:

| Metric | Meaning |
| :--- | :--- |
| Total Slots | Total number of parking slots |
| Available Slots | Number of empty slots |
| Occupied Slots | Number of occupied slots |
| Today Entries | Number of vehicles entering today |
| Today Exits | Number of vehicles exiting today |
| Active Devices | Number of active devices |
| Lambda Errors | Number of Lambda errors |
| Current AWS Cost | Current AWS usage cost |

The dashboard helps administrators monitor the system quickly without checking each AWS service separately.

---

## 3.5.13. Troubleshooting Process

When the system encounters an error, administrators should follow a layer-by-layer checking process to identify the cause.

Example troubleshooting flow when the Web/App does not display data:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB → CloudWatch Logs
```

Checking steps:

1. Check whether the Web/App calls the correct API.
2. Check whether API Gateway receives the request.
3. Check whether Lambda Backend is triggered.
4. Check whether Lambda has errors in CloudWatch.
5. Check whether DynamoDB contains data.
6. Check Lambda IAM permissions.
7. Check the response returned to the Web/App.

Example troubleshooting flow when ESP32 sensor does not update status:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Checking steps:

1. Check whether ESP32 is connected to WiFi.
2. Check whether the device is connected to AWS IoT Core.
3. Check whether the MQTT topic is correct.
4. Check whether the IoT Rule is triggered.
5. Check whether Lambda Sensor Processing has error logs.
6. Check whether DynamoDB is updated.

---

## 3.5.14. Conclusion

The monitoring and management section helps the Parking IoT system operate stably, detect errors easily, and control AWS usage costs. Amazon CloudWatch is used to collect logs and monitor important components such as Lambda, API Gateway, IoT Core, DynamoDB, and Rekognition.

In addition, AWS Budgets helps control costs, IAM manages access permissions, and CloudTrail records activities in the AWS account. Building a dashboard and troubleshooting process allows administrators to monitor, inspect, and maintain the system effectively during real-world operation.