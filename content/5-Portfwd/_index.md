---
title : "Monitoring, Logs and Security"
date :  "`r Sys.Date()`" 
weight : 5
chapter : false
pre : " <b> 5. </b> "
---

# 5. Monitoring, Logs and Security

This section presents the process of monitoring the system, checking logs, and evaluating security mechanisms after the **Smart Parking IoT System** has been deployed. Unlike the previous architecture section, this chapter focuses on real operation, error tracking, log checking, system alerts, and security evaluation of AWS components.

The main services used in this section include **Amazon CloudWatch, AWS Lambda, API Gateway, Amazon Cognito, IAM, AWS WAF, AWS Budgets, and CloudTrail**. Combining these services helps administrators detect errors, control access, and reduce unexpected AWS costs.

---

## 5.1. System Monitoring Overview

System monitoring is the process of tracking the operation of components in the Parking IoT system to ensure that data is transmitted, processed, and displayed correctly.

In the Parking IoT system, the main components that need to be monitored include:

- ESP32 Camera devices.
- ESP32 sensor devices.
- AWS IoT Core.
- Amazon S3.
- AWS Lambda.
- Amazon API Gateway.
- Amazon DynamoDB.
- Amazon Rekognition.
- Amazon Cognito.
- AWS WAF.
- Amazon CloudWatch.

General monitoring flow:

```text
ESP32 / Web-App / API Gateway / Lambda / IoT Core / DynamoDB → CloudWatch Logs
```

The main objectives of system monitoring are:

- Detect errors when ESP32 fails to send data.
- Check whether Lambda processes data correctly.
- Check whether API Gateway returns correct responses.
- Monitor 4xx and 5xx errors from APIs.
- Check whether data is written to DynamoDB.
- Monitor the image upload process to S3.
- Check user security and access permissions.
- Monitor AWS usage costs.

Monitoring helps the system operate more reliably and allows administrators to troubleshoot problems quickly.

---

## 5.2. Monitoring CloudWatch Logs

Amazon CloudWatch Logs is the main service used to record logs from AWS services. In the Parking IoT system, CloudWatch helps monitor Lambda execution, API Gateway requests, and errors during data processing.

Main log sources:

| Component | Log Information |
| :--- | :--- |
| Lambda Backend | Requests from Web/App, DynamoDB queries, processing errors |
| Lambda Presigned URL | Presigned URL generation for ESP32 Camera |
| Lambda Image Processing | Image processing from S3 and Rekognition calls |
| Lambda Sensor Processing | Sensor data processing from AWS IoT Core |
| API Gateway | Requests, responses, and 4xx/5xx errors |
| AWS IoT Core | MQTT data from ESP32 sensors |
| AWS WAF | Blocked or abnormal requests |

Log flow:

```text
API Gateway / Lambda / IoT Core / WAF → Amazon CloudWatch Logs
```

Example successful processing log:

```json
{
  "request_id": "REQ001",
  "function": "LambdaSensorProcessing",
  "slot_id": "A01",
  "status": "occupied",
  "result": "Data saved to DynamoDB",
  "timestamp": "2026-04-27T10:30:00"
}
```

Example error log:

```json
{
  "request_id": "REQ002",
  "function": "LambdaImageProcessing",
  "status": "failed",
  "error_message": "Access denied when reading image from S3",
  "timestamp": "2026-04-27T10:35:00"
}
```

Steps to check logs in CloudWatch:

1. Open Amazon CloudWatch.
2. Select **Log Groups**.
3. Choose the Log Group of the Lambda function or API Gateway to check.
4. Open the latest Log Stream.
5. Check request, response, or error information.
6. Identify the cause of the error and handle it.

CloudWatch Logs helps administrators trace errors step by step, from the time a request is sent until data is written to DynamoDB.

---

## 5.3. Checking Lambda and API Gateway Errors

AWS Lambda and Amazon API Gateway are two important components in the system. API Gateway receives requests from the Web/App or ESP32 Camera and forwards them to Lambda for processing. Therefore, errors in these two components must be checked carefully.

### 5.3.1. Checking AWS Lambda Errors

Lambda functions that need to be checked include:

| Lambda Function | Role |
| :--- | :--- |
| Lambda API Backend | Handles requests from Web/App |
| Lambda Presigned URL | Creates Presigned URLs for ESP32 Camera |
| Lambda Image Processing | Processes images from S3 and calls Rekognition |
| Lambda Sensor Processing | Processes sensor data from AWS IoT Core |
| Lambda AI Service | Handles AI queries if Bedrock is used |

Common Lambda errors:

