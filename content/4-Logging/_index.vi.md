---
title : "Quản lý Session Logs"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 4. </b> "
---

# 4. Quản lý Session Logs

Phần này trình bày cách quản lý **Session Logs** trong hệ thống **Parking IoT thông minh**. Session Logs được sử dụng để ghi nhận lại quá trình hoạt động của thiết bị ESP32, Web/App, API Gateway, Lambda và các dịch vụ AWS liên quan trong từng phiên xử lý dữ liệu.

Khác với log hệ thống thông thường chỉ ghi lỗi hoặc trạng thái thực thi, Session Logs tập trung vào việc theo dõi một phiên hoạt động cụ thể, ví dụ:

- Một lần ESP32 Camera chụp và upload ảnh xe.
- Một lần ESP32 cảm biến gửi trạng thái vị trí đỗ xe.
- Một lần người dùng đăng nhập vào Web/App.
- Một lần Web/App gọi API để lấy dữ liệu bãi xe.
- Một lần Lambda xử lý dữ liệu và ghi kết quả vào DynamoDB.

Việc quản lý Session Logs giúp người quản trị dễ dàng kiểm tra luồng xử lý, phát hiện lỗi, truy vết dữ liệu và đánh giá mức độ ổn định của hệ thống.

---

## 4.1. Tổng quan Session Logs

Session Logs là tập hợp các bản ghi mô tả quá trình hoạt động của một phiên trong hệ thống. Mỗi phiên có thể bắt đầu khi thiết bị hoặc người dùng gửi request đến hệ thống và kết thúc khi dữ liệu được xử lý xong.

Trong hệ thống Parking IoT, Session Logs có thể được chia thành ba nhóm chính:

| Nhóm Session Logs | Mô tả |
| :--- | :--- |
| Device Session Logs | Ghi nhận hoạt động của ESP32 Camera và ESP32 cảm biến |
| User Session Logs | Ghi nhận hoạt động đăng nhập và thao tác của người dùng trên Web/App |
| API Session Logs | Ghi nhận request, response và lỗi khi gọi API Gateway và Lambda |

Ví dụ một phiên hoạt động của ESP32 Camera:

```text
ESP32 Camera chụp ảnh → Xin Presigned URL → Upload ảnh lên S3 → Lambda xử lý ảnh → Lưu kết quả vào DynamoDB
```

Ví dụ một phiên hoạt động của người dùng:

```text
User đăng nhập → Cognito xác thực → Web/App gọi API → Lambda truy vấn DynamoDB → Trả dữ liệu về giao diện
```

Mỗi session nên có một mã định danh riêng, gọi là `session_id`, để dễ dàng truy vết toàn bộ quá trình xử lý.

Ví dụ cấu trúc Session Log:

```json
{
  "session_id": "SESSION001",
  "source": "esp32_camera",
  "action": "upload_image",
  "status": "success",
  "start_time": "2026-04-27T10:30:00",
  "end_time": "2026-04-27T10:30:05",
  "message": "Image uploaded and processed successfully"
}
```

---

## 4.2. Thu thập Logs từ thiết bị ESP32

Thiết bị ESP32 là nguồn dữ liệu đầu vào quan trọng của hệ thống. Vì vậy, cần ghi nhận log từ ESP32 Camera và ESP32 cảm biến để kiểm tra thiết bị có hoạt động đúng hay không.

### 4.2.1. Logs từ ESP32 Camera

ESP32 Camera cần ghi lại các thông tin trong quá trình chụp ảnh và upload ảnh lên Amazon S3.

Luồng hoạt động:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

Các thông tin cần ghi log:

- Mã thiết bị ESP32 Camera.
- Thời gian chụp ảnh.
- Vị trí camera: cổng vào hoặc cổng ra.
- Trạng thái gọi API Gateway.
- Trạng thái nhận Presigned URL.
- Trạng thái upload ảnh lên S3.
- Tên file ảnh.
- Lỗi phát sinh nếu upload thất bại.

