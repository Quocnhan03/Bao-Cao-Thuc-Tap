---
title : "Workshop Overview"
date : 2026-04-26
weight : 1
chapter : false
pre : " <b> 4.1. </b> "
---

### 4.1. Overview & System Architecture

#### Project Overview

The **Smart Parking IoT System** is built on the AWS Serverless platform to address the challenges of modern parking lot automation. The system integrates edge sensors and cameras to gather vehicle data, processes it automatically in the Cloud, and provides intelligent interaction capability through Artificial Intelligence (AI).

The system is divided into 3 main components:
- **Edge Devices:**
  - **ESP32 Camera:** Positioned at the entry/exit gates to automatically capture vehicle photos and upload them to the Cloud.
  - **ESP32 Sensors:** Utilizes ultrasonic sensors at each parking slot to detect empty/occupied status and transmit the data to the Cloud.
- **AWS Cloud Infrastructure (Backend):** Receives data, processes images using AI (license plate recognition), stores data in the database, and provides API endpoints.
- **User Interface (Frontend):** A real-time dashboard for administrators and an interactive AI chatbot interface powered by Amazon Bedrock.

---

#### Overall Architecture Diagram

*The system adopts a 100% Serverless architecture, scaling automatically based on actual traffic:*

![Overall Architecture Diagram](/images/2-Proposal/2-proposal-architecture.png)

---

#### Hardware Wiring Diagrams

##### 1. Gate Area (ESP32 Camera)
Utilizes an ESP32-CAM microcontroller combined with a proximity sensor/button to trigger image capture and control a servo motor acting as the barrier gate.

![Gate Wiring Diagram](/images/2-Proposal/1.Smart%20Parking%20Gate%20Wiring%20-%20English.png)

##### 2. Parking Area (ESP32 Sensors)
Utilizes an ESP32 microcontroller combined with an HC-SR04 ultrasonic sensor to measure distance and determine if a vehicle is parked in the slot.

![Parking Area Wiring Diagram](/images/2-Proposal/2.Parking%20Area%20Wiring%20-%20English.png)

---

#### List of AWS Services Used

| Service | Role in the System |
| :--- | :--- |
| **AWS IoT Core** | Receives MQTT data packets from ESP32 sensors in the parking lot in real-time. |
| **Amazon S3** | Stores vehicle photos captured at the entry/exit gates. Also hosts the static Web Dashboard. |
| **AWS Lambda** | Handles the core business logic (generating presigned URLs, S3 trigger handling, calling Rekognition, updating DynamoDB, invoking Bedrock). |
| **Amazon Rekognition** | Automatically analyzes vehicle photos to recognize license plate letters and numbers. |
| **Amazon DynamoDB** | NoSQL database storing vehicle entry/exit history and the real-time status of each parking slot. |
| **Amazon API Gateway** | Serves RESTful API endpoints for the Web/App and edge devices. |
| **Amazon Cognito** | Manages authentication and issues access tokens for the Web Dashboard to call APIs securely. |
| **Amazon Bedrock** | Integrates Large Language Models (LLMs) to answer natural language queries about the parking database. |
| **Amazon CloudWatch** | Monitors all system logs, tracks errors, and logs Lambda functions. |
