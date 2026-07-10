---
title: "Giám sát với CloudWatch"
weight: 8
chapter: false
pre: " <b> 5.8. </b> "
---


Phần này trình bày quá trình giám sát hệ thống, kiểm tra logs và đánh giá các cơ chế bảo mật sau khi hệ thống **Parking IoT thông minh** được triển khai. Khác với phần kiến trúc trước đó, chương này tập trung vào quá trình vận hành thực tế, theo dõi lỗi, kiểm tra log, cảnh báo hệ thống và đánh giá mức độ an toàn của các thành phần AWS.

Các dịch vụ chính được sử dụng gồm **Amazon CloudWatch, AWS Lambda, API Gateway, Amazon Cognito, IAM, AWS WAF, AWS Budgets và CloudTrail**. Việc kết hợp các dịch vụ này giúp người quản trị dễ dàng phát hiện lỗi, kiểm soát truy cập và hạn chế phát sinh chi phí ngoài dự kiến.

---

## 5.1. Tổng quan giám sát hệ thống

Giám sát hệ thống là quá trình theo dõi hoạt động của các thành phần trong hệ thống Parking IoT nhằm đảm bảo dữ liệu được truyền, xử lý và hiển thị đúng theo thiết kế.

Trong hệ thống Parking IoT, các thành phần cần được giám sát gồm:

- Thiết bị ESP32 Camera.
- Thiết bị ESP32 cảm biến.
- AWS IoT Core.
- Amazon S3.
- AWS Lambda.
- Amazon API Gateway.
- Amazon DynamoDB.
- Amazon Rekognition.
- Amazon Cognito.
- AWS WAF.
- Amazon CloudWatch.

Luồng giám sát tổng quát:

```text
ESP32 / Web-App / API Gateway / Lambda / IoT Core / DynamoDB → CloudWatch Logs
```

Mục tiêu của giám sát hệ thống:

- Phát hiện lỗi khi ESP32 gửi dữ liệu thất bại.
- Kiểm tra Lambda có xử lý dữ liệu đúng không.
- Kiểm tra API Gateway có trả response đúng không.
- Theo dõi lỗi 4xx và 5xx từ API.
- Kiểm tra dữ liệu có được ghi vào DynamoDB không.
- Theo dõi quá trình upload ảnh lên S3.
- Kiểm tra bảo mật người dùng và quyền truy cập.
- Theo dõi chi phí sử dụng AWS.

Việc giám sát giúp hệ thống hoạt động ổn định hơn và hỗ trợ người quản trị xử lý lỗi nhanh chóng khi có sự cố.

---

## 5.2. Giám sát CloudWatch Logs

Amazon CloudWatch Logs là dịch vụ chính được sử dụng để ghi nhận log từ các dịch vụ AWS. Trong hệ thống Parking IoT, CloudWatch giúp theo dõi quá trình thực thi của Lambda, request từ API Gateway và lỗi phát sinh trong quá trình xử lý dữ liệu.

Các nguồn log chính:

| Thành phần | Nội dung log |
| :--- | :--- |
| Lambda Backend | Request từ Web/App, truy vấn DynamoDB, lỗi xử lý |
| Lambda Presigned URL | Quá trình tạo URL upload ảnh cho ESP32 Camera |
| Lambda Image Processing | Xử lý ảnh từ S3, gọi Rekognition |
| Lambda Sensor Processing | Xử lý dữ liệu cảm biến từ AWS IoT Core |
| API Gateway | Request, response, mã lỗi 4xx/5xx |
| AWS IoT Core | Dữ liệu MQTT từ ESP32 cảm biến |
| AWS WAF | Request bị chặn hoặc request bất thường |

Luồng ghi log:

```text
API Gateway / Lambda / IoT Core / WAF → Amazon CloudWatch Logs
```

Ví dụ log xử lý thành công:

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

Ví dụ log lỗi:

```json
{
  "request_id": "REQ002",
  "function": "LambdaImageProcessing",
  "status": "failed",
  "error_message": "Access denied when reading image from S3",
  "timestamp": "2026-04-27T10:35:00"
}
```

Các bước kiểm tra log trong CloudWatch:

1. Truy cập Amazon CloudWatch.
2. Chọn **Log Groups**.
3. Chọn Log Group của Lambda hoặc API Gateway cần kiểm tra.
4. Mở Log Stream gần nhất.
5. Kiểm tra thông tin request, response hoặc lỗi.
6. Xác định nguyên nhân lỗi và tiến hành xử lý.

CloudWatch Logs giúp người quản trị truy vết lỗi theo từng bước xử lý, từ lúc request được gửi đến khi dữ liệu được ghi vào DynamoDB.

---