Ví dụ log từ ESP32 Camera:

```json
{
  "session_id": "CAM_SESSION_001",
  "device_id": "esp32_cam_01",
  "device_type": "camera",
  "gate": "entrance",
  "action": "upload_image",
  "image_name": "esp32_cam_01_20260427_103000.jpg",
  "status": "success",
  "timestamp": "2026-04-27T10:30:00"
}
```

Nếu xảy ra lỗi:

```json
{
  "session_id": "CAM_SESSION_002",
  "device_id": "esp32_cam_01",
  "device_type": "camera",
  "action": "upload_image",
  "status": "failed",
  "error_message": "Failed to get Presigned URL",
  "timestamp": "2026-04-27T10:35:00"
}
```

### 4.2.2. Logs từ ESP32 cảm biến

ESP32 cảm biến gửi dữ liệu trạng thái vị trí đỗ xe lên AWS IoT Core thông qua MQTT. Session Logs giúp kiểm tra thiết bị có gửi đúng topic, đúng dữ liệu và đúng thời gian hay không.

Luồng hoạt động:

```text
ESP32 cảm biến → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Các thông tin cần ghi log:

- Mã thiết bị cảm biến.
- Mã vị trí đỗ xe.
- Trạng thái vị trí đỗ: `available` hoặc `occupied`.
- MQTT topic.
- Thời gian gửi dữ liệu.
- Trạng thái gửi dữ liệu.
- Lỗi kết nối WiFi hoặc MQTT nếu có.

Ví dụ log từ ESP32 cảm biến:

```json
{
  "session_id": "SENSOR_SESSION_001",
  "device_id": "esp32_sensor_01",
  "device_type": "sensor",
  "slot_id": "A01",
  "mqtt_topic": "parking/slot/A01/status",
  "status_value": "occupied",
  "send_status": "success",
  "timestamp": "2026-04-27T10:30:00"
}
```

Nếu thiết bị gửi lỗi:

```json
{
  "session_id": "SENSOR_SESSION_002",
  "device_id": "esp32_sensor_01",
  "device_type": "sensor",
  "slot_id": "A01",
  "send_status": "failed",
  "error_message": "MQTT publish failed",
  "timestamp": "2026-04-27T10:32:00"
}
```

---

## 4.3. Thu thập Logs từ Web/App và API Gateway

Ngoài thiết bị ESP32, hệ thống cũng cần ghi nhận log từ Web/App và API Gateway để kiểm tra quá trình người dùng truy cập hệ thống.

### 4.3.1. Logs từ Web/App

Web/App là nơi người dùng đăng nhập, xem trạng thái bãi xe, tìm kiếm biển số và xem lịch sử xe ra/vào.

Các thông tin cần ghi log:

- Mã người dùng.
- Thời gian đăng nhập.
- Chức năng được truy cập.
- API được gọi.
- Trạng thái request.
- Lỗi hiển thị nếu có.
- Thời gian phản hồi.

Ví dụ User Session Log:

```json
{
  "session_id": "USER_SESSION_001",
  "user_id": "manager01",
  "role": "Manager",
  "action": "view_parking_slots",
  "api_endpoint": "/parking/slots",
  "status": "success",
  "timestamp": "2026-04-27T10:40:00"
}
```

Ví dụ log khi người dùng tìm kiếm biển số:

```json
{
  "session_id": "USER_SESSION_002",
  "user_id": "manager01",
  "action": "search_vehicle",
  "plate_number": "51A-12345",
  "api_endpoint": "/vehicle/search",
  "status": "success",
  "timestamp": "2026-04-27T10:42:00"
}
```

### 4.3.2. Logs từ API Gateway

API Gateway là cổng giao tiếp giữa Web/App, ESP32 Camera và Lambda Backend. Việc ghi log API Gateway giúp kiểm tra request có đến đúng endpoint hay không và backend có phản hồi đúng hay không.

Các thông tin cần ghi log:

- HTTP Method.
- API Endpoint.
- Request ID.
- Status Code.
- Thời gian phản hồi.
- IP hoặc nguồn request nếu cần.
- Lỗi 4xx hoặc 5xx.

Ví dụ API Gateway Log:

```json
{
  "request_id": "REQ001",
  "session_id": "USER_SESSION_001",
  "method": "GET",
  "endpoint": "/parking/slots",
  "status_code": 200,
  "response_time_ms": 120,
  "timestamp": "2026-04-27T10:40:01"
}
```

Ví dụ API lỗi:

```json
{
  "request_id": "REQ002",
  "session_id": "USER_SESSION_003",
  "method": "GET",
  "endpoint": "/vehicle/logs",
  "status_code": 401,
  "error_message": "Unauthorized request",
  "timestamp": "2026-04-27T10:45:00"
}
```

---

## 4.4. Lưu trữ và truy vấn Session Logs

Sau khi thu thập, Session Logs cần được lưu trữ để phục vụ kiểm tra, truy vấn và phân tích. Trong hệ thống Parking IoT, có thể sử dụng kết hợp **Amazon CloudWatch Logs, Amazon DynamoDB và Amazon S3**.

### 4.4.1. Lưu Session Logs trong CloudWatch Logs

CloudWatch Logs được sử dụng để lưu log thực thi của Lambda, API Gateway và các lỗi hệ thống.

Luồng lưu log:

```text
API Gateway / Lambda / IoT Rule → CloudWatch Logs
```

CloudWatch Logs phù hợp để:

- Kiểm tra lỗi Lambda.
- Xem request API Gateway.
- Theo dõi payload từ IoT Core.
- Truy vết lỗi khi hệ thống hoạt động bất thường.

Ví dụ kiểm tra log:

```text
CloudWatch → Log Groups → Chọn Lambda Function → Xem Log Stream
```

### 4.4.2. Lưu Session Logs trong DynamoDB

DynamoDB có thể được sử dụng để lưu các Session Logs quan trọng cần truy vấn nhanh trên Web/App hoặc dashboard quản trị.

Ví dụ bảng `SessionLogs`:

| Thuộc tính | Mô tả |
| :--- | :--- |
| session_id | Mã phiên hoạt động |
| source | Nguồn log: ESP32, Web/App, API Gateway |
| action | Hành động được thực hiện |
| status | Trạng thái xử lý |
| timestamp | Thời gian ghi log |
| error_message | Nội dung lỗi nếu có |

Ví dụ dữ liệu trong bảng `SessionLogs`:

```json
{
  "session_id": "SESSION001",
  "source": "api_gateway",
  "action": "get_parking_slots",
  "status": "success",
  "timestamp": "2026-04-27T10:40:00",
  "response_time_ms": 120
}
```

### 4.4.3. Lưu trữ dài hạn trong Amazon S3

Amazon S3 có thể được sử dụng để lưu trữ log lâu dài, đặc biệt là các log cũ không cần truy vấn thường xuyên.

Ví dụ cấu trúc lưu log trong S3:

```text
parking-session-logs/
├── 2026/
│   ├── 04/
│   │   ├── 27/
│   │   │   ├── device-logs.json
│   │   │   ├── user-logs.json
│   │   │   └── api-logs.json
```

Lưu log trong S3 giúp:

- Giảm chi phí lưu trữ log lâu dài.
- Dễ sao lưu dữ liệu.
- Có thể truy vấn bằng Athena nếu cần.
- Phù hợp cho báo cáo và kiểm tra sau demo.

---

## 4.5. Phân tích Session Logs

Sau khi Session Logs được lưu trữ, hệ thống có thể sử dụng log để phân tích hoạt động và phát hiện lỗi.

### 4.5.1. Phân tích hoạt động thiết bị

Session Logs giúp người quản trị biết thiết bị ESP32 có hoạt động ổn định hay không.

Các chỉ số có thể phân tích:

- Số lần ESP32 Camera upload ảnh thành công.
- Số lần ESP32 Camera upload ảnh thất bại.
- Số lần ESP32 cảm biến gửi dữ liệu.
- Thiết bị nào mất kết nối thường xuyên.
- Vị trí đỗ nào cập nhật trạng thái bất thường.

Ví dụ phân tích:

```text
ESP32 Sensor A01 gửi dữ liệu 120 lần trong ngày.
ESP32 Sensor B03 không gửi dữ liệu trong 2 giờ gần nhất.
ESP32 Camera cổng vào upload ảnh thất bại 3 lần.
```

### 4.5.2. Phân tích hoạt động người dùng

User Session Logs giúp kiểm tra người dùng đã thao tác gì trên hệ thống.

Các thông tin có thể phân tích:

- Người dùng đăng nhập lúc nào.
- Người dùng truy cập chức năng nào nhiều nhất.
- Người dùng có gọi API bị lỗi không.
- Có hành vi truy cập bất thường hay không.

Ví dụ:

```text
Manager01 đăng nhập lúc 08:00 và xem lịch sử xe ra/vào 5 lần.
User02 gọi API /admin/users nhưng bị từ chối vì không đủ quyền.
```

### 4.5.3. Phân tích lỗi API và Lambda

API Session Logs giúp phát hiện các lỗi trong quá trình Web/App hoặc ESP32 gọi API.

Các lỗi cần chú ý:

| Loại lỗi | Ý nghĩa |
| :--- | :--- |
| 400 | Request sai định dạng |
| 401 | Chưa xác thực |
| 403 | Không có quyền |
| 404 | Sai endpoint |
| 500 | Lỗi Lambda Backend |
| 504 | Request timeout |

Ví dụ phân tích lỗi:

```text
API /parking/slots có response time trung bình 120ms.
API /vehicle/logs xuất hiện lỗi 500 trong 3 lần gọi gần nhất.
API /admin/users bị chặn do người dùng không có quyền Admin.
```

### 4.5.4. Phân tích hiệu năng hệ thống

Session Logs có thể hỗ trợ đánh giá hiệu năng của hệ thống thông qua thời gian xử lý từng bước.

Các chỉ số cần quan tâm:

- Thời gian ESP32 upload ảnh lên S3.
- Thời gian Lambda xử lý ảnh.
- Thời gian gọi Rekognition.
- Thời gian API Gateway phản hồi.
- Thời gian truy vấn DynamoDB.
- Tỷ lệ request thành công và thất bại.

Ví dụ:

```text
Thời gian trung bình upload ảnh: 2.5 giây.
Thời gian trung bình xử lý ảnh bằng Lambda: 1.8 giây.
Thời gian trung bình API phản hồi Web/App: 120ms.
```

Nhờ các thông tin này, nhóm có thể tối ưu hệ thống nếu phát hiện bước nào xử lý quá lâu.

---

## 4.6. Kết luận

Session Logs đóng vai trò quan trọng trong quá trình vận hành hệ thống Parking IoT. Việc ghi nhận log theo từng phiên giúp người quản trị theo dõi chi tiết quá trình hoạt động của thiết bị ESP32, Web/App, API Gateway, Lambda và các dịch vụ AWS liên quan.

Thông qua Session Logs, hệ thống có thể truy vết dữ liệu từ lúc thiết bị gửi thông tin đến khi dữ liệu được xử lý và lưu vào DynamoDB. Ngoài ra, Session Logs còn hỗ trợ phát hiện lỗi, phân tích hiệu năng, kiểm tra hoạt động người dùng và đánh giá mức độ ổn định của hệ thống.

Với việc kết hợp CloudWatch Logs, DynamoDB và Amazon S3, hệ thống có thể vừa theo dõi log theo thời gian thực, vừa lưu trữ log lâu dài phục vụ kiểm tra, báo cáo và tối ưu hệ thống sau này.