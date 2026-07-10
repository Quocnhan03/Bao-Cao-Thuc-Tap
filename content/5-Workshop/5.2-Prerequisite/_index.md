---
title: "Prerequisites"
date: 2026-04-26
weight: 2
chapter: false
pre: " <b> 4.2. </b> "
---

### 4.2. Prerequisites

To deploy the Smart Parking IoT system on the AWS environment, the preparation of hardware resources, software tools, and the configuration of required access permissions are conducted as follows.

#### 1. AWS Account
- An active AWS account is utilized to deploy all resources.
- The deployment region is selected as **`ap-southeast-1` (Singapore)** to optimize connection speed and minimize latency between the ESP32 devices and the Cloud.
- The account must have AdministratorAccess or appropriate permissions to create related resources (IAM Roles, S3, IoT Core, Lambda, API Gateway, DynamoDB, Bedrock).

---

#### 2. Hardware Preparation

Below is the list of hardware devices used to connect and build the parking lot model:

| Component | Quantity | Role in the System |
| :--- | :---: | :--- |
| **ESP32-CAM (with programmer)** | 2 | Placed at the entry and exit gates to capture vehicle photos and upload them to S3 |
| **ESP32-S3 DevKitC-1 v1.1** | 1 | Central microcontroller at the parking slots to process data from the ultrasonic sensors |
| **HC-SR04 Ultrasonic Sensor** | 6 | Measures distance at 6 parking slots (A1-A3, B1-B3) to detect empty/occupied status |
| **CD74HC4050 Level Shifter IC** | 1 | Hex buffer/converter to shift the 5V Echo signals from the 6 ultrasonic sensors down to a safe 3.3V level for the ESP32-S3 GPIO pins |
| **SG90 Servo Motor** | 2 | Simulates barrier gates opening/closing automatically at the entry and exit gates |
| **E18-D80NK IR Proximity Sensor** | 2 | Detects vehicles approaching the entry/exit gates to trigger the ESP32-CAM to take photos |
| **Logic Level Shifter (5V to 3.3V)** | 2 | Converts signal voltages between E18-D80NK (5V) and ESP32-CAM (3.3V) |
| **Breadboard & Jumper Wires** | Several | Connecting the hardware components |
| **LEDs & Resistors** | 2 | Displays Red (occupied) / Green (available) status signals |

---

#### 3. Software Preparation

- **Arduino IDE:** Installed on the computer to write, configure, and upload programs to the ESP32 and ESP32-CAM microcontrollers.
- **Required Libraries in Arduino IDE:**
  - `esp32` board manager: Integrates drivers and compiler support for the ESP32 chip family.
  - `PubSubClient` (by Nick O'Leary): Used for transmitting and receiving MQTT data packets with AWS IoT Core.
  - `ArduinoJson` (version 6.x or newer): Used to format data payloads and parse JSON messages exchanged between the devices and the Cloud.
- **VS Code:** The code editor used to write the backend scripts and business logic for AWS Lambda functions (Python).

---

#### 4. Initialize IAM Service Role for AWS Lambda

To allow the Lambda functions to securely interact with other services like S3, DynamoDB, Rekognition, and Bedrock, a shared IAM Service Role is initialized.

##### Execution Steps:
1. Navigate to the **IAM Console** -> select **Roles** -> click **Create role**.
2. Select **Trusted entity type** as **AWS service**.
3. Select **Use case** as **Lambda** and click **Next**.
4. Attach the following permission policies:
   - `AmazonS3FullAccess` (permission to read/write image data on S3 Bucket)
   - `AmazonDynamoDBFullAccess` (permission to query and update the parking slot statuses)
   - `AmazonRekognitionReadOnlyAccess` (permission to invoke the license plate text detection API)
   - `AmazonBedrockFullAccess` (permission to call large language models for AI queries)
   - `CloudWatchLogsFullAccess` (permission to record runtime logs for monitoring)
5. Name the Role `SmartParking-Lambda-Role`.
6. Click **Create role** to complete the initialization.

---
*Once all hardware, software, and IAM Roles are ready, the next step is: AWS IoT Core & Amazon S3 Configuration.*
