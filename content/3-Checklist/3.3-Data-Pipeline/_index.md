---
title : "IoT Data Pipeline"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 3.3. </b> "
---

# 3.3. IoT Data Pipeline

This section describes how data is collected, transmitted, processed, and stored in the **Smart Parking IoT System**. The IoT data pipeline connects ESP32 devices in the parking area with AWS services used for processing, storage, license plate recognition, monitoring, and data visualization.

In the Parking IoT system, the data is divided into two main groups:

- **Image data:** collected from ESP32 Camera when vehicles enter or exit the parking lot.
- **Sensor data:** collected from ESP32 sensor devices to detect the status of each parking slot.

After the data is sent to AWS, it is processed by **AWS Lambda**, stored in **Amazon S3** and **Amazon DynamoDB**, and displayed on the Web/App interface. The data can also be used for AI-based features in the future.

---

## 3.3.1. Data Pipeline Overview

The data pipeline of the Parking IoT system consists of multiple processing steps, starting from edge devices and ending in AWS Cloud services.

General data flow:

```text
ESP32 Camera / ESP32 Sensor → AWS Services → Lambda Processing → DynamoDB / S3 → Web/App
```

The system has three main data flows:

| Data Flow | Description |
| :--- | :--- |
| Image Data Flow | ESP32 Camera captures vehicle images and uploads them to Amazon S3 |
| Sensor Data Flow | ESP32 sensors send parking slot status to AWS IoT Core |
| Web/App Query Flow | Users access system data through API Gateway and Lambda |

Each data flow is processed separately, but the final processed results are stored centrally in DynamoDB for management and visualization.

---

## 3.3.2. Image Data Flow from ESP32 Camera

The image data flow is used to record vehicles entering or exiting the parking lot and to support license plate recognition.

Instead of sending images directly through Lambda, the ESP32 Camera requests a **Presigned URL** from API Gateway. Then, the device uploads the image directly to Amazon S3. This approach reduces Lambda workload and is more suitable for image files with larger sizes.

Image upload flow:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

After the image is uploaded to S3, the system continues processing through the following flow:

```text
Amazon S3 → S3 Event ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Detailed processing steps:

1. ESP32 Camera detects a vehicle at the entry or exit gate.
2. The device captures a vehicle image.
3. ESP32 Camera sends a request to API Gateway to get a Presigned URL.
4. API Gateway invokes the Lambda Presigned URL function.
5. Lambda creates a Presigned URL and returns it to ESP32 Camera.
6. ESP32 Camera uploads the JPEG image directly to Amazon S3.
7. Amazon S3 generates an ObjectCreated event after the image is uploaded successfully.
8. The S3 event triggers the Lambda Image Processing function.
9. Lambda calls Amazon Rekognition to analyze the image.
10. The recognition result is stored in DynamoDB.

---

## 3.3.3. Image Storage in Amazon S3

Amazon S3 is used to store vehicle images. Each image can be named based on the device ID, timestamp, gate location, or vehicle ID for easier management.

Example S3 storage structure:

```text
parking-image-bucket/
├── entrance/
│   ├── esp32_cam_01_20260427_103000.jpg
│   └── esp32_cam_01_20260427_104500.jpg
├── exit/
│   ├── esp32_cam_02_20260427_110000.jpg
│   └── esp32_cam_02_20260427_111500.jpg
```

This folder structure helps distinguish between entry images and exit images.

Example image metadata:

```json
{
  "image_id": "esp32_cam_01_20260427_103000.jpg",
  "device_id": "esp32_cam_01",
  "gate": "entrance",
  "direction": "in",
  "timestamp": "2026-04-27T10:30:00",
  "s3_url": "s3://parking-image-bucket/entrance/esp32_cam_01_20260427_103000.jpg"
}
```

---

## 3.3.4. Image Processing with Lambda and Rekognition

After an image is uploaded to Amazon S3, the ObjectCreated event triggers a Lambda function to process the image. Lambda receives the image information from the S3 event and calls Amazon Rekognition for image analysis.

Processing flow:

```text
S3 ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Role of each component:

| Component | Role |
| :--- | :--- |
| Amazon S3 | Stores vehicle images |
| S3 ObjectCreated | Triggers Lambda when a new image is uploaded |
| Lambda Image Processing | Processes the image and calls Rekognition |
| Amazon Rekognition | Analyzes the image and supports license plate recognition |
| DynamoDB | Stores the recognition result |

The processed result may include:

- Image ID.
- License plate number.
- Recognition confidence score.
- Vehicle direction.
- Timestamp.
- Image path in S3.

