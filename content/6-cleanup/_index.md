---
title : "Resource Cleanup"
date :  "`r Sys.Date()`" 
weight : 6
chapter : false
pre : " <b> 6. </b> "
---

# 6. Resource Cleanup

This section presents the process of cleaning up AWS resources after completing the deployment, testing, or demonstration of the **Smart Parking IoT System**. Resource cleanup is an important step to avoid unexpected costs, especially when the system uses multiple services such as **Amazon S3, AWS Lambda, API Gateway, AWS IoT Core, DynamoDB, Cognito, CloudWatch, CloudFront, and AWS WAF**.

After the system is no longer used or after the demonstration is completed, administrators need to check and delete unnecessary resources. This helps keep the AWS account organized, secure, and cost-efficient.

---

## 6.1. Resource Cleanup Objectives

The objective of resource cleanup is to ensure that AWS services created during the deployment of the Parking IoT system are deleted or disabled when they are no longer needed.

The main objectives include:

- Delete resources that are no longer needed after the demonstration.
- Avoid unnecessary AWS costs.
- Reduce unused resources in the AWS account.
- Minimize security risks from forgotten resources.
- Check which services are still running.
- Clean up resources in the correct order to avoid dependency issues.

Resource groups that need to be checked:

| Resource Group | Related Services |
| :--- | :--- |
| Storage | Amazon S3, DynamoDB |
| Backend Processing | AWS Lambda |
| API | Amazon API Gateway |
| IoT | AWS IoT Core |
| Authentication | Amazon Cognito |
| Monitoring | CloudWatch Logs, CloudWatch Alarm |
| Security | IAM Role, AWS WAF |
| Web Distribution | CloudFront, Route 53 if used |

Before deleting resources, administrators should clearly identify which resources belong to the Parking IoT system to avoid deleting resources from other projects.

---

## 6.2. Deleting S3 Storage Resources

Amazon S3 is used to store the static Web/App interface, vehicle images from ESP32 Camera, and possibly system logs. Since S3 may generate storage costs, unused buckets should be checked and deleted.

### 6.2.1. S3 Buckets to Check

In the Parking IoT system, the following buckets may exist:

| Bucket | Function |
| :--- | :--- |
| Web Static Bucket | Stores the Web/App interface |
| Image Bucket | Stores vehicle images from ESP32 Camera |
| Log Bucket | Stores session logs or backup logs |
| Deployment Bucket | Stores deployment files if CDK or another framework is used |

Example:

```text
parking-web-bucket
parking-image-bucket
parking-session-logs
parking-deployment-bucket
```

### 6.2.2. Steps to Delete Data in S3

Before deleting an S3 Bucket, all objects inside the bucket must be deleted. If the bucket still contains files, AWS will not allow the bucket to be deleted directly.

Steps:

1. Open the Amazon S3 Console.
2. Select the bucket that needs to be deleted.
3. Check the data inside the bucket.
4. Download important data if it needs to be saved.
5. Delete all objects inside the bucket.
6. If versioning is enabled, delete all object versions.
7. After the bucket is empty, delete the bucket.

S3 cleanup flow:

```text
Check Bucket → Backup Important Data → Delete Objects → Delete Bucket
```

### 6.2.3. Notes When Deleting S3

Important notes:

- Do not delete the bucket if vehicle images or demo logs are still needed.
- If the bucket is being used by CloudFront, check CloudFront before deleting it.
- If an S3 Event triggers Lambda, disable or delete the Event Notification first.
- If versioning is enabled, delete all object versions.
- If Lifecycle Rules are configured, check them before deleting the bucket.

Expected result:

```text
The parking-image-bucket is deleted after all vehicle images are no longer needed.
The parking-web-bucket is deleted after the demo website is no longer active.
```

---

## 6.3. Deleting Lambda, API Gateway, and IoT Core

After deleting or backing up storage data, the next step is to clean up processing and connection services such as AWS Lambda, API Gateway, and AWS IoT Core.

---

### 6.3.1. Deleting AWS Lambda

AWS Lambda is used to process the main functions of the Parking IoT system. If it is no longer used, Lambda functions should be deleted to avoid unused resources and additional logs.

Lambda functions to check:

| Lambda Function | Function |
| :--- | :--- |
| Lambda API Backend | Handles requests from Web/App |
| Lambda Presigned URL | Creates Presigned URLs for ESP32 Camera |
| Lambda Image Processing | Processes images from S3 |
| Lambda Sensor Processing | Processes sensor data |
| Lambda AI Service | Handles AI features if used |

Steps to delete Lambda:

