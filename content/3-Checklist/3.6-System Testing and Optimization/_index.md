---
title : "System Testing and Optimization"
date :  "`r Sys.Date()`" 
weight : 6
chapter : false
pre : " <b> 3.6. </b> "
---

# 3.6. System Testing and Optimization

This section presents the testing and optimization process for the **Smart Parking IoT System** after deploying the main components such as ESP32 devices, AWS IoT Core, Amazon S3, AWS Lambda, Amazon Rekognition, DynamoDB, API Gateway, Cognito, CloudFront, and CloudWatch.

The purpose of testing is to ensure that the system works according to the design, data is transmitted and processed correctly, the Web/App interface displays accurate information, and the system can operate stably, securely, and cost-effectively.

---

## 3.6.1. Testing Objectives

The system testing process is used to verify whether the main functions of the Parking IoT system work correctly.

The testing objectives include:

- Check whether ESP32 Camera can capture and upload images to Amazon S3 successfully.
- Check whether ESP32 sensors can send parking slot status data to AWS IoT Core.
- Check whether AWS IoT Core can trigger Lambda to process sensor data.
- Check whether S3 ObjectCreated Event can trigger Lambda to process images.
- Check whether Amazon Rekognition can analyze images and return recognition results.
- Check whether DynamoDB stores data correctly.
- Check whether API Gateway and Lambda Backend return data to the Web/App.
- Check whether Cognito authenticates users correctly.
- Check whether CloudWatch records logs and supports error detection.
- Check whether AWS usage costs remain within the expected budget.

---

## 3.6.2. Testing ESP32 Camera

ESP32 Camera is used to capture images of vehicles entering and exiting the parking lot. Therefore, it is necessary to test its ability to capture images, request a Presigned URL, and upload images to Amazon S3.

Testing flow:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

Testing steps:

1. Power on the ESP32 Camera and connect it to WiFi.
2. Check whether the device connects to the network successfully.
3. Let a vehicle or object pass through the camera area.
4. Check whether ESP32 Camera can capture an image.
5. Check whether ESP32 Camera can call API Gateway to request a Presigned URL.
6. Check whether Lambda creates the Presigned URL successfully.
7. Check whether the image is uploaded to Amazon S3.
8. Check whether the image is stored in the correct `entrance/` or `exit/` folder.

Expected results:

| Test Item | Expected Result |
| :--- | :--- |
| WiFi connection | ESP32 Camera connects successfully |
| Image capture | Image is captured clearly |
| API Gateway request | Request is sent successfully |
| Presigned URL generation | Lambda returns a valid URL |
| S3 upload | Image appears in the S3 Bucket |

---

## 3.6.3. Testing ESP32 Sensors

ESP32 sensors are used to determine the status of each parking slot. The device sends data to AWS IoT Core using MQTT.

Testing flow:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Testing steps:

1. Power on the ESP32 sensor device.
2. Check whether the device connects to WiFi.
3. Check whether the device connects to AWS IoT Core.
4. Place an object or vehicle in the sensor area.
5. Check whether the sensor detects the status as `occupied`.
6. Remove the object or vehicle from the sensor area.
7. Check whether the sensor detects the status as `available`.
8. Check whether data is published to the correct MQTT topic.
9. Check whether IoT Rule triggers Lambda.
10. Check whether DynamoDB updates the latest parking slot status.

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

Expected results:

| Test Item | Expected Result |
| :--- | :--- |
| WiFi connection | ESP32 connects successfully |
| AWS IoT Core connection | Device publishes MQTT data successfully |
| Sensor data | Status is correctly detected as `available` or `occupied` |
| IoT Rule | Lambda is triggered |
| DynamoDB | Data is updated correctly |

---

## 3.6.4. Testing Image Processing and License Plate Recognition

After ESP32 Camera uploads an image to Amazon S3, the system needs to test whether Lambda is triggered and whether Amazon Rekognition processes the image correctly.

Testing flow:

```text
Amazon S3 → S3 ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Testing steps:

1. Upload a vehicle image to S3 using ESP32 Camera or upload it manually for testing.
2. Check whether the S3 ObjectCreated Event is triggered.
3. Check whether Lambda Image Processing runs successfully.
4. Check whether Lambda can read the image from S3.
5. Check whether Lambda calls Amazon Rekognition.
6. Check whether the recognition result is returned.
7. Check whether the data is written to the VehicleLogs table in DynamoDB.

Example processed data:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "confidence": 92.5,
  "direction": "in",
  "image_url": "s3://parking-image-bucket/entrance/car_001.jpg",
  "timestamp": "2026-04-27T10:30:00"
}
```

Expected results:

| Test Item | Expected Result |
| :--- | :--- |
| Image upload | Image is stored in S3 |
| S3 Event | Lambda is triggered |
| Rekognition | Image is analyzed |
| DynamoDB | Result is stored in VehicleLogs |
| CloudWatch | Successful processing log is recorded |

---

## 3.6.5. Testing API Gateway and Lambda Backend

API Gateway and Lambda Backend act as the middle layer between the Web/App and data stored in DynamoDB. The APIs must be tested to ensure they work correctly.

Testing flow:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB
```

APIs to test:

| API Endpoint | Testing Purpose |
| :--- | :--- |
| `GET /parking/slots` | Get the list of parking slots |
| `GET /vehicle/logs` | Get vehicle entry and exit history |
| `POST /upload-url` | Create a Presigned URL |
| `GET /vehicle/search` | Search vehicles by license plate |
| `POST /ai/query` | Send a question to the AI Service |

Testing steps:

1. Send requests to each API endpoint.
2. Check whether API Gateway receives the request.
3. Check whether Lambda Backend is invoked.
4. Check whether Lambda queries DynamoDB correctly.
5. Check whether the response is returned in the correct JSON format.
6. Check whether there are any 4xx or 5xx errors.

Example API response:

```json
{
  "total_slots": 50,
  "available": 18,
  "occupied": 32
}
```

Expected results:

| Test Item | Expected Result |
| :--- | :--- |
| API receives request | Request is sent successfully |
| Lambda Backend | Lambda processes the request correctly |
| DynamoDB Query | Data is queried accurately |
| Response | JSON response is returned correctly |
| Error Handling | Error logs are recorded if the request is invalid |

---

## 3.6.6. Testing the Web/App Interface

The Web/App interface is where users view parking data. Therefore, it is necessary to check whether the interface displays backend data correctly.

Functions to test:

- User login.
- Display total parking slots.
- Display available and occupied slots.
- Display the status of each parking slot.
- Display vehicle entry and exit history.
- Display vehicle images from S3.
- Search vehicles by license plate.
- Display error messages when API issues occur.

Interface testing flow:

```text
User → CloudFront → S3 Static Website → API Gateway → Lambda → DynamoDB
```

Expected results:

| Function | Expected Result |
| :--- | :--- |
| Login | User logs in successfully |
| Dashboard | Correctly displays available and occupied slots |
| Parking Slots | Parking slot status is updated |
| Vehicle Logs | Vehicle entry and exit history is displayed |
| Search | License plate search returns correct results |
| Error Message | Interface displays clear error messages |

---

## 3.6.7. Security Testing

Security testing ensures that the system does not allow unauthorized access and that AWS services are granted only the required permissions.

Items to test:

- Users who are not logged in cannot call protected APIs.
- Expired Cognito tokens are rejected by API Gateway.
- Normal users cannot access Admin functions.
- ESP32 Camera does not have direct AWS permissions.
- Presigned URLs are valid only for a short period of time.
- ESP32 sensors can only publish to authorized MQTT topics.
- Lambda functions only have permissions required for their tasks.

Example test without token:

```text
Web/App → API Gateway → No Cognito Token → Request is rejected
```

Expected results:

| Test Item | Expected Result |
| :--- | :--- |
| Call API without token | Request is rejected |
| Invalid or expired token | Request is rejected |
| User accesses Admin API | Rejected if the user has no permission |
| Expired Presigned URL | Upload is not allowed |
| Wrong MQTT topic | Device is not allowed to publish |

---

## 3.6.8. Testing Monitoring and Logs

CloudWatch is used to check logs of different system components. Log testing ensures that when an error occurs, administrators can quickly identify the cause.

Logs to check:

| Component | Logs to Check |
| :--- | :--- |
| Lambda Backend | Web/App requests and data query errors |
| Lambda Image Processing | Image reading errors and Rekognition errors |
| Lambda Sensor Processing | MQTT payload and DynamoDB write errors |
| API Gateway | Requests, responses, and 4xx/5xx errors |
| IoT Core | MQTT data from ESP32 devices |
| CloudFront/WAF | Blocked or abnormal requests |

Testing steps:

1. Create a valid request and check successful logs.
2. Create an invalid request and check error logs.
3. Send an MQTT payload with missing fields and check Lambda logs.
4. Upload an invalid image format and check Lambda Image Processing logs.
5. Check CloudWatch Log Groups for each Lambda function.

Expected result:

```text
CloudWatch records both successful logs and error logs.
Administrators can trace errors by service and processing step.
```

---

## 3.6.9. System Performance Optimization

After functional testing, the system should be optimized to run faster, more reliably, and support a larger number of users or devices.

Optimization methods include:

- Optimize Lambda execution time.
- Reduce image size before uploading to S3.
- Use Presigned URLs to reduce Lambda workload.
- Design suitable DynamoDB Partition Keys.
- Reduce unnecessary API calls from the Web/App.
- Use CloudFront cache to speed up website access.
- Configure appropriate Lambda timeout values.
- Reduce unnecessary logs to lower CloudWatch costs.

Example image optimization:

```text
ESP32 Camera reduces image size before uploading to S3.
This helps improve upload speed and reduce storage costs.
```

Example API optimization:

```text
The Web/App should call the parking status API at a suitable interval,
instead of calling the API too frequently in a short period of time.
```

---

## 3.6.10. AWS Cost Optimization

Because the system uses multiple AWS services, cost optimization is necessary, especially in a learning or demo environment.

Cost optimization methods include:

- Delete old images in S3 if they are no longer needed.
- Configure S3 Lifecycle Rules to move or delete old data.
- Limit the number of Amazon Rekognition calls.
- Limit the number of Amazon Bedrock calls if AI Service is used.
- Monitor costs using AWS Budgets.
- Enable only necessary logs in CloudWatch.
- Delete unused resources after the demo.
- Use DynamoDB On-Demand mode for small testing environments.

Example budget configuration:

```text
Monthly Budget: 10 USD
Alert at 50%, 80%, and 100%
Send alert to administrator email
```

Expected result:

```text
The system operates within the expected cost range.
Administrators receive alerts when costs increase unexpectedly.
```

---

## 3.6.11. Summary of Testing Results

After testing each component, the results can be summarized in the following table:

| Test Item | Expected Result | Status |
| :--- | :--- | :--- |
| ESP32 Camera | Captures and uploads images to S3 | Passed |
| ESP32 Sensor | Sends status data to AWS IoT Core | Passed |
| S3 Event | Triggers image processing Lambda | Passed |
| Rekognition | Analyzes images and returns results | Passed |
| DynamoDB | Stores data correctly | Passed |
| API Gateway | Returns data to Web/App | Passed |
| Cognito | Authenticates users | Passed |
| CloudWatch | Records system logs | Passed |
| AWS Budgets | Monitors AWS costs | Passed |

This table can be updated based on the actual results during deployment and demonstration.

---

## 3.6.12. Conclusion

The system testing and optimization section ensures that the Parking IoT system works according to the design, data is transmitted correctly from ESP32 devices to AWS, Lambda functions perform their assigned tasks, and the Web/App interface displays complete information.

Through the testing process, the team can detect errors in different flows such as image upload, sensor data transmission, image processing, API queries, or user authentication. In addition, performance and cost optimization help the system operate stably, efficiently, and economically in real-world conditions.

After completing testing, the Parking IoT system can support key functions such as real-time parking slot monitoring, vehicle entry and exit history storage, license plate recognition, Web/App data visualization, and system administration through CloudWatch and AWS Budgets.