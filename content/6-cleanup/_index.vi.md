---
title : "Dọn dẹp tài nguyên"
date :  "`r Sys.Date()`" 
weight : 6
chapter : false
pre : " <b> 6. </b> "
---

# 6. Dọn dẹp tài nguyên

Phần này trình bày quá trình dọn dẹp các tài nguyên AWS sau khi hoàn thành triển khai, kiểm thử hoặc demo hệ thống **Parking IoT thông minh**. Việc dọn dẹp tài nguyên là bước quan trọng nhằm tránh phát sinh chi phí ngoài dự kiến, đặc biệt khi hệ thống sử dụng nhiều dịch vụ như **Amazon S3, AWS Lambda, API Gateway, AWS IoT Core, DynamoDB, Cognito, CloudWatch, CloudFront và WAF**.

Sau khi hệ thống không còn sử dụng hoặc kết thúc quá trình demo, người quản trị cần kiểm tra và xóa các tài nguyên không cần thiết. Việc này giúp tài khoản AWS được quản lý gọn gàng, an toàn và tiết kiệm chi phí.

---

## 6.1. Mục tiêu dọn dẹp tài nguyên

Mục tiêu của việc dọn dẹp tài nguyên là đảm bảo các dịch vụ AWS đã tạo trong quá trình triển khai hệ thống Parking IoT được xóa hoặc tắt khi không còn sử dụng.

Các mục tiêu chính gồm:

- Xóa các tài nguyên không còn cần thiết sau khi demo.
- Tránh phát sinh chi phí từ các dịch vụ AWS.
- Giảm số lượng tài nguyên dư thừa trong tài khoản.
- Hạn chế rủi ro bảo mật từ tài nguyên bị bỏ quên.
- Kiểm tra lại các dịch vụ còn đang hoạt động.
- Đảm bảo hệ thống được dọn dẹp đúng thứ tự để tránh lỗi phụ thuộc giữa các dịch vụ.

Các nhóm tài nguyên cần kiểm tra:

| Nhóm tài nguyên | Dịch vụ liên quan |
| :--- | :--- |
| Lưu trữ | Amazon S3, DynamoDB |
| Xử lý backend | AWS Lambda |
| API | Amazon API Gateway |
| IoT | AWS IoT Core |
| Xác thực | Amazon Cognito |
| Giám sát | CloudWatch Logs, CloudWatch Alarm |
| Bảo mật | IAM Role, WAF |
| Phân phối web | CloudFront, Route 53 nếu có |

Trước khi xóa tài nguyên, cần xác định rõ tài nguyên nào thuộc hệ thống Parking IoT để tránh xóa nhầm tài nguyên của dự án khác.

---

## 6.2. Xóa tài nguyên lưu trữ S3

Amazon S3 được sử dụng để lưu trữ giao diện Web/App tĩnh, hình ảnh xe từ ESP32 Camera và có thể lưu log hệ thống. Vì S3 có thể phát sinh chi phí lưu trữ, cần kiểm tra và xóa các bucket không còn sử dụng.

### 6.2.1. Các S3 Bucket cần kiểm tra

Trong hệ thống Parking IoT, có thể có các bucket sau:

| Bucket | Chức năng |
| :--- | :--- |
| Web Static Bucket | Lưu giao diện Web/App |
| Image Bucket | Lưu ảnh xe từ ESP32 Camera |
| Log Bucket | Lưu session logs hoặc backup logs |
| Deployment Bucket | Lưu file triển khai nếu dùng CDK hoặc framework khác |

Ví dụ:

```text
parking-web-bucket
parking-image-bucket
parking-session-logs
parking-deployment-bucket
```

### 6.2.2. Quy trình xóa dữ liệu trong S3

Trước khi xóa S3 Bucket, cần xóa toàn bộ object bên trong bucket. Nếu bucket còn file, AWS sẽ không cho xóa bucket trực tiếp.

Các bước thực hiện:

1. Truy cập Amazon S3 Console.
2. Chọn bucket cần xóa.
3. Kiểm tra dữ liệu bên trong bucket.
4. Tải xuống dữ liệu quan trọng nếu cần lưu lại.
5. Xóa toàn bộ object trong bucket.
6. Nếu bucket có bật versioning, cần xóa cả các phiên bản object.
7. Sau khi bucket rỗng, tiến hành xóa bucket.

Luồng dọn dẹp S3:

```text
Kiểm tra Bucket → Sao lưu dữ liệu cần thiết → Xóa Object → Xóa Bucket
```

### 6.2.3. Lưu ý khi xóa S3

Một số lưu ý quan trọng:

