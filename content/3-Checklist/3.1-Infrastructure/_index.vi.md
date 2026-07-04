---
title : "Hạ tầng cốt lõi AWS"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 3.1 </b> "
---

# 3.1. Hạ tầng cốt lõi AWS

Phần này trình bày quá trình thiết lập hạ tầng AWS nền tảng cho hệ thống **Parking IoT thông minh**. Hạ tầng cốt lõi bao gồm các dịch vụ chính như **Amazon S3, Amazon DynamoDB, AWS Lambda, Amazon API Gateway, AWS IoT Core, IAM, CloudFront, WAF và CloudWatch**.

Hệ thống được xây dựng theo mô hình **AWS Serverless**, giúp giảm nhu cầu quản lý máy chủ, dễ mở rộng khi tăng số lượng thiết bị ESP32, camera, cảm biến hoặc người dùng truy cập Web/App.

---

## 3.1.1. Mục tiêu của hạ tầng cốt lõi

Hạ tầng cốt lõi AWS được xây dựng nhằm đáp ứng các mục tiêu sau:

- Cung cấp môi trường lưu trữ dữ liệu tập trung cho hệ thống Parking IoT.
- Cho phép ESP32 Camera upload ảnh xe lên Amazon S3.
- Cho phép ESP32 cảm biến gửi dữ liệu trạng thái chỗ đỗ lên AWS IoT Core.
- Xử lý dữ liệu bằng AWS Lambda mà không cần quản lý máy chủ.
- Lưu thông tin xe, biển số, trạng thái vị trí đỗ vào DynamoDB.
- Cung cấp API cho Web/App thông qua Amazon API Gateway.
- Đảm bảo bảo mật bằng IAM, Cognito và WAF.
- Theo dõi log, lỗi và hiệu năng hệ thống bằng Amazon CloudWatch.

---

## 3.1.2. Khởi tạo AWS CDK Project

AWS CDK được sử dụng để quản lý hạ tầng dưới dạng mã nguồn, còn gọi là **Infrastructure as Code - IaC**. Thay vì tạo từng dịch vụ thủ công trên AWS Console, nhóm có thể định nghĩa các tài nguyên AWS bằng code và triển khai tự động.

Các công việc chính gồm:

- Cài đặt Node.js và AWS CDK CLI.
- Cấu hình AWS CLI với tài khoản AWS.
- Khởi tạo project CDK bằng TypeScript hoặc Python.
- Tạo các stack cho từng nhóm tài nguyên.
- Triển khai hạ tầng lên AWS bằng lệnh CDK.

Ví dụ cấu trúc project:

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

Các stack chính có thể chia như sau:

| Stack | Chức năng |
| :--- | :--- |
| Storage Stack | Tạo S3 Bucket và DynamoDB |
| API Stack | Tạo API Gateway và Lambda Backend |
| IoT Stack | Tạo IoT Core Rule và Lambda xử lý cảm biến |
| Auth Stack | Tạo Cognito User Pool |
| Monitoring Stack | Tạo CloudWatch Logs và cảnh báo |

Việc sử dụng AWS CDK giúp quá trình triển khai có tính lặp lại, dễ chỉnh sửa và dễ quản lý phiên bản.

---

## 3.1.3. Thiết lập Amazon S3

Amazon S3 được sử dụng với hai mục đích chính trong hệ thống Parking IoT:

- Lưu trữ giao diện Web/App tĩnh.
- Lưu trữ hình ảnh xe được gửi từ ESP32 Camera.

### S3 Static Website

Giao diện Web/App có thể được build thành các file HTML, CSS, JavaScript và upload lên S3 Bucket. Sau đó, CloudFront sẽ phân phối nội dung website đến người dùng.

Luồng truy cập website:

```text
User → Route 53 → CloudFront → S3 Static Website
```

### S3 lưu ảnh xe

