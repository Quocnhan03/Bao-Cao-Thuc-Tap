---
title : "Đường ống dữ liệu IoT"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 3.3. </b> "
---

# 3.3. Đường ống dữ liệu IoT

Phần này trình bày cách dữ liệu được thu thập, truyền tải, xử lý và lưu trữ trong hệ thống **Parking IoT thông minh**. Đường ống dữ liệu IoT đóng vai trò kết nối giữa các thiết bị ESP32 tại bãi xe và các dịch vụ AWS dùng để xử lý, lưu trữ, nhận diện biển số và hiển thị dữ liệu cho người dùng.

Trong hệ thống Parking IoT, dữ liệu chính được chia thành hai nhóm:

- **Dữ liệu hình ảnh:** được thu thập từ ESP32 Camera khi xe ra/vào bãi.
- **Dữ liệu cảm biến:** được thu thập từ ESP32 cảm biến để xác định trạng thái từng vị trí đỗ xe.

Các dữ liệu này sau khi được gửi lên AWS sẽ được xử lý bằng **AWS Lambda**, lưu trữ trong **Amazon S3** và **Amazon DynamoDB**, đồng thời có thể được hiển thị trên Web/App hoặc sử dụng cho các chức năng AI.

---

## 3.3.1. Tổng quan đường ống dữ liệu

Đường ống dữ liệu của hệ thống Parking IoT gồm nhiều bước xử lý liên tiếp, từ thiết bị biên đến AWS Cloud.

Luồng tổng quan:

```text
ESP32 Camera / ESP32 cảm biến → AWS Services → Lambda Processing → DynamoDB / S3 → Web/App
```

Cụ thể, hệ thống có ba luồng dữ liệu chính:

| Luồng dữ liệu | Mô tả |
| :--- | :--- |
| Luồng hình ảnh | ESP32 Camera chụp ảnh xe và upload lên Amazon S3 |
| Luồng cảm biến | ESP32 cảm biến gửi trạng thái chỗ đỗ lên AWS IoT Core |
| Luồng truy vấn Web/App | Người dùng truy cập dữ liệu thông qua API Gateway và Lambda |

Mỗi luồng dữ liệu đều được xử lý riêng nhưng kết quả cuối cùng sẽ được lưu trữ tập trung trong DynamoDB để phục vụ quản lý và hiển thị.

---

## 3.3.2. Luồng dữ liệu hình ảnh từ ESP32 Camera

Luồng dữ liệu hình ảnh được sử dụng để ghi nhận xe ra/vào bãi và phục vụ quá trình nhận diện biển số xe.

Thay vì gửi ảnh trực tiếp qua Lambda, ESP32 Camera sẽ xin **Presigned URL** từ API Gateway. Sau đó thiết bị upload ảnh trực tiếp lên Amazon S3. Cách làm này giúp giảm tải cho Lambda và phù hợp hơn với dữ liệu hình ảnh có dung lượng lớn.

Luồng xử lý:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

Sau khi ảnh được upload lên S3, hệ thống tiếp tục xử lý:

```text
Amazon S3 → S3 Event ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Các bước xử lý chi tiết:

1. ESP32 Camera phát hiện xe tại cổng vào hoặc cổng ra.
2. Thiết bị chụp ảnh phương tiện.
3. ESP32 Camera gửi request đến API Gateway để xin Presigned URL.
4. API Gateway gọi Lambda Presigned URL.
5. Lambda tạo Presigned URL và trả về cho ESP32 Camera.
6. ESP32 Camera upload ảnh JPEG trực tiếp lên Amazon S3.
7. Amazon S3 phát sinh sự kiện ObjectCreated khi ảnh được upload thành công.
8. S3 Event kích hoạt Lambda Image Processing.
9. Lambda gọi Amazon Rekognition để phân tích hình ảnh.
10. Kết quả nhận diện được lưu vào DynamoDB.

---

## 3.3.3. Dữ liệu hình ảnh được lưu trữ trong Amazon S3

Amazon S3 được sử dụng để lưu trữ ảnh phương tiện. Mỗi ảnh có thể được đặt tên theo mã thiết bị, thời gian hoặc mã xe để dễ quản lý.

Ví dụ cấu trúc lưu trữ ảnh trong S3:

```text
parking-image-bucket/
├── entrance/
│   ├── esp32_cam_01_20260427_103000.jpg
│   └── esp32_cam_01_20260427_104500.jpg
├── exit/
│   ├── esp32_cam_02_20260427_110000.jpg
│   └── esp32_cam_02_20260427_111500.jpg
```

Cách chia thư mục như trên giúp hệ thống dễ phân biệt ảnh xe vào và xe ra.

Ví dụ dữ liệu ảnh:

```json
{
  "image_id": "esp32_cam_01_20260427_103000.jpg",
  "device_id": "esp32_cam_01",
  "gate": "entrance",
  "direction": "in",
  "timestamp": "2026-04-27T10:30:00",
  "s3_url": "s3://parking-image-bucket/entrance/esp32_cam_01_20260427_103000.jpg"
}
```

---

## 3.3.4. Luồng xử lý ảnh bằng Lambda và Rekognition

Sau khi ảnh được upload lên Amazon S3, sự kiện ObjectCreated sẽ kích hoạt Lambda xử lý ảnh. Lambda lấy thông tin ảnh từ S3 Event, sau đó gọi Amazon Rekognition để phân tích hình ảnh.

Luồng xử lý:

```text
S3 ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Vai trò của từng thành phần:

| Thành phần | Vai trò |
| :--- | :--- |
| Amazon S3 | Lưu ảnh xe |
| S3 ObjectCreated | Kích hoạt Lambda khi có ảnh mới |
| Lambda Image Processing | Xử lý ảnh và gọi Rekognition |
| Amazon Rekognition | Phân tích hình ảnh, hỗ trợ nhận diện biển số |
| DynamoDB | Lưu kết quả nhận diện |

Kết quả sau khi xử lý ảnh có thể bao gồm:

- Mã ảnh.
- Biển số xe.
- Độ tin cậy nhận diện.
- Hướng di chuyển của xe.
- Thời gian ghi nhận.
- Đường dẫn ảnh trong S3.

Ví dụ dữ liệu sau xử lý:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "confidence": 92.5,
  "direction": "in",
  "image_url": "s3://parking-image-bucket/entrance/esp32_cam_01_20260427_103000.jpg",
  "timestamp": "2026-04-27T10:30:00"
}
```

---

## 3.3.5. Luồng dữ liệu cảm biến qua AWS IoT Core

Luồng dữ liệu cảm biến được sử dụng để cập nhật trạng thái từng vị trí đỗ xe. ESP32 cảm biến gửi dữ liệu lên AWS IoT Core thông qua giao thức MQTT.

Luồng xử lý:

```text
ESP32 cảm biến → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Các bước xử lý chi tiết:

1. ESP32 cảm biến đọc dữ liệu từ cảm biến tại vị trí đỗ.
2. Thiết bị xác định trạng thái vị trí đỗ là `available` hoặc `occupied`.
3. ESP32 gửi dữ liệu lên AWS IoT Core bằng MQTT.
4. AWS IoT Core nhận dữ liệu từ thiết bị.
5. IoT Rule kiểm tra topic MQTT và chuyển dữ liệu đến Lambda.
6. Lambda Sensor Processing kiểm tra và chuẩn hóa dữ liệu.
7. Dữ liệu được lưu vào DynamoDB.
8. Web/App truy vấn DynamoDB để hiển thị trạng thái mới nhất.

Ví dụ MQTT topic:

```text
parking/slot/A01/status
```

Ví dụ payload:

```json
{
  "device_id": "esp32_sensor_01",
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

---

## 3.3.6. Xử lý và chuẩn hóa dữ liệu cảm biến

Trước khi lưu vào DynamoDB, dữ liệu cảm biến cần được kiểm tra để đảm bảo đúng định dạng và tránh sai lệch.

Lambda Sensor Processing thực hiện các công việc sau:

- Kiểm tra `device_id` có tồn tại hay không.
- Kiểm tra `slot_id` có đúng định dạng hay không.
- Kiểm tra `status` có thuộc hai trạng thái `available` hoặc `occupied` hay không.
- Gắn thời gian xử lý nếu thiết bị không gửi timestamp.
- Loại bỏ dữ liệu lỗi hoặc dữ liệu không hợp lệ.
- Ghi trạng thái mới nhất vào bảng DynamoDB.

Ví dụ dữ liệu hợp lệ:

```json
{
  "slot_id": "A01",
  "status": "available",
  "updated_at": "2026-04-27T10:30:00"
}
```

Ví dụ dữ liệu không hợp lệ:

```json
{
  "slot_id": "",
  "status": "unknown"
}
```

Dữ liệu không hợp lệ sẽ không được ghi vào DynamoDB hoặc sẽ được ghi log vào CloudWatch để kiểm tra sau.

---

## 3.3.7. Lưu dữ liệu vào Amazon DynamoDB

Amazon DynamoDB được sử dụng để lưu trữ dữ liệu đã được xử lý. Hệ thống có thể sử dụng nhiều bảng để tách biệt dữ liệu xe, dữ liệu cảm biến và trạng thái vị trí đỗ.

Các bảng chính:

| Bảng | Chức năng |
| :--- | :--- |
| ParkingSlots | Lưu trạng thái mới nhất của từng vị trí đỗ |
| VehicleLogs | Lưu lịch sử xe ra/vào |
| SensorData | Lưu dữ liệu cảm biến theo thời gian |
| DeviceStatus | Lưu trạng thái hoạt động của thiết bị nếu cần |

Ví dụ bảng `ParkingSlots`:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "updated_at": "2026-04-27T10:30:00",
  "device_id": "esp32_sensor_01"
}
```

Ví dụ bảng `VehicleLogs`:

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

DynamoDB giúp hệ thống truy xuất dữ liệu nhanh, phù hợp với các chức năng như xem trạng thái bãi xe, tìm kiếm lịch sử xe và hiển thị dashboard.

