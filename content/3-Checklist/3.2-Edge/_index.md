---
title : "ESP32 Edge Devices"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 3.2. </b> "
---

# 3.2. ESP32 Edge Devices

This section presents the role of edge devices in the **Smart Parking IoT System**. Edge devices are installed directly at the parking area to collect real-world data, including vehicle images and parking slot status.

In this system, two main types of ESP32 devices are used:

- **ESP32 Camera:** used to capture vehicle images at the entry and exit gates.
- **ESP32 Sensor Device:** used to detect the status of each parking slot.

Data collected from ESP32 devices is sent to AWS for processing, storage, monitoring, and visualization through the Web/App interface.

---

## 3.2.1. Role of Edge Devices in the System

Edge devices act as the first data collection layer of the Parking IoT system. These devices are installed in the parking lot to collect real-time information.

The main tasks of edge devices include:

- Capturing vehicle images when cars enter or exit the parking lot.
- Detecting the status of each parking slot.
- Sending sensor data to AWS IoT Core.
- Uploading vehicle images to Amazon S3 using Presigned URLs.
- Supporting the automation of parking lot monitoring.

With edge devices, the system can reduce manual operations and update parking data more quickly and accurately.

---

## 3.2.2. ESP32 Camera

ESP32 Camera is used to capture vehicle images at the entry and exit gates of the parking lot. When a vehicle passes through the gate, the camera captures an image and uploads it to Amazon S3 for image processing and license plate recognition.

### Main Functions of ESP32 Camera

- Capture vehicle images when a vehicle is detected.
- Send a request to API Gateway to obtain a Presigned URL.
- Upload images directly to Amazon S3.
- Send image information with the recorded timestamp.
- Support license plate recognition using Amazon Rekognition.

### ESP32 Camera Workflow

```text
ESP32 Camera → API Gateway → Lambda creates Presigned URL → Amazon S3
```

After the image is uploaded to S3, the system continues with the following processing flow:

```text
Amazon S3 → S3 Event ObjectCreated → Image Processing Lambda → Amazon Rekognition → DynamoDB
```

### Detailed Processing Steps

1. ESP32 Camera is installed at the entry or exit gate of the parking lot.
2. When a vehicle passes through, the device captures an image.
3. ESP32 Camera sends a request to API Gateway to obtain a Presigned URL.
4. API Gateway invokes Lambda Backend to generate the Presigned URL.
5. Lambda returns the Presigned URL to ESP32 Camera.
6. ESP32 Camera uploads the JPEG image directly to Amazon S3.
7. After the image is successfully uploaded, S3 triggers the image processing Lambda function.
8. Lambda calls Amazon Rekognition to analyze the image.
9. The recognition result is stored in DynamoDB.

### Example Image Data

```json
{
  "image_id": "car_001.jpg",
  "device_id": "esp32_cam_01",
  "gate": "entrance",
  "direction": "in",
  "timestamp": "2026-04-27T10:30:00",
  "s3_url": "s3://parking-image-bucket/car_001.jpg"
}
```

| Attribute | Description |
| :--- | :--- |
| image_id | Image name or image ID |
| device_id | ESP32 Camera device ID |
| gate | Camera location, such as entrance or exit |
| direction | Vehicle direction: `in` or `out` |
| timestamp | Time when the image was captured |
| s3_url | Image path in Amazon S3 |

---

## 3.2.3. ESP32 Sensor Device

ESP32 sensor devices are used to detect the status of each parking slot. Depending on the actual design, the system can use ultrasonic sensors, infrared sensors, or magnetic sensors to determine whether a parking slot is occupied or available.

### Main Functions of ESP32 Sensor Device

- Read sensor data from each parking slot.
- Determine whether a parking slot is available or occupied.
- Send data to AWS IoT Core using the MQTT protocol.
- Update parking slot status in DynamoDB through Lambda.
- Support real-time parking status display on the Web/App interface.

### Parking Slot Status

The system mainly uses two parking slot statuses:

| Status | Description |
| :--- | :--- |
| available | The parking slot is empty |
| occupied | The parking slot is occupied by a vehicle |

### ESP32 Sensor Workflow

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

### Detailed Processing Steps

1. ESP32 reads data from the sensor installed at a parking slot.
2. The device determines the slot status as `available` or `occupied`.
3. ESP32 sends the data to AWS IoT Core using MQTT.
4. AWS IoT Core receives the data from the device.
5. IoT Rule checks the MQTT topic and forwards the data to Lambda.
6. Lambda Sensor Processing validates and normalizes the data.
7. The processed data is stored in DynamoDB.
8. The Web/App queries DynamoDB to display the latest parking slot status.

### Example MQTT Topic

```text
parking/slot/A01/status
```

### Example Payload Sent from ESP32 Sensor