| Error | Possible Cause |
| :--- | :--- |
| Timeout | Lambda takes too long to process |
| Access Denied | Missing IAM permissions |
| Invalid Payload | Input data has an incorrect format |
| DynamoDB Error | Error when reading or writing data |
| S3 Access Error | Lambda cannot read images from S3 |
| Rekognition Error | Error when calling the image recognition service |

Example Lambda error checking flow:

```text
CloudWatch → Log Groups → /aws/lambda/LambdaImageProcessing → Log Stream → Check ERROR
```

Example Lambda error log:

```json
{
  "level": "ERROR",
  "function": "LambdaSensorProcessing",
  "message": "Invalid sensor payload",
  "payload": {
    "slot_id": "",
    "status": "unknown"
  }
}
```

Solutions:

- Check input data.
- Check the IAM Role attached to Lambda.
- Check Lambda timeout and memory settings.
- Check connections to DynamoDB, S3, or Rekognition.
- Add detailed logs for easier troubleshooting.

### 5.3.2. Checking API Gateway Errors

API Gateway receives requests from the Web/App and ESP32 Camera. API Gateway errors are usually shown through HTTP status codes.

Common API status codes:

| Status Code | Meaning |
| :--- | :--- |
| 400 | Invalid request format |
| 401 | Unauthenticated request |
| 403 | Access denied |
| 404 | Incorrect endpoint |
| 500 | Lambda Backend error |
| 504 | Request timeout |

Example API error:

```json
{
  "request_id": "REQ003",
  "endpoint": "/parking/slots",
  "method": "GET",
  "status_code": 500,
  "error_message": "Internal server error"
}
```

API error checking flow:

```text
Web/App → API Gateway → Lambda Backend → CloudWatch Logs
```

Checking steps:

1. Check whether the endpoint is correct.
2. Check whether the HTTP method is GET, POST, PUT, or DELETE.
3. Check whether the request includes a Cognito token.
4. Check whether API Gateway calls the correct Lambda function.
5. Check Lambda logs in CloudWatch.
6. Check the response returned to the Web/App.

Checking Lambda and API Gateway ensures that the Web/App can retrieve data correctly and that ESP32 Camera can request Presigned URLs successfully.

---

## 5.4. Checking Cognito, IAM and WAF Security

Security is important in the Parking IoT system because the system contains user data, vehicle images, license plate data, and parking slot status data. The main services used to protect the system are **Amazon Cognito, IAM, and AWS WAF**.

---

### 5.4.1. Checking Amazon Cognito Security

Amazon Cognito is used to authenticate users before allowing them to access important APIs.

Authentication flow:

```text
User → Web/App → Amazon Cognito → Token → API Gateway → Lambda Backend
```

Items to check:

- Whether users can log in successfully.
- Whether a token is generated after login.
- Whether API Gateway validates the token using Cognito Authorizer.
- Whether expired tokens are rejected.
- Whether unauthenticated users are blocked from calling protected APIs.

Example test without token:

```text
User calls /vehicle/logs API without a Cognito Token → API Gateway rejects the request
```

Expected result:

```text
Invalid requests are rejected.
Only valid authenticated users can call protected APIs.
```

---

### 5.4.2. Checking IAM Permissions

IAM is used to control permissions between AWS services. Each Lambda function or service should only be granted the permissions required for its task.

Example IAM permissions:

| Component | Required Permission |
| :--- | :--- |
| Lambda Backend | Read and write DynamoDB |
| Lambda Presigned URL | Create Presigned URLs for S3 upload |
| Lambda Image Processing | Read S3 images, call Rekognition, write DynamoDB |
| Lambda Sensor Processing | Write sensor data to DynamoDB |
| API Gateway | Invoke Lambda |
| IoT Rule | Trigger Lambda |

IAM checking principles:

```text
Do not grant AdministratorAccess to Lambda.
Do not store Access Key and Secret Key directly in ESP32.
Each Lambda function should only have the permissions required for its task.
```

Example IAM permission error:

```json
{
  "error": "AccessDeniedException",
  "message": "Lambda is not authorized to access DynamoDB table"
}
```

Solutions:

- Check the IAM Role attached to Lambda.
- Check whether the policy allows access to the correct resources.
- Avoid using overly broad permissions.
- Apply the Least Privilege principle.

---

### 5.4.3. Checking AWS WAF Security

AWS WAF is used to protect the website and API layer from abnormal requests. WAF is usually attached to CloudFront to filter requests before they enter the system.

Protection flow:

```text
User → CloudFront + AWS WAF → S3 Static Website / API Gateway
```

Items to check:

- Whether WAF is attached to CloudFront.
- Whether IP blocking rules work correctly.
- Whether rate limiting rules work correctly.
- Whether blocked requests are logged.
- Whether abnormal requests are detected.

Example security rules:

```text
Block suspicious IP addresses.
Limit too many requests in a short period of time.
Block requests that match common attack patterns.
```