- Không xóa bucket nếu còn cần dữ liệu ảnh xe hoặc log demo.
- Nếu bucket đang được CloudFront sử dụng, cần kiểm tra CloudFront trước khi xóa.
- Nếu S3 Event đang trigger Lambda, cần xóa hoặc tắt Event Notification.
- Nếu bucket có versioning, cần xóa cả object version.
- Nếu có Lifecycle Rule, cần kiểm tra trước khi xóa bucket.

Ví dụ kết quả mong đợi:

```text
Bucket parking-image-bucket đã được xóa sau khi toàn bộ ảnh xe không còn cần sử dụng.
Bucket parking-web-bucket đã được xóa sau khi giao diện demo không còn hoạt động.
```

---

## 6.3. Xóa Lambda, API Gateway và IoT Core

Sau khi xóa hoặc sao lưu dữ liệu lưu trữ, cần tiếp tục dọn dẹp các dịch vụ xử lý và kết nối như AWS Lambda, API Gateway và AWS IoT Core.

---

### 6.3.1. Xóa AWS Lambda

AWS Lambda được sử dụng để xử lý các chức năng chính của hệ thống Parking IoT. Nếu không còn sử dụng, cần xóa các Lambda Function để tránh tài nguyên dư thừa và log phát sinh thêm.

Các Lambda cần kiểm tra:

| Lambda Function | Chức năng |
| :--- | :--- |
| Lambda API Backend | Xử lý request từ Web/App |
| Lambda Presigned URL | Tạo Presigned URL cho ESP32 Camera |
| Lambda Image Processing | Xử lý ảnh từ S3 |
| Lambda Sensor Processing | Xử lý dữ liệu cảm biến |
| Lambda AI Service | Xử lý chức năng AI nếu có |

Các bước xóa Lambda:

1. Truy cập AWS Lambda Console.
2. Chọn từng Lambda Function thuộc hệ thống Parking IoT.
3. Kiểm tra trigger của Lambda.
4. Gỡ trigger từ S3, API Gateway hoặc IoT Rule nếu có.
5. Xóa Lambda Function.
6. Kiểm tra CloudWatch Logs liên quan đến Lambda.

Ví dụ:

```text
Xóa LambdaImageProcessing sau khi đã gỡ S3 ObjectCreated Trigger.
Xóa LambdaSensorProcessing sau khi đã xóa IoT Rule.
```

---

### 6.3.2. Xóa Amazon API Gateway

API Gateway là nơi nhận request từ Web/App và ESP32 Camera. Nếu không còn sử dụng API, cần xóa API Gateway để tránh nhầm lẫn và giảm tài nguyên dư thừa.

Các API cần kiểm tra:

| API Endpoint | Chức năng |
| :--- | :--- |
| `/parking/slots` | Lấy trạng thái bãi xe |
| `/vehicle/logs` | Lấy lịch sử xe ra/vào |
| `/upload-url` | Tạo Presigned URL |
| `/vehicle/search` | Tìm kiếm biển số |
| `/ai/query` | Gửi câu hỏi đến AI Service |

Các bước xóa API Gateway:

1. Truy cập Amazon API Gateway Console.
2. Chọn API thuộc hệ thống Parking IoT.
3. Kiểm tra stage đang triển khai, ví dụ `dev`, `test`, hoặc `prod`.
4. Kiểm tra API có còn được Web/App sử dụng không.
5. Xóa API hoặc xóa từng stage nếu cần.
6. Kiểm tra lại CloudWatch Logs của API Gateway.

Luồng dọn dẹp API:

```text
Kiểm tra API → Kiểm tra Stage → Gỡ liên kết Lambda → Xóa API Gateway
```

---

### 6.3.3. Xóa AWS IoT Core

AWS IoT Core được sử dụng để nhận dữ liệu từ ESP32 cảm biến thông qua MQTT. Khi hệ thống không còn chạy, cần xóa các tài nguyên IoT để tránh thiết bị tiếp tục gửi dữ liệu vào AWS.

Các tài nguyên IoT cần xóa:

| Tài nguyên IoT | Chức năng |
| :--- | :--- |
| IoT Thing | Đại diện cho thiết bị ESP32 |
| Certificate | Xác thực thiết bị |
| IoT Policy | Cấp quyền publish/subscribe |
| IoT Rule | Chuyển dữ liệu đến Lambda |
| MQTT Topic | Topic dùng cho cảm biến |

Các bước xóa AWS IoT Core:

1. Truy cập AWS IoT Core Console.
2. Xóa IoT Rule dùng để trigger Lambda.
3. Gỡ policy khỏi certificate.
4. Deactivate certificate.
5. Xóa certificate.
6. Xóa IoT Thing đại diện cho thiết bị ESP32.
7. Kiểm tra thiết bị không còn gửi dữ liệu vào AWS.

