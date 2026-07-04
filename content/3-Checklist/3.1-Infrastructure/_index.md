---
title : "AWS Core Infrastructure"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 3.1 </b> "
---

# 3.1. AWS Core Infrastructure

This section presents the process of setting up the core AWS infrastructure for the **Smart Parking IoT System**. The core infrastructure includes main services such as **Amazon S3, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS IoT Core, IAM, CloudFront, WAF, and CloudWatch**.

The system is built using an **AWS Serverless** model, which reduces the need for server management and allows the system to scale easily when the number of ESP32 devices, cameras, sensors, or Web/App users increases.

---

## 3.1.1. Objectives of the Core Infrastructure

The AWS core infrastructure is designed to achieve the following objectives:

- Provide a centralized data storage environment for the Parking IoT system.
- Allow ESP32 Camera to upload vehicle images to Amazon S3.
- Allow ESP32 sensors to send parking slot status data to AWS IoT Core.
- Process data using AWS Lambda without managing servers.
- Store vehicle information, license plate data, and parking slot status in DynamoDB.
- Provide APIs for the Web/App through Amazon API Gateway.
- Ensure security using IAM, Cognito, and WAF.
- Monitor logs, errors, and system performance using Amazon CloudWatch.

---

## 3.1.2. Initializing the AWS CDK Project

AWS CDK is used to manage infrastructure as code, also known as **Infrastructure as Code - IaC**. Instead of manually creating each service in the AWS Console, the team can define AWS resources using code and deploy them automatically.

The main tasks include:

- Install Node.js and AWS CDK CLI.
- Configure AWS CLI with the AWS account.
- Initialize a CDK project using TypeScript or Python.
- Create stacks for different groups of resources.
- Deploy the infrastructure to AWS using CDK commands.

Example project structure:

```text
parking-iot-cdk/
├── bin/
│   └── parking-iot.ts
├── lib/
│   ├── storage-stack.ts
│   ├── api-stack.ts
│   ├── iot-stack.ts
│   ├── auth-stack.ts
│   └── monitoring-stack.ts
├── package.json
└── cdk.json
```

The main stacks can be organized as follows:

| Stack | Function |
| :--- | :--- |
| Storage Stack | Creates S3 Bucket and DynamoDB tables |
| API Stack | Creates API Gateway and Lambda Backend |
| IoT Stack | Creates IoT Core Rule and sensor processing Lambda |
| Auth Stack | Creates Cognito User Pool |
| Monitoring Stack | Creates CloudWatch Logs and alerts |

Using AWS CDK makes the deployment process repeatable, easier to modify, and easier to manage through version control.

---

## 3.1.3. Setting Up Amazon S3

Amazon S3 is used for two main purposes in the Parking IoT system:

- Hosting the static Web/App interface.
- Storing vehicle images sent from ESP32 Camera.

### S3 Static Website

The Web/App interface can be built into HTML, CSS, and JavaScript files and uploaded to an S3 Bucket. After that, CloudFront distributes the website content to users.

Website access flow:

```text
User → Route 53 → CloudFront → S3 Static Website
```

### S3 for Vehicle Image Storage

When the ESP32 Camera captures an image of a vehicle entering or exiting the parking area, the device requests a **Presigned URL** from API Gateway. Then, the ESP32 Camera uploads the image directly to Amazon S3.

Image upload flow:

```text
ESP32 Camera → API Gateway → Lambda creates Presigned URL → Amazon S3
```

After the image is successfully uploaded, S3 generates an **ObjectCreated** event to trigger the image processing Lambda function.

```text
Amazon S3 → S3 Event ObjectCreated → Image Processing Lambda
```

---

## 3.1.4. Setting Up Amazon DynamoDB

Amazon DynamoDB is used as the main database of the system. Data is stored in NoSQL format, which is suitable for IoT systems that require fast writing and real-time querying.

The main data tables include:

| Table Name | Function |
| :--- | :--- |
| ParkingSlots | Stores the status of each parking slot |
| VehicleLogs | Stores vehicle entry and exit history |
| SensorData | Stores sensor data |
| Users | Stores user information if needed |

Example data for the `ParkingSlots` table:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "updated_at": "2026-04-27T10:30:00"
}
```

Example data for the `VehicleLogs` table:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "direction": "in",
  "image_url": "s3://parking-image-bucket/car_001.jpg",
  "timestamp": "2026-04-27T10:30:00"
}
```

