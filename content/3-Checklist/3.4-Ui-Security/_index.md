---
title : "User Interface and Security"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 3.4. </b> "
---

# 3.4. User Interface and Security

This section describes how the user interface and security mechanisms are implemented for the **Smart Parking IoT System**. The Web/App interface allows users to monitor parking slot status, view vehicle entry and exit history, check license plate information, and access system data.

In addition, the system uses security services such as **Amazon Cognito, AWS WAF, IAM, API Gateway Authorizer, and CloudFront HTTPS** to ensure that users are authenticated, data is protected, and AWS services are granted only the required permissions.

---

## 3.4.1. Web/App Interface Overview

The Web/App interface is the main place where users interact with the Parking IoT system. Through this interface, users can view real-time parking data, check the status of each parking slot, and monitor vehicle entry and exit history.

Main features of the interface include:

- User login.
- View total parking slots.
- View available and occupied parking slots.
- View the status of each parking slot.
- View vehicle entry and exit history.
- View vehicle images stored in Amazon S3.
- View recognized license plate information.
- Search vehicles by license plate number.
- View parking activity statistics.
- Send questions to the AI Service if Amazon Bedrock is integrated.

The interface can be developed using HTML/CSS/JavaScript or frameworks such as React and Next.js. After being built, the static files are stored in Amazon S3 and delivered to users through Amazon CloudFront.

---

## 3.4.2. Deploying the Interface with Amazon S3 Static Website

Amazon S3 is used to store the static files of the Web/App interface, including:

- HTML files.
- CSS files.
- JavaScript files.
- Images, icons, and other UI assets.

Interface deployment flow:

```text
Web/App Source Code → Build Project → Upload Static Files to Amazon S3 → CloudFront Delivers Content to Users
```

Example build output structure:

```text
web-app-build/
├── index.html
├── assets/
│   ├── style.css
│   ├── app.js
│   └── logo.png
└── dashboard/
    └── index.html
```

Amazon S3 provides a simple and low-cost way to host the web interface, which is suitable for a serverless architecture.

---

## 3.4.3. Website Distribution with Amazon CloudFront

Amazon CloudFront is used to deliver the Web/App interface to users with faster access speed. CloudFront acts as an intermediary between users and Amazon S3.

Website access flow:

```text
User → Route 53 → CloudFront → Amazon S3 Static Website
```

Roles of CloudFront:

- Improve website access speed.
- Reduce latency for users.
- Support HTTPS for secure connections.
- Reduce direct load on Amazon S3.
- Integrate with AWS WAF to protect the website.

When users access the website, CloudFront retrieves content from S3 and caches it at edge locations. This helps the website respond faster, especially when many users access it at the same time.

---

## 3.4.4. Domain Management with Amazon Route 53

Amazon Route 53 is used to manage the system domain name. Instead of accessing a long CloudFront URL, users can access the system through a friendly domain name.

Example:

```text
parking.example.com → CloudFront Distribution
```

Roles of Route 53:

- Manage DNS for the system.
- Route users to CloudFront.
- Provide a user-friendly website address.
- Support domain configuration for demo or production environments.

Access flow with Route 53:

```text
User enters domain name → Route 53 → CloudFront → S3 Static Website
```

---

## 3.4.5. Website Protection with AWS WAF

AWS WAF is placed in front of CloudFront to protect the website from abnormal or malicious requests. WAF improves system security when the website is public on the Internet.

Website protection flow:

```text
User → Route 53 → CloudFront + AWS WAF → Amazon S3 Static Website
```

AWS WAF can help:

- Block suspicious IP addresses.
- Block requests with abnormal formats.
- Limit the number of requests from one source.
- Protect the website from common web attacks.
- Create rules to filter invalid requests.

In the Parking IoT system, WAF protects the user interface layer before requests are forwarded to the Web/App or API.

---

## 3.4.6. User Authentication with Amazon Cognito

Amazon Cognito is used to authenticate users before allowing them to access parking management features. Users must log in with an assigned account.

Authentication flow:

```text
User → Web/App → Amazon Cognito → Receive Token → API Gateway → Lambda Backend
```

Processing steps:

1. The user opens the Web/App.
2. The user enters a username and password.
3. The Web/App sends login information to Amazon Cognito.
4. Cognito verifies the user information.
5. If login is successful, Cognito returns a token.
6. The Web/App sends the token with requests to API Gateway.
7. API Gateway validates the token using Cognito Authorizer.
8. If the token is valid, the request is forwarded to Lambda Backend.

Amazon Cognito helps the system manage login securely and integrates easily with API Gateway.

---

## 3.4.7. User Authorization

The system can divide users into different roles to control access permissions. Each role is allowed to use different functions in the Web/App.

Example role-based access control:

| Role | Access Permission |
| :--- | :--- |
| User | View parking status and available slots |
| Manager | View vehicle history, statistics, and license plate data |
| Admin | Manage users, configure the system, and access all data |

