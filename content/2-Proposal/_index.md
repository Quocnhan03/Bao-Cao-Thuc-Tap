---
title: "Proposal"
date: 2026-04-26
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# Smart Parking IoT Platform with AWS Serverless

> **AWS Serverless Solution for Parking Monitoring, License Plate Recognition, and AI Assistance**

---

## 1. Executive Summary

The project aims to build a **Smart Parking IoT** system that automates the parking monitoring process, vehicle recognition, and real-time data management. The system utilizes IoT devices such as **ESP32 Camera** and **ESP32 Sensors** to capture images of vehicles entering/exiting, monitor parking slot availability, and collect data from the parking lot.

Data from the devices is transmitted to AWS through services like **AWS IoT Core**, **Amazon S3**, and **Amazon API Gateway**, and processed using **AWS Lambda**. Vehicle images are stored in **Amazon S3**, which triggers Lambda to process the images and call **Amazon Rekognition** for license plate recognition. The recognition results and sensor data are stored in **Amazon DynamoDB** for querying, management, and display on the Web/App.

Additionally, the system integrates **Amazon Bedrock** via a **Lambda AI Service** layer to support data analysis, answer intelligent queries, and provide a modern parking management experience. With the AWS Serverless architecture, the system is highly scalable, reduces operational costs, and eliminates the need for traditional server management.

---

## 2. Problem Statement

### 2.1. Current Challenges

Traditional parking lots face many limitations in operations and management. Controlling vehicle entry and exit still heavily relies on human effort, leading to errors in recording license plates, entry times, or parking slot statuses. As the number of vehicles increases, manual management becomes difficult, inaccurate, and time-consuming.

Key issues include:
- Difficulty in quickly checking the availability of individual parking slots.
- Manual recording of vehicle entry/exit is prone to confusing license plates or times.
- Data regarding images, license plates, and parking lot status is not centrally managed.
- It is difficult for managers to track the historical activity of vehicles.
- Scaling the system when the number of cameras, sensors, or parking slots increases is challenging.
- Building a custom system can be expensive if physical servers need to be invested in.

### 2.2. Proposed Solution

The project proposes building a smart Parking IoT system on the AWS Serverless platform. The system uses ESP32 Cameras to capture images of entering/exiting vehicles, and ESP32 Sensors to record the status of parking slots, then sends the data to AWS for processing and centralized storage.

**The solution includes the following main functions:**
- **ESP32 Camera** captures images of vehicles when they enter or leave the lot.
- **ESP32 Sensors** detect the status of each parking slot.
- Vehicle images are uploaded to **Amazon S3** via Presigned URLs.
- **AWS Lambda** processes events when new images are uploaded to S3.
- **Amazon Rekognition** analyzes images and assists in recognizing license plates.
- **DynamoDB** stores vehicle information, license plates, timestamps, statuses, and sensor data.
- **Web/App** allows users to log in, view parking lot status, and track vehicle entry/exit history.
- **Amazon Cognito** supports user authentication and authorization.
- **Amazon Bedrock** provides an AI layer to analyze data and answer intelligent questions.
- **Amazon CloudWatch** monitors logs, errors, and the operational status of the system.

### 2.3. Expected Outcomes

The system reduces manual operations, increases accuracy in parking management, supports real-time monitoring, and creates a data foundation for future AI analysis. By leveraging the Serverless architecture, the system can scale flexibly based on the number of devices, vehicles, and actual usage demand.

### 2.4. Project Scope

Defining the scope ensures the project focuses on core functionalities and remains feasible during deployment:
- **In Scope:** AI-based license plate recognition, tracking parking slot status using sensors, auto-logging entry/exit history, gate opening decisions, displaying a monitoring dashboard on a Web App, and supporting queries via Bedrock virtual assistant.
- **Out of Scope:** Online parking fee payment modules are not integrated yet, and there is no native Mobile App developed (focusing entirely on the Web App platform).

### 2.5. Specific Objectives (KPIs)

The project sets measurable technical targets to evaluate its success:
- **Latency:** The time from capturing an image to storing data, analyzing the license plate, and sending the open-gate command is under 2-3 seconds.
- **Accuracy:** The license plate recognition accuracy (Confidence score) exceeds 95% under good lighting conditions.
- **Reliability:** The AWS Serverless infrastructure ensures up to 99.9% uptime and scales automatically during traffic spikes.

---

## 3. Solution Architecture

The system applies the **AWS Serverless** architecture to reduce infrastructure management costs, increase scalability, and easily integrate with AI, IoT, and database services on AWS.

*Overall Architecture Diagram (AWS Serverless Architecture):*

![Overall Architecture - Smart Parking IoT](/images/2-Proposal/2-proposal-architecture.png)

### 3.1. Key AWS Services

| Module | AWS Service | Function |
| :--- | :--- | :--- |
| **User Interface** | Amazon Route 53 <br> Amazon CloudFront <br> AWS WAF <br> Amazon S3 Static Website | Domain management. <br> Website content distribution. <br> Protect website from malicious access. <br> Host static Web/App interface. |
| **Authentication & Authorization** | Amazon Cognito <br> IAM | Manage login, authentication. <br> Manage access permissions between services. |
| **API & Backend** | Amazon API Gateway <br> AWS Lambda | Receive requests from Web/App/Devices. <br> Handle core business logic, image processing, sensor data, and AI. |
| **IoT & Edge Devices** | AWS IoT Core <br> ESP32 Camera / Sensors | Receive MQTT data from IoT devices. <br> Collect images and parking slot statuses. |
| **Storage & Database** | Amazon S3 <br> Amazon DynamoDB | Store vehicle images. <br> Store license plate data, history, and parking slot statuses. |
| **Image Processing & AI** | Amazon Rekognition <br> Amazon Bedrock | Analyze images, recognize license plates. <br> Support data analysis, intelligent queries. |
| **System Monitoring** | Amazon CloudWatch | Log recording, error tracking, monitoring related components. |