1. Open the AWS Lambda Console.
2. Select each Lambda Function that belongs to the Parking IoT system.
3. Check the triggers of the Lambda Function.
4. Remove triggers from S3, API Gateway, or IoT Rule if they exist.
5. Delete the Lambda Function.
6. Check CloudWatch Logs related to the Lambda Function.

Example:

```text
Delete LambdaImageProcessing after removing the S3 ObjectCreated Trigger.
Delete LambdaSensorProcessing after deleting the IoT Rule.
```

---

### 6.3.2. Deleting Amazon API Gateway

API Gateway receives requests from the Web/App and ESP32 Camera. If the API is no longer used, it should be deleted to avoid confusion and reduce unused resources.

APIs to check:

| API Endpoint | Function |
| :--- | :--- |
| `/parking/slots` | Gets parking lot status |
| `/vehicle/logs` | Gets vehicle entry and exit history |
| `/upload-url` | Creates Presigned URL |
| `/vehicle/search` | Searches license plate |
| `/ai/query` | Sends questions to AI Service |

Steps to delete API Gateway:

1. Open the Amazon API Gateway Console.
2. Select the API that belongs to the Parking IoT system.
3. Check the deployed stage, such as `dev`, `test`, or `prod`.
4. Check whether the API is still used by the Web/App.
5. Delete the API or delete each stage if needed.
6. Check API Gateway CloudWatch Logs.

API cleanup flow:

```text
Check API → Check Stage → Remove Lambda Integration → Delete API Gateway
```

---

### 6.3.3. Deleting AWS IoT Core

AWS IoT Core is used to receive data from ESP32 sensors through MQTT. When the system is no longer running, IoT resources should be deleted to prevent devices from continuing to send data to AWS.

IoT resources to delete:

| IoT Resource | Function |
| :--- | :--- |
| IoT Thing | Represents ESP32 device |
| Certificate | Authenticates device |
| IoT Policy | Grants publish/subscribe permissions |
| IoT Rule | Forwards data to Lambda |
| MQTT Topic | Topic used by sensors |

Steps to delete AWS IoT Core:

1. Open the AWS IoT Core Console.
2. Delete the IoT Rule that triggers Lambda.
3. Detach the policy from the certificate.
4. Deactivate the certificate.
5. Delete the certificate.
6. Delete the IoT Thing representing the ESP32 device.
7. Check that the device no longer sends data to AWS.

Example:

```text
Delete IoT Rule parkingSlotStatusRule.
Deactivate and delete the certificate of esp32_sensor_01.
Delete IoT Thing esp32_sensor_01.
```

Note: If the ESP32 device is still running, it should be turned off or the AWS connection information should be removed from the program to avoid repeated connection failures.

---

## 6.4. Deleting DynamoDB, Cognito, and CloudWatch Logs

After cleaning up processing and connection services, the next step is to delete the database, authentication service, and system logs if they are no longer needed.

---

### 6.4.1. Deleting Amazon DynamoDB

DynamoDB stores the main data of the system, such as parking slot status, vehicle entry and exit history, sensor data, and session logs.

DynamoDB tables to check:

| DynamoDB Table | Data |
| :--- | :--- |
| ParkingSlots | Status of each parking slot |
| VehicleLogs | Vehicle entry and exit history |
| SensorData | Sensor data |
| SessionLogs | Session activity logs |
| DeviceStatus | Device status if available |

Steps to delete DynamoDB:

1. Open the Amazon DynamoDB Console.
2. Select the table that belongs to the Parking IoT system.
3. Check whether the data needs to be backed up.
4. Export data to S3 if it needs to be saved.
5. Delete each DynamoDB table that is no longer used.
6. Check the table list after deletion.

Example:

```text
Export the VehicleLogs table if vehicle history needs to be saved.
Delete ParkingSlots, SensorData, and SessionLogs after the demo is completed.
```

---

### 6.4.2. Deleting Amazon Cognito

Amazon Cognito is used to manage login and user authentication. If the Web/App is no longer used, the User Pool and App Client should be deleted to avoid unused resources.

Cognito resources to delete:

| Resource | Function |
| :--- | :--- |
| User Pool | Manages user accounts |
| App Client | Allows Web/App login integration |
| User Group | Groups users such as User, Manager, and Admin |
| Cognito Domain | Login domain if configured |

Steps to delete Cognito:

1. Open the Amazon Cognito Console.
2. Select the User Pool of the Parking IoT system.
3. Check the user list if user information needs to be saved.
4. Delete the App Client if it is no longer used.
5. Delete User Groups if they exist.
6. Delete the Cognito domain if configured.
7. Delete the User Pool.

Note:

```text
After deleting the User Pool, user accounts and login configurations cannot be restored unless they were backed up.
```

