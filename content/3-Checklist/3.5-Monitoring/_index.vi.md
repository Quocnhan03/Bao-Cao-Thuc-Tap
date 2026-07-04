---
title : "Giám sát và quản trị"
date :  "`r Sys.Date()`" 
weight : 5
chapter : false
pre : " <b> 3.5. </b> "
---

# 3.5. Giám sát và quản trị

Phần này trình bày cách giám sát, ghi log, phát hiện lỗi và quản trị hệ thống **Parking IoT thông minh** sau khi triển khai. Trong hệ thống sử dụng nhiều dịch vụ AWS như **Lambda, API Gateway, AWS IoT Core, Amazon S3, Amazon DynamoDB, Amazon Rekognition và Amazon Bedrock**, việc giám sát là rất quan trọng để đảm bảo hệ thống hoạt động ổn định, dễ phát hiện lỗi và kiểm soát chi phí.

Các dịch vụ chính được sử dụng trong phần giám sát và quản trị gồm:

- **Amazon CloudWatch:** ghi log, theo dõi lỗi và hiệu năng hệ thống.
- **AWS Budgets:** theo dõi và cảnh báo chi phí sử dụng AWS.
- **AWS CloudTrail:** ghi nhận các hành động trong tài khoản AWS.
- **IAM:** kiểm soát quyền truy cập và quản trị bảo mật.
- **DynamoDB Console / S3 Console:** kiểm tra dữ liệu và tài nguyên lưu trữ.

---

## 3.5.1. Mục tiêu giám sát hệ thống

Việc giám sát hệ thống nhằm đảm bảo các thành phần trong kiến trúc Parking IoT hoạt động đúng, dữ liệu được xử lý đầy đủ và người quản trị có thể phát hiện sự cố kịp thời.

Các mục tiêu chính gồm:

- Theo dõi trạng thái hoạt động của Lambda.
- Kiểm tra request từ Web/App đến API Gateway.
- Theo dõi dữ liệu gửi từ ESP32 cảm biến lên AWS IoT Core.
- Kiểm tra quá trình upload ảnh từ ESP32 Camera lên Amazon S3.
- Theo dõi quá trình xử lý ảnh và nhận diện biển số.
- Kiểm tra dữ liệu được ghi vào DynamoDB.
- Phát hiện lỗi trong quá trình xử lý dữ liệu.
- Theo dõi chi phí sử dụng AWS để tránh vượt ngân sách.
- Kiểm tra hoạt động của người dùng và dịch vụ trong tài khoản AWS.

---

## 3.5.2. Giám sát bằng Amazon CloudWatch

Amazon CloudWatch là dịch vụ chính dùng để ghi log và theo dõi hoạt động của hệ thống. Các dịch vụ như Lambda, API Gateway, AWS IoT Core và DynamoDB có thể gửi log hoặc metric về CloudWatch.

Luồng giám sát tổng quát:

```text
API Gateway / Lambda / AWS IoT Core / DynamoDB / Rekognition → Amazon CloudWatch
```

CloudWatch hỗ trợ:

- Ghi log khi Lambda được thực thi.
- Ghi log request từ API Gateway.
- Theo dõi lỗi khi Lambda xử lý thất bại.
- Theo dõi thời gian thực thi của Lambda.
- Theo dõi số lượng request API.
- Kiểm tra lỗi khi ghi dữ liệu vào DynamoDB.
- Hỗ trợ tạo cảnh báo khi hệ thống có dấu hiệu bất thường.

Ví dụ các loại log cần theo dõi:

| Thành phần | Nội dung cần theo dõi |
| :--- | :--- |
| Lambda Backend | Request từ Web/App, lỗi xử lý API |
| Lambda Image Processing | Lỗi đọc ảnh S3, lỗi gọi Rekognition |
| Lambda Sensor Processing | Payload MQTT, lỗi ghi DynamoDB |
| API Gateway | Request, response, lỗi 4xx/5xx |
| AWS IoT Core | Dữ liệu MQTT từ ESP32 |
| DynamoDB | Lỗi ghi dữ liệu hoặc truy vấn dữ liệu |