Khi ESP32 Camera chụp ảnh xe ra/vào, thiết bị sẽ xin **Presigned URL** từ API Gateway. Sau đó, ESP32 Camera upload ảnh trực tiếp lên S3.

Luồng upload ảnh:

```text
ESP32 Camera → API Gateway → Lambda tạo Presigned URL → Amazon S3
```

Sau khi ảnh được upload thành công, S3 phát sinh sự kiện **ObjectCreated** để kích hoạt Lambda xử lý ảnh.

```text
Amazon S3 → S3 Event ObjectCreated → Lambda xử lý ảnh
```

---

## 3.1.4. Thiết lập Amazon DynamoDB

Amazon DynamoDB được sử dụng làm cơ sở dữ liệu chính của hệ thống. Dữ liệu được lưu theo dạng NoSQL, phù hợp với hệ thống IoT cần ghi dữ liệu nhanh và truy vấn theo thời gian thực.

Các bảng dữ liệu chính gồm:

| Tên bảng | Chức năng |
| :--- | :--- |
| ParkingSlots | Lưu trạng thái từng vị trí đỗ xe |
| VehicleLogs | Lưu lịch sử xe ra/vào |
| SensorData | Lưu dữ liệu cảm biến |
| Users | Lưu thông tin người dùng nếu cần |

Ví dụ dữ liệu bảng `ParkingSlots`:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "updated_at": "2026-04-27T10:30:00"
}
```

Ví dụ dữ liệu bảng `VehicleLogs`:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "direction": "in",
  "image_url": "s3://parking-image-bucket/car_001.jpg",
  "timestamp": "2026-04-27T10:30:00"
}
```

DynamoDB giúp hệ thống truy xuất nhanh dữ liệu trạng thái bãi xe, lịch sử xe ra/vào và kết quả nhận diện biển số.

---

## 3.1.5. Thiết lập AWS Lambda

AWS Lambda là thành phần xử lý chính trong hệ thống. Lambda cho phép chạy code khi có sự kiện xảy ra mà không cần triển khai máy chủ riêng.

Các Lambda Function chính gồm:

| Lambda Function | Chức năng |
| :--- | :--- |
| Lambda API Backend | Xử lý request từ Web/App |
| Lambda Presigned URL | Tạo Presigned URL cho ESP32 Camera upload ảnh |
| Lambda Image Processing | Xử lý ảnh khi có ảnh mới trong S3 |
| Lambda Sensor Processing | Xử lý dữ liệu cảm biến từ AWS IoT Core |
| Lambda AI Service | Kết nối Amazon Bedrock để xử lý chức năng AI |

Luồng Lambda xử lý ảnh:

```text
S3 ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Luồng Lambda xử lý cảm biến:

```text
AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Lambda giúp hệ thống hoạt động linh hoạt, chỉ chạy khi có sự kiện và tự động mở rộng theo số lượng request.

---

## 3.1.6. Thiết lập Amazon API Gateway

Amazon API Gateway được sử dụng làm cổng giao tiếp giữa Web/App, ESP32 Camera và các Lambda Function.

Các API chính có thể gồm:

| API Endpoint | Chức năng |
| :--- | :--- |
| `/parking/slots` | Lấy trạng thái vị trí đỗ xe |
| `/vehicle/logs` | Lấy lịch sử xe ra/vào |
| `/upload-url` | Tạo Presigned URL cho ESP32 Camera |
| `/ai/query` | Gửi câu hỏi đến AI Service |

Luồng Web/App gọi API:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB
```

Luồng ESP32 Camera xin Presigned URL:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

API Gateway giúp hệ thống quản lý request tập trung, dễ kiểm soát quyền truy cập và dễ tích hợp với Cognito Authorizer.

---

## 3.1.7. Thiết lập AWS IoT Core

AWS IoT Core được sử dụng để tiếp nhận dữ liệu từ ESP32 cảm biến thông qua giao thức MQTT.

ESP32 cảm biến gửi dữ liệu trạng thái vị trí đỗ lên topic MQTT, ví dụ:

```text
parking/slot/A01/status
```

Ví dụ payload:

```json
{
  "slot_id": "A01",
  "status": "available",
  "timestamp": "2026-04-27T10:30:00"
}
```

Luồng dữ liệu cảm biến:

```text
ESP32 cảm biến → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