## 5.3. Kiểm tra lỗi Lambda và API Gateway

AWS Lambda và Amazon API Gateway là hai thành phần quan trọng trong hệ thống. API Gateway tiếp nhận request từ Web/App hoặc ESP32 Camera, sau đó chuyển request đến Lambda để xử lý. Vì vậy, cần kiểm tra kỹ lỗi ở hai thành phần này.

### 5.3.1. Kiểm tra lỗi AWS Lambda

Các Lambda cần kiểm tra gồm:

| Lambda Function | Vai trò |
| :--- | :--- |
| Lambda API Backend | Xử lý request từ Web/App |
| Lambda Presigned URL | Tạo Presigned URL cho ESP32 Camera |
| Lambda Image Processing | Xử lý ảnh từ S3 và gọi Rekognition |
| Lambda Sensor Processing | Xử lý dữ liệu cảm biến từ AWS IoT Core |
| Lambda AI Service | Xử lý truy vấn AI nếu có dùng Bedrock |

Các lỗi Lambda thường gặp:

| Lỗi | Nguyên nhân |
| :--- | :--- |
| Timeout | Lambda xử lý quá lâu |
| Access Denied | Thiếu quyền IAM |
| Invalid Payload | Dữ liệu gửi vào sai định dạng |
| DynamoDB Error | Lỗi ghi hoặc đọc dữ liệu |
| S3 Access Error | Lambda không đọc được ảnh từ S3 |
| Rekognition Error | Lỗi khi gọi dịch vụ nhận diện ảnh |

Ví dụ kiểm tra lỗi Lambda:

```text
CloudWatch → Log Groups → /aws/lambda/LambdaImageProcessing → Log Stream → Kiểm tra ERROR
```

Ví dụ log lỗi Lambda:

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

Cách xử lý:

- Kiểm tra dữ liệu đầu vào.
- Kiểm tra quyền IAM Role của Lambda.
- Kiểm tra timeout và memory của Lambda.
- Kiểm tra kết nối đến DynamoDB, S3 hoặc Rekognition.
- Ghi log chi tiết để dễ truy vết lỗi.

### 5.3.2. Kiểm tra lỗi API Gateway

API Gateway là nơi tiếp nhận request từ Web/App và ESP32 Camera. Các lỗi API Gateway thường thể hiện qua mã trạng thái HTTP.

Một số mã lỗi phổ biến:

| Mã lỗi | Ý nghĩa |
| :--- | :--- |
| 400 | Request sai định dạng |
| 401 | Chưa xác thực |
| 403 | Không có quyền truy cập |
| 404 | Sai endpoint |
| 500 | Lỗi từ Lambda Backend |
| 504 | Request timeout |

Ví dụ lỗi API:

```json
{
  "request_id": "REQ003",
  "endpoint": "/parking/slots",
  "method": "GET",
  "status_code": 500,
  "error_message": "Internal server error"
}
```

Luồng kiểm tra lỗi API:

```text
Web/App → API Gateway → Lambda Backend → CloudWatch Logs
```

Các bước kiểm tra:

1. Kiểm tra endpoint có đúng không.
2. Kiểm tra method là GET, POST, PUT hay DELETE.
3. Kiểm tra request có token Cognito không.
4. Kiểm tra API Gateway có gọi đúng Lambda không.
5. Kiểm tra log của Lambda trong CloudWatch.
6. Kiểm tra response trả về cho Web/App.

Việc kiểm tra Lambda và API Gateway giúp đảm bảo Web/App có thể lấy dữ liệu chính xác và ESP32 Camera có thể xin Presigned URL thành công.

---

## 5.4. Kiểm tra bảo mật Cognito, IAM và WAF

Bảo mật là phần quan trọng trong hệ thống Parking IoT vì hệ thống có dữ liệu người dùng, hình ảnh xe, biển số xe và dữ liệu trạng thái bãi đỗ. Các dịch vụ chính được sử dụng để bảo vệ hệ thống gồm **Amazon Cognito, IAM và AWS WAF**.

---

### 5.4.1. Kiểm tra bảo mật Amazon Cognito

Amazon Cognito được sử dụng để xác thực người dùng trước khi truy cập vào các API quan trọng.

Luồng xác thực:

```text
User → Web/App → Amazon Cognito → Token → API Gateway → Lambda Backend
```

Các nội dung cần kiểm tra:

- Người dùng có đăng nhập thành công không.
- Token có được tạo sau khi đăng nhập không.
- API Gateway có kiểm tra token bằng Cognito Authorizer không.
- Token hết hạn có bị từ chối không.
- Người dùng không đăng nhập có bị chặn khi gọi API không.

Ví dụ kiểm thử không có token:

```text
User gọi API /vehicle/logs nhưng không có Cognito Token → API Gateway từ chối request
```