---

## 3.5.3. Giám sát AWS Lambda

AWS Lambda là thành phần xử lý chính của hệ thống, vì vậy cần theo dõi kỹ các Lambda Function để đảm bảo hệ thống hoạt động ổn định.

Các Lambda cần giám sát gồm:

| Lambda Function | Chức năng |
| :--- | :--- |
| Lambda API Backend | Xử lý request từ Web/App |
| Lambda Presigned URL | Tạo URL upload ảnh cho ESP32 Camera |
| Lambda Image Processing | Xử lý ảnh và gọi Rekognition |
| Lambda Sensor Processing | Xử lý dữ liệu cảm biến từ AWS IoT Core |
| Lambda AI Service | Kết nối Amazon Bedrock để xử lý truy vấn AI |

Các chỉ số cần theo dõi:

- **Invocations:** số lần Lambda được gọi.
- **Errors:** số lần Lambda bị lỗi.
- **Duration:** thời gian thực thi Lambda.
- **Throttles:** số lần Lambda bị giới hạn thực thi.
- **Memory Usage:** mức sử dụng bộ nhớ.
- **Timeout:** lỗi do Lambda chạy quá thời gian cho phép.

Ví dụ luồng kiểm tra lỗi Lambda:

```text
CloudWatch → Log Groups → Chọn Lambda Function → Xem Log Stream → Kiểm tra lỗi
```

Khi phát hiện lỗi, người quản trị cần kiểm tra nội dung log để xác định nguyên nhân, ví dụ lỗi quyền IAM, lỗi dữ liệu đầu vào, lỗi kết nối DynamoDB hoặc lỗi khi gọi Rekognition.

---

## 3.5.4. Giám sát Amazon API Gateway

Amazon API Gateway là cổng giao tiếp giữa Web/App, ESP32 Camera và Lambda Backend. Nếu API Gateway gặp lỗi, người dùng hoặc thiết bị IoT sẽ không thể gửi request đến hệ thống.

Các nội dung cần giám sát:

- Số lượng request đến API.
- Tỷ lệ request thành công.
- Lỗi 4xx do request sai hoặc thiếu quyền.
- Lỗi 5xx do backend Lambda lỗi.
- Thời gian phản hồi API.
- Request từ Web/App và ESP32 Camera.

Các lỗi thường gặp:

| Mã lỗi | Ý nghĩa |
| :--- | :--- |
| 400 | Request sai định dạng |
| 401 | Chưa xác thực |
| 403 | Không có quyền truy cập |
| 404 | Sai endpoint |
| 500 | Lỗi Lambda Backend |
| 504 | Request timeout |

Luồng giám sát API:

```text
API Gateway → CloudWatch Logs → Kiểm tra request và response
```

Việc giám sát API Gateway giúp phát hiện lỗi kết nối giữa giao diện Web/App và backend.

---

## 3.5.5. Giám sát AWS IoT Core

AWS IoT Core được sử dụng để nhận dữ liệu từ ESP32 cảm biến thông qua giao thức MQTT. Vì vậy, cần giám sát quá trình gửi dữ liệu từ thiết bị đến AWS.

Các nội dung cần kiểm tra:

- ESP32 có kết nối được đến AWS IoT Core hay không.
- MQTT topic có đúng định dạng không.
- Payload gửi lên có đầy đủ dữ liệu không.
- IoT Rule có kích hoạt Lambda đúng không.
- Lambda có ghi dữ liệu vào DynamoDB thành công không.

Ví dụ MQTT topic:

```text
parking/slot/A01/status
```

Ví dụ payload hợp lệ:

```json
{
  "device_id": "esp32_sensor_01",
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

Các lỗi thường gặp trong luồng IoT:

| Lỗi | Nguyên nhân có thể |
| :--- | :--- |
| Thiết bị không kết nối được | Sai endpoint, sai certificate hoặc mất WiFi |
| Không nhận được dữ liệu | Sai MQTT topic hoặc thiết bị không publish |
| IoT Rule không chạy | Sai điều kiện rule hoặc thiếu quyền gọi Lambda |
| Lambda không ghi DynamoDB | Thiếu IAM permission hoặc dữ liệu sai định dạng |

Luồng giám sát dữ liệu cảm biến:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda → CloudWatch Logs
```