Ví dụ:

```text
Xóa IoT Rule parkingSlotStatusRule.
Deactivate và xóa certificate của esp32_sensor_01.
Xóa IoT Thing esp32_sensor_01.
```

Lưu ý: Nếu còn thiết bị ESP32 đang chạy, nên tắt thiết bị hoặc xóa thông tin kết nối AWS trong chương trình để tránh gửi dữ liệu thất bại liên tục.

---

## 6.4. Xóa DynamoDB, Cognito, CloudWatch Logs

Sau khi dọn dẹp các dịch vụ xử lý và kết nối, cần tiếp tục xóa cơ sở dữ liệu, dịch vụ xác thực và log hệ thống nếu không còn cần sử dụng.

---

### 6.4.1. Xóa Amazon DynamoDB

DynamoDB lưu trữ dữ liệu chính của hệ thống như trạng thái chỗ đỗ, lịch sử xe ra/vào, dữ liệu cảm biến và session logs.

Các bảng cần kiểm tra:

| Bảng DynamoDB | Dữ liệu |
| :--- | :--- |
| ParkingSlots | Trạng thái từng vị trí đỗ |
| VehicleLogs | Lịch sử xe ra/vào |
| SensorData | Dữ liệu cảm biến |
| SessionLogs | Log theo phiên hoạt động |
| DeviceStatus | Trạng thái thiết bị nếu có |

Các bước xóa DynamoDB:

1. Truy cập Amazon DynamoDB Console.
2. Chọn bảng thuộc hệ thống Parking IoT.
3. Kiểm tra dữ liệu có cần sao lưu không.
4. Export dữ liệu ra S3 nếu cần lưu lại.
5. Xóa từng bảng DynamoDB không còn sử dụng.
6. Kiểm tra lại danh sách bảng sau khi xóa.

Ví dụ:

```text
Export bảng VehicleLogs nếu cần lưu lịch sử xe ra/vào.
Xóa bảng ParkingSlots, SensorData và SessionLogs sau khi hoàn tất demo.
```

---

### 6.4.2. Xóa Amazon Cognito

Amazon Cognito được dùng để quản lý đăng nhập và xác thực người dùng. Nếu không còn dùng Web/App, cần xóa User Pool và App Client để tránh tài nguyên dư thừa.

Các tài nguyên Cognito cần xóa:

| Tài nguyên | Chức năng |
| :--- | :--- |
| User Pool | Quản lý tài khoản người dùng |
| App Client | Cho phép Web/App tích hợp đăng nhập |
| User Group | Phân nhóm quyền User, Manager, Admin |
| Domain Cognito | Domain đăng nhập nếu có |

Các bước xóa Cognito:

1. Truy cập Amazon Cognito Console.
2. Chọn User Pool của hệ thống Parking IoT.
3. Kiểm tra danh sách user nếu cần lưu thông tin.
4. Xóa App Client nếu không còn sử dụng.
5. Xóa User Groups nếu có.
6. Xóa Cognito domain nếu đã cấu hình.
7. Xóa User Pool.

Lưu ý:

```text
Sau khi xóa User Pool, tài khoản người dùng và cấu hình đăng nhập sẽ không thể khôi phục nếu chưa sao lưu.
```

---

### 6.4.3. Xóa CloudWatch Logs và Alarms

CloudWatch Logs lưu log từ Lambda, API Gateway, IoT Core và các dịch vụ khác. Nếu không còn cần kiểm tra log, có thể xóa Log Groups để giảm lưu trữ không cần thiết.

Các Log Groups cần kiểm tra:

| Log Group | Nguồn log |
| :--- | :--- |
| `/aws/lambda/LambdaBackend` | Log Lambda Backend |
| `/aws/lambda/LambdaImageProcessing` | Log xử lý ảnh |
| `/aws/lambda/LambdaSensorProcessing` | Log xử lý cảm biến |
| `/aws/apigateway/parking-api` | Log API Gateway |
| WAF Logs | Log request bị chặn nếu có |

Các bước xóa CloudWatch Logs:

1. Truy cập Amazon CloudWatch Console.
2. Chọn **Log Groups**.
3. Tìm các Log Group liên quan đến hệ thống Parking IoT.
4. Kiểm tra log có cần xuất ra S3 không.
5. Xóa các Log Group không còn sử dụng.
6. Kiểm tra và xóa CloudWatch Alarm nếu có.

Các Alarm cần kiểm tra:

| Alarm | Chức năng |
| :--- | :--- |
| Lambda Error Alarm | Cảnh báo lỗi Lambda |
| API 5xx Alarm | Cảnh báo lỗi API |
| Cost Alarm | Cảnh báo chi phí |
| IoT Data Alarm | Cảnh báo không nhận dữ liệu từ thiết bị |

Ví dụ:

```text
Xóa alarm LambdaImageProcessingError sau khi Lambda đã bị xóa.
Xóa Log Group /aws/lambda/LambdaSensorProcessing nếu không còn cần lưu log.
```

---

## 6.5. Kiểm tra chi phí sau khi dọn dẹp

Sau khi xóa tài nguyên, cần kiểm tra lại phần Billing để đảm bảo không còn dịch vụ phát sinh chi phí không mong muốn.

### 6.5.1. Kiểm tra AWS Billing

Các bước kiểm tra:

1. Truy cập AWS Billing and Cost Management.
2. Chọn **Bills** để xem chi phí theo từng dịch vụ.
3. Chọn **Cost Explorer** để xem biểu đồ chi phí.
4. Kiểm tra các dịch vụ đã dùng trong dự án Parking IoT.
5. Xác định dịch vụ nào vẫn còn phát sinh chi phí.
6. Quay lại dịch vụ đó để kiểm tra tài nguyên còn sót.

Các dịch vụ cần kiểm tra chi phí:

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

### 6.5.2. Kiểm tra tài nguyên còn sót

Sau khi dọn dẹp, có thể vẫn còn một số tài nguyên bị bỏ sót như CloudWatch Logs, IAM Role, CloudFront Distribution hoặc S3 Bucket chưa xóa hết object.

Các tài nguyên thường bị quên:

| Tài nguyên | Lý do dễ bị bỏ sót |
| :--- | :--- |
| S3 Bucket | Bucket còn object hoặc version |
| CloudWatch Logs | Log Group không tự xóa khi xóa Lambda |
| IAM Role | Role không tự xóa nếu tạo thủ công |
| API Gateway Stage | Stage vẫn còn sau khi xóa Lambda |
| IoT Certificate | Certificate chưa deactivate |
| CloudFront Distribution | Cần disable trước khi xóa |
| WAF Web ACL | Vẫn gắn với CloudFront hoặc API |

Checklist kiểm tra sau dọn dẹp:

```text
[ ] Đã xóa S3 Bucket không cần thiết
[ ] Đã xóa Lambda Function
[ ] Đã xóa API Gateway
[ ] Đã xóa IoT Rule, Thing, Certificate và Policy
[ ] Đã xóa DynamoDB Tables
[ ] Đã xóa Cognito User Pool
[ ] Đã xóa CloudWatch Logs và Alarms
[ ] Đã kiểm tra IAM Roles không còn dùng
[ ] Đã kiểm tra CloudFront và WAF
[ ] Đã kiểm tra Billing sau khi xóa
```

---

### 6.5.3. Theo dõi chi phí sau vài ngày

Một số chi phí AWS có thể cập nhật chậm. Vì vậy, sau khi dọn dẹp, nên kiểm tra lại Billing sau vài giờ hoặc vài ngày để chắc chắn không còn dịch vụ phát sinh chi phí.

Ví dụ:

```text
Sau khi dọn dẹp tài nguyên, kiểm tra Billing lại sau 24 giờ.
Nếu vẫn còn chi phí phát sinh, kiểm tra theo từng dịch vụ trong Cost Explorer.
```

Kết quả mong đợi:

```text
Không còn tài nguyên Parking IoT chạy ngoài ý muốn.
Chi phí AWS không tiếp tục tăng bất thường sau khi dọn dẹp.
```

---

## 6.6. Kết luận

Dọn dẹp tài nguyên là bước cuối cùng nhưng rất quan trọng trong quá trình triển khai hệ thống Parking IoT trên AWS. Sau khi hoàn thành demo hoặc kiểm thử, các tài nguyên không còn sử dụng cần được xóa để tránh phát sinh chi phí và giảm rủi ro bảo mật.

Các tài nguyên cần được kiểm tra bao gồm Amazon S3, AWS Lambda, API Gateway, AWS IoT Core, DynamoDB, Cognito, CloudWatch Logs, CloudFront, WAF và IAM Roles. Ngoài ra, người quản trị cần kiểm tra lại Billing và Cost Explorer để đảm bảo không còn dịch vụ nào tiếp tục phát sinh chi phí ngoài dự kiến.

Việc thực hiện dọn dẹp đúng quy trình giúp tài khoản AWS được quản lý an toàn, gọn gàng và phù hợp với môi trường học tập, thử nghiệm hoặc demo dự án.