---

## 4. System Operational Flow

### 4.1. Web/App Access Flow

Users access the system through a web browser or mobile device. The website is hosted on Amazon S3 Static Website and distributed via Amazon CloudFront.

```text
User → Route 53 → CloudFront → AWS WAF → Amazon S3 Static Website → API Gateway → Lambda Backend → DynamoDB
```

### 4.2. User Authentication Flow

The system uses Amazon Cognito to authenticate users. Cognito issues a token that the Web/App includes in requests to the API Gateway.

```text
User → Amazon Cognito → API Gateway (Cognito Authorizer) → Lambda Backend → DynamoDB
```

### 4.3. Gate Area Wiring Diagram (ESP32 Camera)

The gate area is equipped with an ESP32 microcontroller combined with a Camera module to recognize vehicles entering and exiting the parking lot.

![Gate Wiring Diagram](/images/2-Proposal/1.Smart%20Parking%20Gate%20Wiring%20-%20English.png)

**Example of historical vehicle entry/exit data stored:**
```json
{
  "plate_number": "29A17938",
  "timestamp": 1782032316749,
  "allow_open": true,
  "bucket": "smart-parking-images-075647413376-ap-southeast-1-an",
  "camera_id": "gate-in-01",
  "confidence": 98.23,
  "created_at": "2026-06-21T15:58:36.749547+07:00",
  "device_id": "gate-in-01",
  "direction": "IN",
  "display_plate_number": "29A-179.38",
  "event_id": "evt_29A17938_1782032316749_IN_21668d9a",
  "image_key": "parking/in/photo-1782032314126-8770cde7.jpg",
  "raw_plate_number": "29A-179.38",
  "status": "ALLOWED",
  "vehicle_type": "GUEST"
}
```

### 4.4. Parking Area Wiring Diagram (ESP32 Sensors)

The parking slots are equipped with sensors (ultrasonic/infrared) connected to ESP32 microcontrollers to track availability status (empty/occupied).

![Parking Area Wiring Diagram](/images/2-Proposal/2.Parking%20Area%20Wiring%20-%20English.png)

**Example of sensor data stored for each parking slot:**
```json
{
  "slot_id": "A1",
  "distance_cm": 2.8,
  "is_occupied": 1,
  "sensor_id": "esp-slot-01",
  "threshold_cm": 3.5,
  "updated_at": "2026-07-09T17:33:56.017039+07:00",
  "zone": "Zone_A",
  "zone_id": "A"
}
```

### 4.5. AI Service Processing Flow

The system integrates an AI layer to help users and administrators query parking lot data using natural language.

```text
Web/App → API Gateway → Lambda AI Service → Amazon Bedrock → DynamoDB → Web/App
```

### 4.6. System Monitoring Flow

Amazon CloudWatch is used to record logs and monitor the activities of all services.

```text
API Gateway / Lambda / IoT Core / Rekognition / DynamoDB → CloudWatch
```

---

## 5. Technical Implementation

| Phase | Content |
| :--- | :--- |
| **Phase 1: Analysis & Design** | Determine deployment scope, number of cameras/sensors, design architecture diagram, and database schema. |
| **Phase 2: IoT Deployment** | Configure ESP32 Cameras for taking photos and ESP32 Sensors for MQTT connection with AWS IoT Core. |
| **Phase 3: AWS Backend** | Create API Gateway, Lambda Functions, S3 Buckets, DynamoDB tables, and integrate Rekognition. |
| **Phase 4: Web/App Development** | Develop the user interface, integrate Cognito authentication, and display parking lot status. |
| **Phase 5: AI & Monitoring** | Configure Amazon Bedrock, set up CloudWatch logging, and Alarms. |

---

## 6. Budget Estimation

### 6.1. Hardware Costs
- **ESP32 Camera**: Based on the number of entry/exit gates.
- **ESP32 Sensors & Ultrasonic Sensors**: Based on the number of parking slots.
- **Accessories**: Power supply, wiring, protective housing, Router/WiFi.

### 6.2. AWS Service Costs (Pay-as-you-go)
- **Compute & Processing**: AWS Lambda, Amazon Rekognition, Amazon Bedrock.
- **Storage**: Amazon S3 (Images), Amazon DynamoDB (Data).
- **Networking & API**: AWS IoT Core, Amazon API Gateway, Amazon CloudFront.
- **Management**: Amazon Cognito, Amazon CloudWatch, AWS Budgets.

---

## 7. Risk Assessment & Mitigation

| Risk | Severity | Mitigation Plan |
| :--- | :--- | :--- |
| **Device loses network connection** | Medium | Temporarily store data locally and resend when the network is restored. |
| **Blurry license plate images** | High | Adjust camera angle, lighting, and shooting distance. |
| **Incorrect license plate recognition** | Medium | Combine with manual verification and improve image quality. |
| **AWS Service Error (Lambda, API)** | Medium | Monitor CloudWatch Alarms for timely handling. |
| **Exceeding AWS budget** | Medium | Set up AWS Budgets for automated alerts. |

---

## 8. Conclusion

The **Smart Parking IoT** project using AWS Serverless is an appropriate solution for modernizing parking lot management. The combination of **IoT, Serverless, and AI (Rekognition, Bedrock)** creates an automated, highly accurate, and infinitely scalable management platform without the need to maintain physical servers.