Kết quả mong đợi:

```text
Request không hợp lệ bị từ chối.
Chỉ người dùng đăng nhập hợp lệ mới được gọi API bảo vệ.
```

---

### 5.4.2. Kiểm tra phân quyền IAM

IAM được dùng để kiểm soát quyền truy cập giữa các dịch vụ AWS. Mỗi Lambda hoặc dịch vụ chỉ nên được cấp quyền đúng với nhiệm vụ của nó.

Ví dụ phân quyền IAM:

| Thành phần | Quyền cần có |
| :--- | :--- |
| Lambda Backend | Đọc/ghi DynamoDB |
| Lambda Presigned URL | Tạo Presigned URL upload S3 |
| Lambda Image Processing | Đọc ảnh S3, gọi Rekognition, ghi DynamoDB |
| Lambda Sensor Processing | Ghi dữ liệu cảm biến vào DynamoDB |
| API Gateway | Gọi Lambda |
| IoT Rule | Kích hoạt Lambda |

Nguyên tắc kiểm tra IAM:

```text
Không cấp quyền AdministratorAccess cho Lambda.
Không lưu Access Key và Secret Key trực tiếp trong ESP32.
Mỗi Lambda chỉ có quyền đúng với nhiệm vụ cần thực hiện.
```

Ví dụ lỗi do thiếu quyền IAM:

```json
{
  "error": "AccessDeniedException",
  "message": "Lambda is not authorized to access DynamoDB table"
}
```

Cách xử lý:

- Kiểm tra IAM Role gắn với Lambda.
- Kiểm tra Policy có quyền đọc/ghi đúng tài nguyên không.
- Không dùng quyền quá rộng.
- Áp dụng nguyên tắc Least Privilege.

---

### 5.4.3. Kiểm tra bảo mật AWS WAF

AWS WAF được sử dụng để bảo vệ lớp website và API khỏi các request bất thường. WAF thường được gắn với CloudFront để lọc request trước khi request đi vào hệ thống.

Luồng bảo vệ:

```text
User → CloudFront + AWS WAF → S3 Static Website / API Gateway
```

Các nội dung cần kiểm tra:

- WAF có được gắn với CloudFront không.
- Rule chặn IP bất thường có hoạt động không.
- Rule giới hạn request có hoạt động không.
- Request bị chặn có được ghi log không.
- Có phát hiện request bất thường hay không.

Ví dụ rule bảo mật:

```text
Chặn request từ IP đáng ngờ.
Giới hạn số lượng request quá nhiều trong thời gian ngắn.
Chặn request có mẫu tấn công phổ biến.
```

Kết quả mong đợi:

```text
Các request không hợp lệ hoặc bất thường bị WAF chặn trước khi vào hệ thống.
```

---

## 5.5. Cảnh báo hệ thống và chi phí

Ngoài việc kiểm tra log thủ công, hệ thống cần có cơ chế cảnh báo tự động để người quản trị phát hiện lỗi kịp thời. Các cảnh báo có thể được cấu hình bằng **CloudWatch Alarm, Amazon SNS và AWS Budgets**.

---

### 5.5.1. Cảnh báo lỗi hệ thống bằng CloudWatch Alarm

CloudWatch Alarm được sử dụng để theo dõi các chỉ số bất thường và gửi cảnh báo khi vượt ngưỡng.

Một số cảnh báo nên cấu hình:

| Dịch vụ | Điều kiện cảnh báo |
| :--- | :--- |
| Lambda | Errors > 0 trong 5 phút |
| API Gateway | Tỷ lệ lỗi 5xx tăng cao |
| DynamoDB | Lỗi ghi dữ liệu |
| IoT Core | Không nhận dữ liệu từ thiết bị trong thời gian dài |
| CloudFront/WAF | Nhiều request bị chặn bất thường |

Ví dụ cảnh báo Lambda:

```text
Nếu Lambda Image Processing có Errors > 0 trong 5 phút → gửi cảnh báo email cho quản trị viên.
```

Luồng cảnh báo:

```text
CloudWatch Alarm → Amazon SNS → Email Administrator
```

Ví dụ nội dung cảnh báo:

```text
Alarm: LambdaImageProcessingError
Status: ALARM
Reason: Lambda Image Processing has 3 errors in the last 5 minutes.
```

---

### 5.5.2. Cảnh báo chi phí bằng AWS Budgets

AWS Budgets được sử dụng để theo dõi chi phí và gửi cảnh báo khi chi phí vượt ngưỡng đã cấu hình.

Các dịch vụ cần theo dõi chi phí:

- Amazon S3.
- AWS Lambda.
- API Gateway.
- DynamoDB.
- CloudWatch Logs.
- Rekognition.
- Bedrock.
- CloudFront.
- AWS WAF.

Ví dụ cấu hình ngân sách:

```text
Monthly Budget: 10 USD
Alert 1: 50% budget
Alert 2: 80% budget
Alert 3: 100% budget
```

Luồng cảnh báo chi phí:

```text
AWS Budgets → Email Administrator
```

Lợi ích:

- Tránh phát sinh chi phí ngoài dự kiến.
- Phát hiện dịch vụ sử dụng quá nhiều.
- Phù hợp với môi trường học tập, demo và thử nghiệm.
- Hỗ trợ quản lý ngân sách AWS hiệu quả hơn.

---

## 5.6. Đánh giá kết quả giám sát và bảo mật

Sau khi cấu hình giám sát, logs và bảo mật, cần đánh giá kết quả để xác định hệ thống có hoạt động ổn định và an toàn hay không.

### 5.6.1. Đánh giá kết quả giám sát

Các tiêu chí đánh giá:

| Tiêu chí | Kết quả mong đợi |
| :--- | :--- |
| CloudWatch Logs | Ghi nhận đầy đủ log Lambda và API Gateway |
| Lambda Monitoring | Theo dõi được số lần gọi, lỗi và thời gian xử lý |
| API Gateway Logs | Ghi nhận request, response và mã lỗi |
| IoT Logs | Theo dõi được dữ liệu từ ESP32 cảm biến |
| S3 Processing Logs | Theo dõi được quá trình upload và xử lý ảnh |
| DynamoDB Logs | Phát hiện được lỗi ghi hoặc truy vấn dữ liệu |

Kết quả mong đợi:

```text
Người quản trị có thể kiểm tra toàn bộ luồng xử lý dữ liệu thông qua CloudWatch Logs.
Các lỗi phát sinh được ghi nhận rõ ràng và có thể truy vết theo từng thành phần.
```

---

### 5.6.2. Đánh giá kết quả bảo mật

Các tiêu chí đánh giá bảo mật:

| Thành phần | Kết quả mong đợi |
| :--- | :--- |
| Cognito | Chỉ người dùng hợp lệ mới đăng nhập được |
| API Gateway Authorizer | Chặn request không có token |
| IAM | Mỗi dịch vụ chỉ có quyền cần thiết |
| WAF | Chặn request bất thường |
| Presigned URL | Chỉ upload ảnh trong thời gian cho phép |
| IoT Policy | ESP32 chỉ publish vào topic được cấp quyền |

Ví dụ kết quả kiểm thử bảo mật:

```text
Người dùng không có token không thể gọi API /vehicle/logs.
User thường không thể truy cập API quản trị.
ESP32 Sensor chỉ được gửi dữ liệu vào topic của chính nó.
Presigned URL hết hạn sẽ không còn upload được ảnh.
```

---

### 5.6.3. Đánh giá tổng hợp

Bảng đánh giá tổng hợp:

| Hạng mục | Kết quả đánh giá |
| :--- | :--- |
| Giám sát Lambda | Đạt |
| Giám sát API Gateway | Đạt |
| Giám sát dữ liệu ESP32 | Đạt |
| Ghi log CloudWatch | Đạt |
| Xác thực Cognito | Đạt |
| Phân quyền IAM | Đạt |
| Bảo vệ bằng WAF | Đạt |
| Cảnh báo chi phí | Đạt |

Nhìn chung, hệ thống đã có đầy đủ các lớp giám sát và bảo mật cơ bản. CloudWatch giúp theo dõi hoạt động và lỗi hệ thống, Cognito hỗ trợ xác thực người dùng, IAM kiểm soát quyền giữa các dịch vụ, WAF bảo vệ website khỏi request bất thường và AWS Budgets hỗ trợ kiểm soát chi phí.

---

## 5.7. Kết luận

Phần giám sát, logs và bảo mật giúp hệ thống Parking IoT vận hành ổn định, an toàn và dễ quản trị hơn. Amazon CloudWatch đóng vai trò trung tâm trong việc ghi log, theo dõi lỗi và hỗ trợ truy vết sự cố. API Gateway và Lambda được giám sát để đảm bảo request từ Web/App và ESP32 được xử lý chính xác.

Bên cạnh đó, Amazon Cognito giúp xác thực người dùng, IAM đảm bảo mỗi dịch vụ chỉ có quyền cần thiết, AWS WAF bảo vệ lớp truy cập bên ngoài và AWS Budgets giúp kiểm soát chi phí. Với các cơ chế này, hệ thống Parking IoT có thể giảm rủi ro bảo mật, phát hiện lỗi nhanh hơn và phù hợp với quá trình vận hành thực tế trên AWS.