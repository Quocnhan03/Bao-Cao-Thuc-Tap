---
title: "System Monitoring with CloudWatch"
date: 2026-04-26
weight: 8
chapter: false
pre: " <b> 4.8. </b> "
---

To maintain system stability, monitor real-time operational performance, and promptly detect errors arising in the Serverless architecture, the system uses the centralized monitoring service **Amazon CloudWatch**. All logging activities from backend and IoT components are aggregated here for monitoring and diagnostics purposes.

---

### 1. Log Groups for AWS Lambda Functions
Each time an AWS Lambda function is triggered to process an event (license plate recognition, sensor-based slot status updates, API authentication), a corresponding **Log Group** is automatically created on Amazon CloudWatch Logs.

Currently, the monitoring system records **13 Log Groups** for core service functions:

![Log Groups list](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-logs.png)
*Evidence 5.8.1: CloudWatch Log Groups management interface for Lambda functions*

---

### 2. Detailed Execution Logs for Each Core Subsystem
To evaluate the operational process in detail, below is the actual configuration evidence and content of Log Events / Log Streams extracted from the Log Groups of all 13 Lambda functions in the system:

#### 2.1. License Plate Recognition Subsystem (`smart-parking-detect-plate`)
This function receives trigger events from S3 when a new image is uploaded, calls Amazon Rekognition for license plate OCR, controls the barrier gate, and saves information to DynamoDB.

- **Selected Log Stream**: `2026/07/09/[$LATEST]a01b705ba4f5495eac53ccc0f4ff250b`

![detect-plate log events](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events.png)
*Evidence 5.8.2: AWS Lambda license plate recognition processing logs*

**Log event analysis**:
- `EVENT`: Records event-driven trigger data from the S3 Bucket (`ObjectCreated:Put`) when a vehicle image is uploaded to the entry gate directory.
- `REKOGNITION`: Results returned from Amazon Rekognition accurately recognized the license plate **`29K-258.17`** with a confidence score of **`97.28%`**.
- `GATE_COMMAND_CREATED`: Generated an `OPEN` gate control command sent to the entry gate controller (`gate-in-01`).
- `SAVED_ITEM`: Successfully saved the record to DynamoDB and set the gate open flag (`"allow_open": true`).
- `REPORT`: Execution completed in **`905.45 ms`** (under 1 second) and consumed a maximum of **`97 MB`** RAM out of the configured `128 MB`.

---

#### 2.2. Sensor Slot Update Subsystem (`smart-parking-slot-update`)
This Lambda function receives distance data from HC-SR04 ultrasonic sensors sent by the ESP32-S3, then analyzes and records the slot status to DynamoDB.

- **Selected Log Stream**: `2026/07/09/[$LATEST]430dc2dcf3dd45b48c7bd615aa5b7429`

![slot-update log events](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-slot-update.png)
*Evidence 5.8.3: Processing logs for parking slot status updates from ultrasonic sensors*

**Log event analysis**:
- `Received event: {"device_id": "esp-slot-01", "slot_id": "A1", "occupied": true, "distance": 2.8}`: Shows that Lambda successfully received the JSON payload from the ESP32-S3 for slot A1 controller with a measured distance of `2.8 cm` (less than the 15cm threshold, determining status as `occupied: true`).
- `REPORT`: DynamoDB write and Lambda response time was extremely fast, taking only **`290.02 ms`** with a maximum RAM consumption of **`94 MB`**.

---

#### 2.3. Parking Status API Subsystem (`Get_Parking_Status`)
A REST API function serving the Web Dashboard to retrieve the current parking slot status list for real-time parking lot map updates.

- **Selected Log Stream**: `2026/07/10/[$LATEST]e81c07f1a4d7411fb09f22dc6689564e`

![Get_Parking_Status log events](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-parking-status.png)
*Evidence 5.8.4: Execution logs for the current parking lot status retrieval API*

**Log event analysis**:
- Logs record numerous connection sessions from the Web Dashboard Client through API Gateway.
- Average API processing time is extremely low, ranging from **`25.74 ms`** to **`58.71 ms`**, ensuring the user interface responds smoothly and nearly instantaneously.
- RAM consumption remains stable at **`97 MB`**.

---