Expected result:

```text
Invalid or abnormal requests are blocked by WAF before entering the system.
```

---

## 5.5. System and Cost Alerts

Besides manual log checking, the system should have automatic alerts so administrators can detect issues quickly. Alerts can be configured using **CloudWatch Alarm, Amazon SNS, and AWS Budgets**.

---

### 5.5.1. System Error Alerts with CloudWatch Alarm

CloudWatch Alarm is used to monitor abnormal metrics and send alerts when thresholds are exceeded.

Recommended alarms:

| Service | Alarm Condition |
| :--- | :--- |
| Lambda | Errors > 0 within 5 minutes |
| API Gateway | High 5xx error rate |
| DynamoDB | Data write errors |
| IoT Core | No data received from devices for a long time |
| CloudFront/WAF | Many abnormal blocked requests |

Example Lambda alarm:

```text
If Lambda Image Processing has Errors > 0 within 5 minutes → send an email alert to the administrator.
```

Alert flow:

```text
CloudWatch Alarm → Amazon SNS → Email Administrator
```

Example alert content:

```text
Alarm: LambdaImageProcessingError
Status: ALARM
Reason: Lambda Image Processing has 3 errors in the last 5 minutes.
```

---

### 5.5.2. Cost Alerts with AWS Budgets

AWS Budgets is used to monitor AWS costs and send alerts when spending exceeds configured thresholds.

Services that should be monitored for cost:

- Amazon S3.
- AWS Lambda.
- API Gateway.
- DynamoDB.
- CloudWatch Logs.
- Rekognition.
- Bedrock.
- CloudFront.
- AWS WAF.

Example budget configuration:

```text
Monthly Budget: 10 USD
Alert 1: 50% budget
Alert 2: 80% budget
Alert 3: 100% budget
```

Cost alert flow:

```text
AWS Budgets → Email Administrator
```

Benefits:

- Avoid unexpected costs.
- Detect services with high usage.
- Suitable for learning, demo, and testing environments.
- Support better AWS budget management.

---

## 5.6. Evaluation of Monitoring and Security Results

After configuring monitoring, logs, and security, the results should be evaluated to determine whether the system operates stably and securely.

### 5.6.1. Monitoring Result Evaluation

Evaluation criteria:

| Criteria | Expected Result |
| :--- | :--- |
| CloudWatch Logs | Records complete Lambda and API Gateway logs |
| Lambda Monitoring | Tracks invocations, errors, and processing time |
| API Gateway Logs | Records requests, responses, and status codes |
| IoT Logs | Tracks data from ESP32 sensors |
| S3 Processing Logs | Tracks image upload and image processing |
| DynamoDB Logs | Detects write or query errors |

Expected result:

```text
Administrators can check the entire data processing flow through CloudWatch Logs.
Errors are recorded clearly and can be traced by component.
```

---

### 5.6.2. Security Result Evaluation

Security evaluation criteria:

| Component | Expected Result |
| :--- | :--- |
| Cognito | Only valid users can log in |
| API Gateway Authorizer | Blocks requests without tokens |
| IAM | Each service has only the required permissions |
| WAF | Blocks abnormal requests |
| Presigned URL | Allows image upload only within the allowed time |
| IoT Policy | ESP32 can only publish to authorized topics |

Example security test results:

```text
Users without tokens cannot call /vehicle/logs API.
Normal users cannot access admin APIs.
ESP32 Sensor can only send data to its own topic.
Expired Presigned URLs cannot be used to upload images.
```

---

### 5.6.3. Overall Evaluation

Overall evaluation table:

| Item | Evaluation Result |
| :--- | :--- |
| Lambda Monitoring | Passed |
| API Gateway Monitoring | Passed |
| ESP32 Data Monitoring | Passed |
| CloudWatch Logging | Passed |
| Cognito Authentication | Passed |
| IAM Authorization | Passed |
| WAF Protection | Passed |
| Cost Alerts | Passed |

In general, the system has basic monitoring and security layers. CloudWatch helps monitor system activities and errors, Cognito supports user authentication, IAM controls service permissions, WAF protects the website from abnormal requests, and AWS Budgets helps control costs.

---

## 5.7. Conclusion

The monitoring, logs, and security section helps the Parking IoT system operate more stably, securely, and manageably. Amazon CloudWatch plays a central role in logging, error monitoring, and troubleshooting. API Gateway and Lambda are monitored to ensure that requests from the Web/App and ESP32 devices are processed correctly.

In addition, Amazon Cognito authenticates users, IAM ensures that each service has only the required permissions, AWS WAF protects the external access layer, and AWS Budgets helps control costs. With these mechanisms, the Parking IoT system can reduce security risks, detect errors faster, and better support real operation on AWS.