Authorization helps prevent users from accessing functions that are not suitable for their role. For example, a normal user can only view parking status, while an Admin can manage accounts and system settings.

---

## 3.4.8. API Security with API Gateway Authorizer

API Gateway is the communication gateway between the Web/App and Lambda Backend. To protect APIs, the system uses Cognito Authorizer to verify user tokens before allowing API access.

API security flow:

```text
Web/App → API Gateway → Cognito Authorizer → Lambda Backend → DynamoDB
```

How it works:

1. The Web/App sends a request to API Gateway.
2. The request includes a token from Amazon Cognito.
3. API Gateway validates the token using Cognito Authorizer.
4. If the token is valid, the request is forwarded to Lambda.
5. If the token is invalid, API Gateway rejects the request.

APIs that should be protected:

| API Endpoint | Purpose |
| :--- | :--- |
| `/parking/slots` | Get parking slot status |
| `/vehicle/logs` | View vehicle entry and exit history |
| `/vehicle/search` | Search vehicles by license plate |
| `/ai/query` | Send questions to the AI Service |
| `/admin/users` | Manage users |

This approach helps prevent unauthorized access to parking data.

---

## 3.4.9. Access Control with IAM

IAM is used to control permissions between AWS services. Each service is granted only the required permissions based on the **Least Privilege** principle.

Example IAM permissions:

| Component | Required Permission |
| :--- | :--- |
| Lambda Backend | Read and write DynamoDB data |
| Lambda Image Processing | Read images from S3, call Rekognition, and write to DynamoDB |
| Lambda Presigned URL | Create Presigned URLs for S3 |
| Lambda Sensor Processing | Write sensor data to DynamoDB |
| Lambda AI Service | Read DynamoDB and call Amazon Bedrock |
| API Gateway | Invoke Lambda |
| IoT Rule | Trigger Lambda Sensor Processing |

Important principles:

```text
Do not grant overly broad permissions.
Each Lambda function should only have permissions required for its task.
ESP32 devices should not store AWS Access Keys or Secret Keys directly.
```

IAM helps reduce security risks if a component fails or is accessed without authorization.

---

## 3.4.10. Secure Image Upload with Presigned URL

ESP32 Camera is not given direct AWS permissions to upload images to S3. Instead, the system uses Presigned URLs.

Secure image upload flow:

```text
ESP32 Camera → API Gateway → Lambda creates Presigned URL → ESP32 Camera uploads image to S3
```

Benefits of Presigned URLs:

- No need to store AWS Access Keys on ESP32 Camera.
- The URL is valid only for a short period of time.
- The upload is limited to a specific file or bucket.
- Reduces risk if the device is accessed without authorization.

Example:

```text
The Presigned URL is valid for 5 minutes.
ESP32 Camera can only upload images to the entrance/ or exit/ folder.
```

This method is suitable for IoT systems because edge devices usually have limited resources and should not store sensitive credentials.

---

## 3.4.11. IoT Device Connection Security

For ESP32 sensors, data is sent to AWS IoT Core through MQTT. To secure the connection, each device should have its own certificate and IoT Policy.

Security components include:

- IoT Thing representing the device.
- Device Certificate.
- Private Key.
- IoT Policy.
- Separate MQTT topic for each device.

Example topic:

```text
parking/slot/A01/status
```

Example permission principle:

```text
ESP32 Sensor A01 can only publish to topic parking/slot/A01/status.
ESP32 Sensor B03 can only publish to topic parking/slot/B03/status.
```

Limiting MQTT topics reduces the risk of devices sending incorrect data or being accessed without authorization.

---

## 3.4.12. Overall Security Flow

User access flow:

```text
User → Route 53 → CloudFront → AWS WAF → S3 Static Website → Cognito → API Gateway → Lambda → DynamoDB
```

Image upload flow from ESP32 Camera:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3 → Lambda Image Processing
```

Sensor data flow:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Main security layers:

| Security Layer | AWS Services |
| :--- | :--- |
| Website protection | CloudFront, AWS WAF, HTTPS |
| User authentication | Amazon Cognito |
| API protection | API Gateway Authorizer |
| Service permission control | IAM |
| Secure image upload | Presigned URL |
| IoT device security | IoT Certificate and IoT Policy |
| Security log monitoring | CloudWatch Logs |

---

## 3.4.13. Conclusion

The user interface and security layer allows the Parking IoT system to serve users in a clear, secure, and manageable way. The Web/App interface is hosted on Amazon S3 and distributed through CloudFront, allowing users to access the system quickly and reliably.

Services such as Amazon Cognito, AWS WAF, IAM, API Gateway Authorizer, and Presigned URLs help protect the system from unauthorized access, secure parking data, and control permissions between components. With this design, the system can operate securely, scale easily, and fit well with the AWS Serverless architecture.