---

## 3.5.6. Giám sát Amazon S3 và xử lý ảnh

Amazon S3 được sử dụng để lưu ảnh xe từ ESP32 Camera. Khi có ảnh mới được upload, S3 sẽ phát sinh sự kiện ObjectCreated để kích hoạt Lambda xử lý ảnh.

Luồng xử lý ảnh:

```text
ESP32 Camera → Amazon S3 → S3 ObjectCreated → Lambda Image Processing → Rekognition → DynamoDB
```

Các nội dung cần kiểm tra:

- Ảnh có được upload lên S3 thành công không.
- Ảnh có đúng thư mục `entrance/` hoặc `exit/` không.
- S3 Event ObjectCreated có kích hoạt Lambda không.
- Lambda có đọc được ảnh từ S3 không.
- Lambda có gọi Rekognition thành công không.
- Kết quả nhận diện có được ghi vào DynamoDB không.

Ví dụ cấu trúc thư mục ảnh trong S3:

```text
parking-image-bucket/
├── entrance/
│   └── esp32_cam_01_20260427_103000.jpg
└── exit/
    └── esp32_cam_02_20260427_110000.jpg
```

Các lỗi thường gặp:

| Lỗi | Cách kiểm tra |
| :--- | :--- |
| Ảnh không upload được | Kiểm tra Presigned URL và quyền S3 |
| S3 không trigger Lambda | Kiểm tra Event Notification |
| Lambda không đọc được ảnh | Kiểm tra IAM Role của Lambda |
| Rekognition lỗi | Kiểm tra định dạng ảnh và quyền gọi Rekognition |
| Không lưu kết quả | Kiểm tra quyền ghi DynamoDB |

---

## 3.5.7. Giám sát Amazon DynamoDB

Amazon DynamoDB là nơi lưu trữ dữ liệu chính của hệ thống. Các dữ liệu như trạng thái vị trí đỗ, lịch sử xe ra/vào, kết quả nhận diện biển số đều được lưu tại đây.

Các bảng cần giám sát:

| Bảng | Dữ liệu lưu trữ |
| :--- | :--- |
| ParkingSlots | Trạng thái mới nhất của từng vị trí đỗ |
| VehicleLogs | Lịch sử xe ra/vào |
| SensorData | Dữ liệu cảm biến theo thời gian |
| DeviceStatus | Trạng thái hoạt động của thiết bị nếu có |

Các nội dung cần kiểm tra:

- Dữ liệu có được ghi vào bảng đúng không.
- Trạng thái vị trí đỗ có được cập nhật mới nhất không.
- Dữ liệu xe ra/vào có đầy đủ biển số, thời gian và ảnh không.
- Có lỗi ghi dữ liệu từ Lambda không.
- Có cần tối ưu khóa chính và truy vấn không.

Ví dụ dữ liệu bảng `ParkingSlots`:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "updated_at": "2026-04-27T10:30:00",
  "device_id": "esp32_sensor_01"
}
```

Ví dụ dữ liệu bảng `VehicleLogs`:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "direction": "in",
  "image_url": "s3://parking-image-bucket/entrance/car_001.jpg",
  "timestamp": "2026-04-27T10:30:00",
  "confidence": 92.5
}
```

---

## 3.5.8. Giám sát Amazon Rekognition và AI Service

Amazon Rekognition được sử dụng để phân tích ảnh xe và hỗ trợ nhận diện biển số. Amazon Bedrock có thể được sử dụng để hỗ trợ AI Service, giúp người dùng truy vấn dữ liệu bằng ngôn ngữ tự nhiên.

### Giám sát Rekognition

Các nội dung cần kiểm tra:

- Rekognition có được Lambda gọi thành công không.
- Ảnh truyền vào có đúng định dạng không.
- Kết quả nhận diện có độ tin cậy cao không.
- Trường hợp không nhận diện được biển số có được ghi log không.