#### 2.4. AI Parking Virtual Assistant Subsystem (`smart-parking-ai-assistant`)
The Lambda function responsible for processing parking assistant chatbot logic, linking RAG data from DynamoDB, and forwarding questions to Amazon Bedrock for inference responses.

- **Selected Log Stream**: `2026/07/09/[$LATEST]ea468fd7a69f4a7082765ba878c8d777`

![ai-assistant log events](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-ai-assistant.png)
*Evidence 5.8.5: Execution logs for AI chatbot processing integrated with Amazon Bedrock*

**Log event analysis**:
- `INIT_START Runtime Version: nodejs:24...`: Running on the Node.js v24 runtime environment.
- `REPORT`: Inference session processing time reached **`2403.76 ms`** (~2.4 seconds). This duration is longer than typical APIs because Lambda must wait for inference results from the Bedrock AI model (Claude/LLaMA) and retrieve RAG context data from DynamoDB.
- Actual RAM consumption reached **`111 MB`** out of the `128 MB` allocated.

---

#### 2.5. Real-time WebSocket Chat Support Subsystem (`OnMessage`)
This function manages the routing and synchronization of real-time messages between customers and administrators through persistent WebSocket connections of API Gateway.

- **Selected Log Stream**: `2026/06/28/[$LATEST]e00925c02c844c6795dc6a7ee6a1e0f6`

![OnMessage log events](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-websocket.png)
*Evidence 5.8.6: Chat message routing logs through WebSocket connections*

**Log event analysis**:
- `INFO Event: { "requestContext": { "routeKey": "sendMessage", "messageId": "gSW-..." } }`: Records the event when a new chat message is sent through the `sendMessage` route. The message is immediately synchronized to the other client via the WebSocket Client connection.
- Average message routing time is only about **`62.52 ms`** to **`90.59 ms`**, ensuring real-time conversations proceed smoothly without latency.

---

#### 2.6. Vehicle History API Subsystem (`Get_Vehicle_History`)
Log group recording requests from the Web Dashboard Client application to retrieve vehicle entry/exit history for users or admins.

![Get_Vehicle_History logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-vehicle-history.png)
*Evidence 5.8.7: Execution log streams for the Get_Vehicle_History API*

---

#### 2.7. WebSocket OnConnect Subsystem (`OnConnect`)
Handles initial WebSocket connection establishment events from the support web chat interface.

![OnConnect logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-onconnect.png)
*Evidence 5.8.8: WebSocket connection execution log streams for OnConnect*

---

#### 2.8. WebSocket OnDisconnect Subsystem (`OnDisconnect`)
Handles WebSocket disconnection events when users close the browser or lose connectivity.

![OnDisconnect logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-ondisconnect.png)
*Evidence 5.8.9: WebSocket disconnection execution log streams for OnDisconnect*

---

#### 2.9. Account Management API Subsystem (`account-api`)
Execution logs for the user information management API, password changes, and license plate registration.

![account-api logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-account-api.png)
*Evidence 5.8.10: Execution log streams for the account-api account management subsystem*

---

#### 2.10. Gate Command Subsystem (`smart-parking-gate-command`)
Handles sending open/close barrier gate control events directly to the ESP32-CAM at the physical station.

![smart-parking-gate-command logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-gate-command.png)
*Evidence 5.8.11: Execution log streams for sending control commands to the barrier gate*

---

#### 2.11. Automatic User Creation Subsystem (`smart-parking-save-user-to-db`)
Automatically triggered when a new account is successfully registered on Cognito to back up the corresponding user account information to DynamoDB.

![smart-parking-save-user-to-db logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-save-user.png)
*Evidence 5.8.12: Log streams for saving newly registered account information*

---

#### 2.12. S3 Image Upload Management Subsystem (`smart-parking-upload-lambda`)
Handles the process of generating Presigned URL signatures and uploading images captured by ESP32-CAM to the S3 storage Bucket.

![smart-parking-upload-lambda logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-upload-lambda.png)
*Evidence 5.8.13: Lambda image upload process log streams to S3*

---

#### 2.13. Vehicle Event Capture Subsystem (`smart-parking-vehicle-event`)
Monitors, processes, and routes vehicle entry/exit status event streams within the parking lot.

![smart-parking-vehicle-event logs](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-vehicle-event.png)
*Evidence 5.8.14: Lambda smart-parking-vehicle-event process log streams*