---

### 6.4.3. Deleting CloudWatch Logs and Alarms

CloudWatch Logs stores logs from Lambda, API Gateway, IoT Core, and other services. If logs are no longer needed, Log Groups can be deleted to reduce unnecessary storage.

Log Groups to check:

| Log Group | Log Source |
| :--- | :--- |
| `/aws/lambda/LambdaBackend` | Lambda Backend logs |
| `/aws/lambda/LambdaImageProcessing` | Image processing logs |
| `/aws/lambda/LambdaSensorProcessing` | Sensor processing logs |
| `/aws/apigateway/parking-api` | API Gateway logs |
| WAF Logs | Blocked request logs if available |

Steps to delete CloudWatch Logs:

1. Open the Amazon CloudWatch Console.
2. Select **Log Groups**.
3. Find Log Groups related to the Parking IoT system.
4. Check whether logs need to be exported to S3.
5. Delete Log Groups that are no longer used.
6. Check and delete CloudWatch Alarms if they exist.

Alarms to check:

| Alarm | Function |
| :--- | :--- |
| Lambda Error Alarm | Alerts Lambda errors |
| API 5xx Alarm | Alerts API errors |
| Cost Alarm | Alerts cost issues |
| IoT Data Alarm | Alerts when no data is received from devices |

Example:

```text
Delete LambdaImageProcessingError alarm after the Lambda function has been deleted.
Delete /aws/lambda/LambdaSensorProcessing Log Group if the logs are no longer needed.
```

---

## 6.5. Checking Costs After Cleanup

After deleting resources, the Billing section should be checked to ensure that no services continue to generate unexpected costs.

### 6.5.1. Checking AWS Billing

Steps:

1. Open AWS Billing and Cost Management.
2. Select **Bills** to view costs by service.
3. Select **Cost Explorer** to view cost charts.
4. Check the services used in the Parking IoT project.
5. Identify any service that is still generating costs.
6. Return to that service to check whether any resources remain.

Services to check for costs:

- Amazon S3.
- AWS Lambda.
- Amazon API Gateway.
- AWS IoT Core.
- Amazon DynamoDB.
- Amazon CloudWatch.
- Amazon Cognito.
- AWS WAF.
- Amazon CloudFront.
- Amazon Rekognition.
- Amazon Bedrock.

---

### 6.5.2. Checking Remaining Resources

After cleanup, some resources may still remain, such as CloudWatch Logs, IAM Roles, CloudFront Distributions, or S3 Buckets that still contain objects.

Common resources that may be forgotten:

| Resource | Why It Is Often Missed |
| :--- | :--- |
| S3 Bucket | Bucket still contains objects or object versions |
| CloudWatch Logs | Log Groups are not automatically deleted when Lambda is deleted |
| IAM Role | Roles are not automatically deleted if created manually |
| API Gateway Stage | Stage may remain after Lambda is deleted |
| IoT Certificate | Certificate has not been deactivated |
| CloudFront Distribution | Must be disabled before deletion |
| WAF Web ACL | Still attached to CloudFront or API |

Post-cleanup checklist:

```text
[ ] Deleted unused S3 Buckets
[ ] Deleted Lambda Functions
[ ] Deleted API Gateway
[ ] Deleted IoT Rules, Things, Certificates, and Policies
[ ] Deleted DynamoDB Tables
[ ] Deleted Cognito User Pool
[ ] Deleted CloudWatch Logs and Alarms
[ ] Checked unused IAM Roles
[ ] Checked CloudFront and WAF
[ ] Checked Billing after cleanup
```

---

### 6.5.3. Monitoring Costs After a Few Days

Some AWS costs may take time to update. Therefore, after cleanup, Billing should be checked again after a few hours or a few days to make sure no services are still generating costs.

Example:

```text
After cleaning up resources, check Billing again after 24 hours.
If costs are still increasing, check each service in Cost Explorer.
```

Expected result:

```text
No Parking IoT resources are running unintentionally.
AWS costs do not continue to increase abnormally after cleanup.
```

---

## 6.6. Conclusion

Resource cleanup is the final but very important step in deploying the Parking IoT system on AWS. After completing the demo or testing process, unused resources should be deleted to avoid unnecessary costs and reduce security risks.

Resources that need to be checked include Amazon S3, AWS Lambda, API Gateway, AWS IoT Core, DynamoDB, Cognito, CloudWatch Logs, CloudFront, WAF, and IAM Roles. In addition, administrators should check Billing and Cost Explorer to ensure that no services continue to generate unexpected costs.

Following a proper cleanup process helps keep the AWS account secure, organized, and suitable for learning, testing, or project demonstration environments.