Ví dụ dữ liệu kết quả:

```json
{
  "plate_number": "51A-12345",
  "confidence": 92.5,
  "status": "recognized"
}
```

### Giám sát AI Service

Luồng AI Service:

```text
Web/App → API Gateway → Lambda AI Service → DynamoDB → Amazon Bedrock → Web/App
```

Các nội dung cần kiểm tra:

- Người dùng có gửi câu hỏi thành công không.
- Lambda AI Service có lấy được dữ liệu từ DynamoDB không.
- Amazon Bedrock có phản hồi đúng không.
- Thời gian phản hồi có quá lâu không.
- Có phát sinh chi phí cao do gọi AI quá nhiều không.

---

## 3.5.9. Cảnh báo lỗi bằng CloudWatch Alarm

CloudWatch Alarm được sử dụng để gửi cảnh báo khi hệ thống có dấu hiệu bất thường. Các cảnh báo giúp người quản trị phát hiện lỗi sớm và xử lý kịp thời.

Một số cảnh báo nên cấu hình:

| Dịch vụ | Điều kiện cảnh báo |
| :--- | :--- |
| Lambda | Số lỗi lớn hơn 0 trong 5 phút |
| API Gateway | Tỷ lệ lỗi 5xx tăng cao |
| IoT Core | Không có dữ liệu từ thiết bị trong thời gian dài |
| DynamoDB | Lỗi ghi dữ liệu |
| CloudWatch Logs | Xuất hiện log lỗi nghiêm trọng |
| AWS Budgets | Chi phí vượt ngưỡng cho phép |

Ví dụ cảnh báo Lambda:

```text
Nếu Lambda Image Processing có Errors > 0 trong 5 phút → gửi cảnh báo cho quản trị viên.
```

Cảnh báo có thể được gửi qua:

- Email.
- Amazon SNS.
- Dashboard quản trị.
- CloudWatch Alarm notification.

---

## 3.5.10. Quản lý chi phí bằng AWS Budgets

AWS Budgets được sử dụng để theo dõi chi phí sử dụng AWS và gửi cảnh báo khi chi phí vượt ngưỡng. Đây là phần quan trọng vì các dịch vụ như Rekognition, Bedrock, S3, API Gateway và CloudWatch đều có thể phát sinh chi phí khi sử dụng nhiều.

Các dịch vụ cần theo dõi chi phí:

- Amazon S3.
- AWS Lambda.
- Amazon API Gateway.
- AWS IoT Core.
- Amazon DynamoDB.
- Amazon Rekognition.
- Amazon Bedrock.
- Amazon CloudWatch.
- Amazon CloudFront.

Ví dụ thiết lập ngân sách:

```text
Ngân sách tháng: 10 USD
Cảnh báo 1: Khi chi phí đạt 50%
Cảnh báo 2: Khi chi phí đạt 80%
Cảnh báo 3: Khi chi phí đạt 100%
```

Lợi ích của AWS Budgets:

- Tránh phát sinh chi phí ngoài dự kiến.
- Theo dõi chi phí theo từng tháng.
- Phát hiện dịch vụ đang sử dụng quá nhiều.
- Hỗ trợ quản lý ngân sách cho môi trường demo hoặc học tập.

---

## 3.5.11. Quản trị bảo mật bằng IAM và CloudTrail

IAM và CloudTrail giúp người quản trị kiểm soát quyền truy cập và theo dõi hoạt động trong tài khoản AWS.

### IAM

IAM được sử dụng để quản lý quyền truy cập giữa các dịch vụ AWS. Hệ thống nên áp dụng nguyên tắc **Least Privilege**, nghĩa là mỗi thành phần chỉ có quyền cần thiết.

Ví dụ:

| Thành phần | Quyền cần có |
| :--- | :--- |
| Lambda Image Processing | Đọc S3, gọi Rekognition, ghi DynamoDB |
| Lambda Sensor Processing | Ghi DynamoDB |
| Lambda AI Service | Đọc DynamoDB, gọi Bedrock |
| API Gateway | Gọi Lambda |
| IoT Rule | Kích hoạt Lambda |

