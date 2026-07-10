---
title: "Resource Cleanup"
date: 2026-04-26
weight: 9
chapter: false
pre: " <b> 4.9. </b> "
---

After completing the workshop experiment and finalizing the report, to avoid unexpected costs from provisioned AWS resources, it is necessary to perform a systematic cleanup in the following order.

---

### 1. Clean Up Distribution & Static Storage (CloudFront & S3)
Since CloudFront and S3 are directly linked, the distribution must be disabled before deleting the Buckets.

1. **Amazon CloudFront**:
   - Navigate to the CloudFront console.
   - Select Distribution ID `EHS22PYCLM5X0`.
   - Click the **Disable** button and wait for the status to change to *Disabled*.
   - After disabling is complete, select the distribution and click **Delete**.
2. **Amazon S3**:
   - S3 does not allow deleting a bucket that still contains data. Therefore, navigate to each bucket:
     - `smart-parking-fe-prod-075647413376-ap-southeast-1-an`
     - `smart-parking-images-075647413376-ap-southeast-1-an`
   - Click **Empty** to delete all static source files and stored license plate images.
   - After the bucket is empty, select the bucket and click **Delete** to remove it completely.

---

### 2. Delete API Endpoints & Authentication Services (API Gateway & Cognito)
1. **Amazon Cognito**:
   - Navigate to the Cognito service, select User Pool `User pool - ahlii` (ID: `ap-southeast-1_syJgrpSKt`).
   - Click **Delete** to remove the entire user account database and associated App Client.
2. **Amazon API Gateway**:
   - Select the REST APIs serving the parking operations.
   - Choose **Actions** -> **Delete** to remove the public Endpoints from the Internet.

---

### 3. Release Logic Layer and Real-time Synchronization (Lambda & AppSync)
1. **AWS AppSync**:
   - Navigate to the AppSync service, select GraphQL API `smart-parking-chat-api`.
   - Choose **Settings** -> **Delete API** to terminate the real-time WebSocket connections of the chat portal.
2. **AWS Lambda**:
   - Select and delete all deployed Lambda functions (e.g., `smart-parking-detect-plate`, `smart-parking-slot-update`, `Get_Parking_Status`, etc.).
3. **IAM Roles**:
   - Navigate to IAM Console -> Roles.
   - Search for and delete the Roles that were granted permissions for Lambda function execution to keep security resources clean.

---

### 4. Delete NoSQL Database (Amazon DynamoDB)
1. **DynamoDB Tables**:
   - Navigate to DynamoDB Console -> Tables.
   - Select the following data tables:
     - `SmartParking_Slots` (Parking slot status)
     - `SmartParking_VehicleHistory` (Vehicle entry/exit log)
     - `SmartParking_ChatLogs` (Chat conversation history)
   - Click **Delete** and confirm deletion (type `delete` in the confirmation field).

---

### 5. Unlink Devices and Routing Rules (IoT Core & CloudWatch)
1. **AWS IoT Core**:
   - **Rules**: Navigate to *Message Routing* -> *Rules*, delete the rules that automatically push data to S3/Lambda.
   - **Things**: Navigate to *Manage* -> *Things*, select the ESP32 devices and delete them.
   - **Certificates**: Deactivate and delete the SSL certificates issued to the ESP32 devices.
2. **Amazon CloudWatch Logs**:
   - Navigate to CloudWatch -> Log Groups.
   - Select the log groups of the old Lambda functions and click **Delete log group** to avoid storing expired logs that incur storage costs.