Example processed data:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "confidence": 92.5,
  "direction": "in",
  "image_url": "s3://parking-image-bucket/entrance/esp32_cam_01_20260427_103000.jpg",
  "timestamp": "2026-04-27T10:30:00"
}
```

---

## 3.3.5. Sensor Data Flow through AWS IoT Core

The sensor data flow is used to update the status of each parking slot in real time. ESP32 sensor devices send data to AWS IoT Core using the MQTT protocol.

Sensor data flow:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Detailed processing steps:

1. ESP32 sensor reads data from the sensor installed at a parking slot.
2. The device determines whether the parking slot is `available` or `occupied`.
3. ESP32 sends the data to AWS IoT Core using MQTT.
4. AWS IoT Core receives data from the device.
5. IoT Rule checks the MQTT topic and forwards the data to Lambda.
6. Lambda Sensor Processing validates and normalizes the data.
7. The processed data is stored in DynamoDB.
8. The Web/App queries DynamoDB to display the latest parking status.

Example MQTT topic:

```text
parking/slot/A01/status
```

Example payload:

```json
{
  "device_id": "esp32_sensor_01",
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

---

## 3.3.6. Sensor Data Processing and Normalization

Before storing data in DynamoDB, sensor data must be validated to ensure the correct format and reduce inaccurate records.

Lambda Sensor Processing performs the following tasks:

- Checks whether `device_id` exists.
- Checks whether `slot_id` has the correct format.
- Checks whether `status` is either `available` or `occupied`.
- Adds a processing timestamp if the device does not send one.
- Removes invalid or incomplete data.
- Writes the latest parking slot status to DynamoDB.

Example valid data:

```json
{
  "slot_id": "A01",
  "status": "available",
  "updated_at": "2026-04-27T10:30:00"
}
```

Example invalid data:

```json
{
  "slot_id": "",
  "status": "unknown"
}
```

Invalid data will not be written to DynamoDB, or it can be logged to CloudWatch for later checking.

---

## 3.3.7. Storing Data in Amazon DynamoDB

Amazon DynamoDB is used to store processed data. The system can use multiple tables to separate vehicle data, sensor data, and parking slot status.

Main tables:

| Table | Function |
| :--- | :--- |
| ParkingSlots | Stores the latest status of each parking slot |
| VehicleLogs | Stores vehicle entry and exit history |
| SensorData | Stores sensor data over time |
| DeviceStatus | Stores device operating status if needed |

Example `ParkingSlots` data:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "updated_at": "2026-04-27T10:30:00",
  "device_id": "esp32_sensor_01"
}
```

Example `VehicleLogs` data:

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

DynamoDB allows the system to query data quickly for features such as parking status display, vehicle history search, and dashboard visualization.

---

## 3.3.8. Data Query Flow from Web/App

Users access the Web/App to view parking slot status, vehicle entry and exit history, and license plate information. The Web/App does not access DynamoDB directly. Instead, it calls API Gateway, and API Gateway forwards the request to Lambda Backend.

Query flow:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB → Lambda Backend → Web/App
```

Main query functions include:

- Get the list of parking slots.
- View the status of each parking slot.
- View the number of available and occupied slots.
- View vehicle entry and exit history.
- Search vehicles by license plate.
- View vehicle images stored in S3.
- View parking statistics.

Example API endpoint:

```text
GET /parking/slots
```

Example response:

```json
{
  "total_slots": 50,
  "available": 18,
  "occupied": 32,
  "slots": [
    {
      "slot_id": "A01",
      "status": "occupied"
    },
    {
      "slot_id": "A02",
      "status": "available"
    }
  ]
}
```

---

## 3.3.9. AI Service Data Flow

In addition to standard parking management features, the system can integrate Amazon Bedrock to support natural language queries. Users can ask questions through the Web/App, and the system processes the request using Lambda AI Service.

AI service flow:

```text
Web/App → API Gateway → Lambda AI Service → DynamoDB → Amazon Bedrock → Web/App
```

Processing steps:

1. The user enters a question in the Web/App.
2. The Web/App sends the question to API Gateway.
3. API Gateway invokes Lambda AI Service.
4. Lambda AI Service queries the required data from DynamoDB.
5. Lambda sends the data context to Amazon Bedrock.
6. Amazon Bedrock generates a natural language response.
7. The result is returned to the Web/App.

Example question:

```text
How many parking slots are currently available?
```

Example response:

```text
There are currently 18 available parking slots out of 50 total slots.
```

---

## 3.3.10. Logging and Error Handling in the Data Pipeline

During data transmission and processing, the system may encounter errors such as device disconnection, failed image upload, invalid sensor payload, or Lambda processing failure. Therefore, CloudWatch is used to collect logs and support error checking.

Common errors and handling methods:

| Error | Handling Method |
| :--- | :--- |
| ESP32 loses WiFi connection | Device reconnects automatically and resends data |
| Image upload fails | ESP32 requests a new Presigned URL and uploads again |
| MQTT payload has invalid format | Lambda logs the error to CloudWatch |
| Rekognition cannot detect license plate | Store the result as requiring manual review |
| DynamoDB write failure | Lambda retries or logs the error |
| API Gateway returns 4xx/5xx errors | Check request format and Lambda logs |

Logging flow:

```text
API Gateway / Lambda / IoT Core / Rekognition / DynamoDB → CloudWatch
```

CloudWatch helps the team detect issues early and ensures that the data pipeline operates reliably.

---

## 3.3.11. Conclusion

The IoT data pipeline is an important component that allows the Parking IoT system to operate automatically and in real time. Data from ESP32 Camera and ESP32 sensors is sent to AWS through two main flows: vehicle images are uploaded to Amazon S3 using Presigned URLs, while sensor data is sent to AWS IoT Core using MQTT.

After the data is received, AWS Lambda performs processing tasks, Amazon Rekognition supports license plate recognition, DynamoDB stores the results, and the Web/App displays the data to users. CloudWatch is also used to log and monitor errors throughout the entire process.

With this design, the system can monitor the parking lot in real time, store data centrally, support license plate recognition, and provide a foundation for advanced features such as statistics, alerts, and AI Service.