```json
{
  "device_id": "esp32_sensor_01",
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

| Attribute | Description |
| :--- | :--- |
| device_id | ESP32 sensor device ID |
| slot_id | Parking slot ID |
| status | Parking slot status |
| timestamp | Time when the data was recorded |

---

## 3.2.4. Connecting ESP32 Devices to the Internet

ESP32 devices need a WiFi connection to send data to AWS. Each device is configured with network information and AWS connection information.

The required configuration includes:

- WiFi SSID.
- WiFi password.
- API Gateway endpoint for ESP32 Camera.
- AWS IoT Core endpoint for ESP32 sensors.
- Security certificates and private keys for MQTT connection.
- Device ID to identify each ESP32 device in the system.

Example device configuration:

```text
WiFi SSID: Parking_WiFi
Device ID: esp32_sensor_01
MQTT Topic: parking/slot/A01/status
AWS IoT Endpoint: xxxxxxxxxxxxxx-ats.iot.ap-southeast-1.amazonaws.com
```

Device identification helps the system manage devices more easily, troubleshoot errors, and scale when adding more sensors or cameras.

---

## 3.2.5. Connecting ESP32 Camera to Amazon S3

ESP32 Camera does not upload images directly through Lambda because image files can be large. Instead, it uses a Presigned URL to upload images directly to Amazon S3.

The image upload process is as follows:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → ESP32 Camera → Amazon S3
```

The steps include:

1. ESP32 Camera captures a vehicle image.
2. ESP32 Camera sends a request to API Gateway.
3. Lambda creates a Presigned URL for image upload.
4. ESP32 Camera receives the Presigned URL.
5. ESP32 Camera uploads the JPEG image to Amazon S3.
6. S3 triggers Lambda after the image is uploaded successfully.

This approach provides several benefits:

- Reduces workload on Lambda.
- Improves image upload performance.
- Uses Amazon S3 for reliable object storage.
- Makes it easy to trigger image processing using S3 events.

---

## 3.2.6. Connecting ESP32 Sensors to AWS IoT Core

ESP32 sensor devices send data to AWS IoT Core using the MQTT protocol. MQTT is suitable for IoT systems because it is lightweight, efficient, and works well with resource-limited devices.

The data transmission flow is:

```text
ESP32 Sensor → MQTT → AWS IoT Core → IoT Rule → Lambda → DynamoDB
```

The implementation steps include:

1. Create an IoT Thing to represent the ESP32 device in AWS IoT Core.
2. Create security certificates for the device.
3. Attach an IoT Policy to the certificate.
4. Configure the MQTT endpoint on the ESP32 device.
5. ESP32 publishes data to the defined MQTT topic.
6. IoT Rule forwards the data to Lambda for processing.
7. Lambda writes the processed data to DynamoDB.

Example periodic sensor data:

```json
{
  "device_id": "esp32_sensor_02",
  "slot_id": "B03",
  "status": "available",
  "timestamp": "2026-04-27T10:35:00"
}
```

---

## 3.2.7. Edge Device Security

Edge device security is important because ESP32 devices connect directly to the Internet and send data to AWS.

Security measures include:

- Do not store sensitive information publicly in the source code.
- Use certificates when connecting ESP32 devices to AWS IoT Core.
- Assign a unique device ID to each device.
- Configure IoT Policy so each device can publish only to its own topic.
- Validate ESP32 Camera requests through API Gateway.
- Use Presigned URLs with short expiration times.
- Do not provide direct AWS credentials to ESP32 devices.

Example security principle:

```text
Each ESP32 device can only publish data to its own MQTT topic.
ESP32 Camera can only upload images using a short-lived Presigned URL.
```

Limiting permissions reduces risks when a device fails or is accessed without authorization.

---

## 3.2.8. Error Handling at Edge Devices

During operation, ESP32 devices may encounter issues such as WiFi disconnection, failed data transmission, or failed image upload. Therefore, basic error handling should be implemented on the device side.

Common errors and handling methods:

| Error | Handling Method |
| :--- | :--- |
| WiFi disconnection | Automatically reconnect after a short delay |
| MQTT publishing failure | Retry sending data when the connection is restored |
| Image upload failure | Request a new Presigned URL and upload again |
| Incorrect sensor reading | Filter data or check multiple times before sending |
| Blurry camera image | Adjust camera angle and lighting conditions |

The device can temporarily store data in local memory if the network connection is lost and resend the data when the Internet connection is restored.

---

## 3.2.9. Edge Device Testing

Before fully integrating with AWS, each ESP32 device should be tested to ensure correct operation.

### ESP32 Camera Testing

- Check whether the camera can capture images.
- Check whether the image clearly shows the license plate.
- Check whether ESP32 can call API Gateway.
- Check whether the Presigned URL is generated successfully.
- Check whether the image is uploaded to S3 successfully.
- Check whether S3 triggers the image processing Lambda function.

### ESP32 Sensor Testing

- Check whether the sensor reads the correct status.
- Check whether ESP32 connects to WiFi successfully.
- Check whether ESP32 connects to AWS IoT Core.
- Check whether data is sent to the correct MQTT topic.
- Check whether IoT Rule triggers Lambda correctly.
- Check whether DynamoDB stores the latest parking status.

---

## 3.2.10. Conclusion

The ESP32 edge device layer is an important data collection layer of the Parking IoT system. ESP32 Camera is responsible for capturing vehicle entry and exit images, while ESP32 sensor devices record the status of each parking slot.

Data from edge devices is sent to AWS through two main flows: vehicle images are uploaded to Amazon S3 using Presigned URLs, while sensor data is sent to AWS IoT Core using MQTT. After that, AWS Lambda processes the data and stores the results in DynamoDB.

Deploying edge devices allows the Parking IoT system to monitor the parking lot in real time, reduce manual operations, and provide a data foundation for advanced features such as license plate recognition, parking statistics, and AI-assisted management.