### CloudTrail

AWS CloudTrail ghi lại các hành động trong tài khoản AWS, ví dụ:

- Ai đã tạo hoặc xóa Lambda.
- Ai đã thay đổi IAM Policy.
- Ai đã tạo S3 Bucket.
- Ai đã thay đổi cấu hình API Gateway.
- Ai đã truy cập hoặc chỉnh sửa tài nguyên quan trọng.

CloudTrail giúp tăng tính minh bạch và hỗ trợ điều tra khi có sự cố bảo mật.

---

## 3.5.12. Dashboard quản trị hệ thống

Người quản trị có thể xây dựng dashboard để theo dõi tổng quan hệ thống Parking IoT.

Các thông tin nên hiển thị trên dashboard:

- Tổng số vị trí đỗ xe.
- Số chỗ trống.
- Số chỗ đã có xe.
- Số xe vào trong ngày.
- Số xe ra trong ngày.
- Danh sách lỗi gần nhất.
- Trạng thái thiết bị ESP32.
- Số lượng ảnh đã upload lên S3.
- Số lần Lambda bị lỗi.
- Chi phí AWS hiện tại.

Ví dụ chỉ số dashboard:

| Chỉ số | Ý nghĩa |
| :--- | :--- |
| Total Slots | Tổng số vị trí đỗ |
| Available Slots | Số vị trí còn trống |
| Occupied Slots | Số vị trí đã có xe |
| Today Entries | Số xe vào trong ngày |
| Today Exits | Số xe ra trong ngày |
| Active Devices | Số thiết bị đang hoạt động |
| Lambda Errors | Số lỗi Lambda |
| Current AWS Cost | Chi phí AWS hiện tại |

Dashboard giúp người quản trị theo dõi hệ thống nhanh chóng mà không cần kiểm tra từng dịch vụ riêng lẻ.

---

## 3.5.13. Quy trình xử lý sự cố

Khi hệ thống gặp lỗi, người quản trị cần có quy trình kiểm tra theo từng lớp để xác định nguyên nhân.

Ví dụ quy trình kiểm tra khi Web/App không hiển thị dữ liệu:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB → CloudWatch Logs
```

Các bước kiểm tra:

1. Kiểm tra Web/App có gọi đúng API không.
2. Kiểm tra API Gateway có nhận request không.
3. Kiểm tra Lambda Backend có được kích hoạt không.
4. Kiểm tra Lambda có lỗi trong CloudWatch không.
5. Kiểm tra DynamoDB có dữ liệu không.
6. Kiểm tra quyền IAM của Lambda.
7. Kiểm tra phản hồi trả về Web/App.

Ví dụ quy trình kiểm tra khi ESP32 cảm biến không cập nhật trạng thái:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Các bước kiểm tra:

1. Kiểm tra ESP32 có kết nối WiFi không.
2. Kiểm tra thiết bị có kết nối AWS IoT Core không.
3. Kiểm tra MQTT topic có đúng không.
4. Kiểm tra IoT Rule có chạy không.
5. Kiểm tra Lambda Sensor Processing có log lỗi không.
6. Kiểm tra DynamoDB có cập nhật dữ liệu không.

---

## 3.5.14. Kết luận

Phần giám sát và quản trị giúp hệ thống Parking IoT vận hành ổn định, dễ phát hiện lỗi và kiểm soát chi phí sử dụng AWS. Amazon CloudWatch được sử dụng để ghi log và theo dõi các thành phần quan trọng như Lambda, API Gateway, IoT Core, DynamoDB và Rekognition.

Bên cạnh đó, AWS Budgets hỗ trợ kiểm soát chi phí, IAM giúp quản lý quyền truy cập, còn CloudTrail ghi nhận các hoạt động trong tài khoản AWS. Việc xây dựng dashboard và quy trình xử lý sự cố giúp người quản trị dễ dàng theo dõi, kiểm tra và duy trì hệ thống trong quá trình vận hành thực tế.