DynamoDB helps the system quickly retrieve parking slot status, vehicle entry and exit history, and license plate recognition results.

---

## 3.1.5. Setting Up AWS Lambda

AWS Lambda is the main processing component of the system. Lambda allows code to run when an event occurs without deploying or managing a separate server.

The main Lambda functions include:

| Lambda Function | Function |
| :--- | :--- |
| Lambda API Backend | Handles requests from the Web/App |
| Lambda Presigned URL | Creates Presigned URLs for ESP32 Camera to upload images |
| Lambda Image Processing | Processes images when new images are uploaded to S3 |
| Lambda Sensor Processing | Processes sensor data from AWS IoT Core |
| Lambda AI Service | Connects with Amazon Bedrock for AI features |

Image processing Lambda flow:

```text
S3 ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Sensor processing Lambda flow:

```text
AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Lambda allows the system to operate flexibly, run only when events occur, and automatically scale based on the number of requests.

---

## 3.1.6. Setting Up Amazon API Gateway

Amazon API Gateway is used as the communication gateway between the Web/App, ESP32 Camera, and Lambda Functions.

The main APIs may include:

| API Endpoint | Function |
| :--- | :--- |
| `/parking/slots` | Gets parking slot status |
| `/vehicle/logs` | Gets vehicle entry and exit history |
| `/upload-url` | Creates a Presigned URL for ESP32 Camera |
| `/ai/query` | Sends questions to the AI Service |

Web/App API request flow:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB
```

ESP32 Camera Presigned URL request flow:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

API Gateway helps the system manage requests in a centralized way, control access more easily, and integrate with Cognito Authorizer.

---

## 3.1.7. Setting Up AWS IoT Core

AWS IoT Core is used to receive data from ESP32 sensors through the MQTT protocol.

ESP32 sensors send parking slot status data to an MQTT topic, for example:

```text
parking/slot/A01/status
```

Example payload:

```json
{
  "slot_id": "A01",
  "status": "available",
  "timestamp": "2026-04-27T10:30:00"
}
```

Sensor data flow:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

AWS IoT Core helps manage device connections, security certificates, and MQTT data from IoT devices.

---

## 3.1.8. Setting Up VPC and Networking

In the Parking IoT system using serverless architecture, most services such as **S3, DynamoDB, IoT Core, Rekognition, Bedrock, and CloudWatch** are AWS managed services and are not placed directly inside a VPC.

However, a VPC can be configured if the system needs to:

- Run Lambda functions inside a private network.
- Connect to an internal database.
- Isolate backend components.
- Improve network traffic control.

A basic VPC may include:

| Component | Function |
| :--- | :--- |
| Public Subnet | Used for resources that need Internet access |
| Private Subnet | Used for Lambda or internal resources |
| Internet Gateway | Allows Internet access from the Public Subnet |
| NAT Gateway | Allows resources in the Private Subnet to access the Internet |
| Security Group | Controls inbound and outbound traffic |

Note: In the architecture diagram, services such as S3, DynamoDB, CloudWatch, Rekognition, and Bedrock should not be placed inside the VPC because they are regional AWS managed services.

---

## 3.1.9. Configuring IAM Roles and Policies

IAM is used to manage permissions for AWS services. The system applies the **Least Privilege** principle, meaning each service is granted only the minimum permissions required to perform its task.

Some required permissions include:

| Component | Required Permission |
| :--- | :--- |
| Lambda API Backend | Read and write data in DynamoDB |
| Lambda Presigned URL | Create Presigned URLs for image upload to S3 |
| Lambda Image Processing | Read images from S3, call Rekognition, and write data to DynamoDB |
| Lambda Sensor Processing | Write sensor data to DynamoDB |
| Lambda AI Service | Call Bedrock and read data from DynamoDB |
| API Gateway | Invoke Lambda functions |
| IoT Rule | Trigger the sensor processing Lambda function |

Clear permission management improves system security, avoids overly broad permissions, and reduces security risks.

---

## 3.1.10. Conclusion

The AWS core infrastructure is an important foundation for the stable operation of the Parking IoT system. Services such as S3, DynamoDB, Lambda, API Gateway, and IoT Core handle data storage, processing, and communication between ESP32 devices and the Web/App.

In addition, IAM controls access permissions, CloudWatch supports system monitoring, and CDK helps deploy infrastructure automatically and manage it more easily. With the serverless architecture, the system can scale flexibly, optimize costs, and meet the requirements of a Smart Parking IoT model.