---

## 3.3.8. Luồng truy vấn dữ liệu từ Web/App

Người dùng truy cập Web/App để xem trạng thái bãi xe, lịch sử xe ra/vào và thông tin biển số. Web/App không truy cập trực tiếp DynamoDB mà gọi API Gateway. API Gateway chuyển request đến Lambda Backend để xử lý.

Luồng xử lý:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB → Lambda Backend → Web/App
```

Các chức năng truy vấn chính:

- Lấy danh sách vị trí đỗ xe.
- Xem trạng thái từng vị trí đỗ.
- Xem số lượng chỗ trống và chỗ đã có xe.
- Xem lịch sử xe ra/vào.
- Tìm kiếm xe theo biển số.
- Xem hình ảnh xe đã lưu trong S3.
- Xem thống kê dữ liệu bãi xe.

Ví dụ API lấy trạng thái bãi xe:

```text
GET /parking/slots
```

Ví dụ phản hồi:

```json
{
  "total_slots": 50,
  "available": 18,
  "occupied": 32,
  "slots": [
    {
      "slot_id": "A01",
      "status": "occupied"
    },
    {
      "slot_id": "A02",
      "status": "available"
    }
  ]
}
```

---

## 3.3.9. Luồng dữ liệu AI Service

Ngoài các chức năng quản lý thông thường, hệ thống có thể tích hợp thêm Amazon Bedrock để hỗ trợ truy vấn dữ liệu bằng ngôn ngữ tự nhiên. Người dùng có thể đặt câu hỏi trên Web/App, sau đó hệ thống xử lý bằng Lambda AI Service.

Luồng xử lý:

```text
Web/App → API Gateway → Lambda AI Service → DynamoDB → Amazon Bedrock → Web/App
```

Các bước xử lý:

1. Người dùng nhập câu hỏi trên Web/App.
2. Web/App gửi câu hỏi đến API Gateway.
3. API Gateway gọi Lambda AI Service.
4. Lambda AI Service truy vấn dữ liệu cần thiết từ DynamoDB.
5. Lambda gửi ngữ cảnh dữ liệu đến Amazon Bedrock.
6. Amazon Bedrock tạo phản hồi theo ngôn ngữ tự nhiên.
7. Kết quả được trả về Web/App.

Ví dụ câu hỏi:

```text
Hiện tại bãi xe còn bao nhiêu chỗ trống?
```

Ví dụ phản hồi:

```text
Hiện tại bãi xe còn 18 chỗ trống trên tổng số 50 vị trí đỗ.
```

---

## 3.3.10. Ghi log và xử lý lỗi trong đường ống dữ liệu

Trong quá trình truyền và xử lý dữ liệu, hệ thống có thể gặp các lỗi như thiết bị mất kết nối, upload ảnh thất bại, dữ liệu cảm biến sai định dạng hoặc Lambda xử lý lỗi. Vì vậy, CloudWatch được sử dụng để ghi log và hỗ trợ kiểm tra lỗi.

Các lỗi cần theo dõi:

| Lỗi | Cách xử lý |
| :--- | :--- |
| ESP32 mất WiFi | Thiết bị tự kết nối lại và gửi lại dữ liệu |
| Upload ảnh thất bại | ESP32 xin lại Presigned URL và upload lại |
| Payload MQTT sai định dạng | Lambda ghi log lỗi vào CloudWatch |
| Rekognition không nhận diện được biển số | Lưu kết quả với trạng thái cần kiểm tra thủ công |
| DynamoDB ghi dữ liệu thất bại | Lambda retry hoặc ghi log lỗi |
| API Gateway lỗi 4xx/5xx | Kiểm tra request và log Lambda |

Luồng ghi log:

```text
API Gateway / Lambda / IoT Core / Rekognition / DynamoDB → CloudWatch
```

CloudWatch giúp nhóm phát hiện lỗi sớm và đảm bảo đường ống dữ liệu hoạt động ổn định.

---

## 3.3.11. Kết luận

Đường ống dữ liệu IoT là thành phần quan trọng giúp hệ thống Parking IoT hoạt động tự động và theo thời gian thực. Dữ liệu từ ESP32 Camera và ESP32 cảm biến được gửi lên AWS thông qua hai luồng chính: ảnh xe được upload lên Amazon S3 bằng Presigned URL, còn dữ liệu cảm biến được gửi lên AWS IoT Core bằng MQTT.

Sau khi dữ liệu được tiếp nhận, AWS Lambda thực hiện xử lý, Amazon Rekognition hỗ trợ nhận diện biển số, DynamoDB lưu trữ kết quả và Web/App hiển thị dữ liệu cho người dùng. Bên cạnh đó, CloudWatch giúp ghi log và theo dõi lỗi trong toàn bộ quá trình xử lý.

Với thiết kế này, hệ thống có thể giám sát bãi xe theo thời gian thực, lưu trữ dữ liệu tập trung, hỗ trợ nhận diện biển số và tạo nền tảng cho các chức năng nâng cao như thống kê, cảnh báo và AI Service.