AWS IoT Core giúp quản lý kết nối thiết bị, chứng chỉ bảo mật và dữ liệu MQTT từ các thiết bị IoT.

---

## 3.1.8. Thiết lập VPC và mạng

Trong hệ thống Parking IoT sử dụng kiến trúc serverless, phần lớn dịch vụ như **S3, DynamoDB, IoT Core, Rekognition, Bedrock và CloudWatch** là các dịch vụ AWS được quản lý và không đặt trực tiếp bên trong VPC.

Tuy nhiên, VPC có thể được thiết lập nếu hệ thống cần:

- Chạy Lambda trong mạng riêng.
- Kết nối đến cơ sở dữ liệu nội bộ.
- Tách biệt các thành phần backend.
- Tăng cường kiểm soát luồng mạng.

Một VPC cơ bản có thể gồm:

| Thành phần | Chức năng |
| :--- | :--- |
| Public Subnet | Dành cho tài nguyên cần truy cập Internet |
| Private Subnet | Dành cho Lambda hoặc tài nguyên nội bộ |
| Internet Gateway | Cho phép truy cập Internet từ Public Subnet |
| NAT Gateway | Cho phép tài nguyên trong Private Subnet truy cập Internet |
| Security Group | Kiểm soát lưu lượng ra/vào |

Lưu ý: Trong sơ đồ kiến trúc, không nên đặt các dịch vụ như S3, DynamoDB, CloudWatch, Rekognition hoặc Bedrock bên trong VPC vì đây là các dịch vụ AWS managed services ở cấp vùng.

---

## 3.1.9. Cấu hình IAM Roles và Policies

IAM được sử dụng để phân quyền cho các dịch vụ AWS. Hệ thống áp dụng nguyên tắc **Least Privilege**, tức là mỗi dịch vụ chỉ được cấp quyền tối thiểu cần thiết để thực hiện nhiệm vụ.

Một số quyền cần cấu hình:

| Thành phần | Quyền cần có |
| :--- | :--- |
| Lambda API Backend | Đọc/ghi DynamoDB |
| Lambda Presigned URL | Tạo Presigned URL upload ảnh lên S3 |
| Lambda Image Processing | Đọc ảnh từ S3, gọi Rekognition, ghi DynamoDB |
| Lambda Sensor Processing | Ghi dữ liệu cảm biến vào DynamoDB |
| Lambda AI Service | Gọi Bedrock, đọc dữ liệu DynamoDB |
| API Gateway | Gọi Lambda |
| IoT Rule | Kích hoạt Lambda xử lý cảm biến |

Việc phân quyền rõ ràng giúp hệ thống an toàn hơn, tránh cấp quyền quá rộng và giảm rủi ro khi có lỗi bảo mật.

---

## 3.1.10. Kết luận

Phần hạ tầng cốt lõi AWS là nền tảng quan trọng để hệ thống Parking IoT hoạt động ổn định. Các dịch vụ như S3, DynamoDB, Lambda, API Gateway và IoT Core đảm nhiệm việc lưu trữ, xử lý và truyền dữ liệu giữa thiết bị ESP32 và Web/App.

Bên cạnh đó, IAM giúp kiểm soát quyền truy cập, CloudWatch hỗ trợ giám sát hệ thống, còn CDK giúp triển khai hạ tầng một cách tự động và dễ quản lý. Với kiến trúc serverless, hệ thống có thể mở rộng linh hoạt, tối ưu chi phí và phù hợp với mô hình Parking IoT thông minh.