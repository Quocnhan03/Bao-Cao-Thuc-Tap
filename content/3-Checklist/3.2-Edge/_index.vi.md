---
title : "Thiết bị biên ESP32"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 3.2. </b> "
---

# 3.2. Thiết bị biên ESP32

Phần này trình bày vai trò của các thiết bị biên trong hệ thống **Parking IoT thông minh**. Thiết bị biên là các thiết bị được đặt trực tiếp tại bãi đỗ xe để thu thập dữ liệu thực tế, bao gồm hình ảnh phương tiện và trạng thái vị trí đỗ xe.

Trong hệ thống này, nhóm sử dụng hai loại thiết bị chính:

- **ESP32 Camera:** dùng để chụp ảnh xe ra/vào bãi.
- **ESP32 cảm biến:** dùng để phát hiện trạng thái từng vị trí đỗ xe.

Dữ liệu từ các thiết bị ESP32 sẽ được gửi lên AWS để xử lý, lưu trữ và hiển thị trên giao diện Web/App.

---

## 3.2.1. Vai trò của thiết bị biên trong hệ thống

Thiết bị biên đóng vai trò là lớp thu thập dữ liệu đầu tiên của hệ thống Parking IoT. Các thiết bị này được lắp đặt tại bãi xe để ghi nhận thông tin theo thời gian thực.

Các nhiệm vụ chính của thiết bị biên gồm:

- Chụp ảnh phương tiện khi xe đi vào hoặc đi ra.
- Ghi nhận trạng thái vị trí đỗ xe.
- Gửi dữ liệu cảm biến lên AWS IoT Core.
- Gửi ảnh xe lên Amazon S3 thông qua Presigned URL.
- Hỗ trợ hệ thống tự động hóa quá trình giám sát bãi xe.

Nhờ có thiết bị biên, hệ thống có thể giảm thao tác thủ công và cập nhật dữ liệu nhanh chóng hơn.

---

## 3.2.2. ESP32 Camera

ESP32 Camera được sử dụng để chụp ảnh phương tiện tại cổng ra/vào của bãi đỗ xe. Khi có xe đi qua, camera sẽ chụp ảnh và gửi ảnh lên Amazon S3 để phục vụ quá trình xử lý ảnh và nhận diện biển số.

### Chức năng chính của ESP32 Camera

- Chụp ảnh xe khi phát hiện phương tiện.
- Gửi yêu cầu đến API Gateway để lấy Presigned URL.
- Upload ảnh trực tiếp lên Amazon S3.
- Gửi thông tin ảnh kèm thời gian ghi nhận.
- Hỗ trợ quá trình nhận diện biển số bằng Amazon Rekognition.

### Luồng hoạt động của ESP32 Camera

```text
ESP32 Camera → API Gateway → Lambda tạo Presigned URL → Amazon S3
```

Sau khi ảnh được upload lên S3, hệ thống tiếp tục xử lý theo luồng:

```text
Amazon S3 → S3 Event ObjectCreated → Lambda xử lý ảnh → Amazon Rekognition → DynamoDB
```

### Các bước xử lý chi tiết

1. ESP32 Camera được lắp tại cổng ra hoặc cổng vào của bãi xe.
2. Khi có xe đi qua, thiết bị tiến hành chụp ảnh.
3. ESP32 Camera gửi request đến API Gateway để xin Presigned URL.
4. API Gateway gọi Lambda Backend để tạo Presigned URL.
5. Lambda trả Presigned URL về cho ESP32 Camera.
6. ESP32 Camera upload ảnh JPEG trực tiếp lên Amazon S3.
7. Khi ảnh được upload thành công, S3 kích hoạt Lambda xử lý ảnh.
8. Lambda gọi Amazon Rekognition để phân tích hình ảnh.
9. Kết quả nhận diện được lưu vào DynamoDB.

### Ví dụ dữ liệu ảnh

```json
{
  "image_id": "car_001.jpg",
  "device_id": "esp32_cam_01",
  "gate": "entrance",
  "direction": "in",
  "timestamp": "2026-04-27T10:30:00",
  "s3_url": "s3://parking-image-bucket/car_001.jpg"
}
```

Trong đó:

| Thuộc tính | Ý nghĩa |
| :--- | :--- |
| image_id | Tên hoặc mã ảnh |
| device_id | Mã thiết bị ESP32 Camera |
| gate | Vị trí camera, ví dụ cổng vào hoặc cổng ra |
| direction | Hướng di chuyển của xe: `in` hoặc `out` |
| timestamp | Thời gian chụp ảnh |
| s3_url | Đường dẫn ảnh trong Amazon S3 |

---

## 3.2.3. ESP32 cảm biến

ESP32 cảm biến được sử dụng để phát hiện trạng thái của từng vị trí đỗ xe. Tùy vào thiết kế thực tế, hệ thống có thể sử dụng cảm biến siêu âm, cảm biến hồng ngoại hoặc cảm biến từ để xác định vị trí đỗ có xe hay không.

### Chức năng chính của ESP32 cảm biến

- Đọc dữ liệu từ cảm biến tại từng vị trí đỗ.
- Xác định trạng thái vị trí đỗ là còn trống hoặc đã có xe.
- Gửi dữ liệu lên AWS IoT Core bằng giao thức MQTT.
- Cập nhật trạng thái vị trí đỗ vào DynamoDB thông qua Lambda.
- Hỗ trợ Web/App hiển thị trạng thái bãi xe theo thời gian thực.

### Trạng thái vị trí đỗ

Hệ thống có thể sử dụng hai trạng thái chính:

| Trạng thái | Ý nghĩa |
| :--- | :--- |
| available | Vị trí đỗ còn trống |
| occupied | Vị trí đỗ đã có xe |

### Luồng hoạt động của ESP32 cảm biến

```text
ESP32 cảm biến → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

### Các bước xử lý chi tiết

1. ESP32 đọc dữ liệu từ cảm biến tại vị trí đỗ.
2. Thiết bị xác định trạng thái vị trí đỗ là `available` hoặc `occupied`.
3. ESP32 gửi dữ liệu lên AWS IoT Core bằng MQTT.
4. AWS IoT Core tiếp nhận dữ liệu từ thiết bị.
5. IoT Rule kiểm tra topic MQTT và chuyển dữ liệu đến Lambda.
6. Lambda Sensor Processing xử lý và chuẩn hóa dữ liệu.
7. Dữ liệu được lưu vào DynamoDB.
8. Web/App truy vấn DynamoDB để hiển thị trạng thái mới nhất.

### Ví dụ MQTT Topic

```text
parking/slot/A01/status
```

### Ví dụ payload gửi từ ESP32 cảm biến

```json
{
  "device_id": "esp32_sensor_01",
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

Trong đó:

| Thuộc tính | Ý nghĩa |
| :--- | :--- |
| device_id | Mã thiết bị ESP32 cảm biến |
| slot_id | Mã vị trí đỗ xe |
| status | Trạng thái vị trí đỗ |
| timestamp | Thời gian ghi nhận dữ liệu |

---

## 3.2.4. Kết nối ESP32 với Internet

Các thiết bị ESP32 cần kết nối WiFi để gửi dữ liệu lên AWS. Mỗi thiết bị sẽ được cấu hình thông tin mạng và thông tin kết nối đến hệ thống AWS.

Các thông tin cần cấu hình gồm:

- Tên WiFi.
- Mật khẩu WiFi.
- Địa chỉ API Gateway dùng cho ESP32 Camera.
- Endpoint AWS IoT Core dùng cho ESP32 cảm biến.
- Chứng chỉ và khóa bảo mật nếu kết nối MQTT với AWS IoT Core.
- Mã thiết bị để phân biệt từng ESP32 trong hệ thống.

Ví dụ thông tin cấu hình thiết bị:

```text
WiFi SSID: Parking_WiFi
Device ID: esp32_sensor_01
MQTT Topic: parking/slot/A01/status
AWS IoT Endpoint: xxxxxxxxxxxxxx-ats.iot.ap-southeast-1.amazonaws.com
```

Việc định danh từng thiết bị giúp hệ thống dễ quản lý, dễ kiểm tra lỗi và dễ mở rộng khi thêm nhiều cảm biến hoặc camera mới.

---

## 3.2.5. Kết nối ESP32 Camera với Amazon S3

ESP32 Camera không upload ảnh trực tiếp qua Lambda vì ảnh có thể có dung lượng lớn. Thay vào đó, thiết bị sử dụng Presigned URL để tải ảnh trực tiếp lên Amazon S3.

Quy trình upload ảnh gồm:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → ESP32 Camera → Amazon S3
```

Các bước thực hiện:

1. ESP32 Camera chụp ảnh xe.
2. ESP32 Camera gửi request đến API Gateway.
3. Lambda tạo Presigned URL cho ảnh cần upload.
4. ESP32 Camera nhận Presigned URL.
5. ESP32 Camera upload ảnh JPEG lên Amazon S3.
6. S3 kích hoạt Lambda xử lý ảnh sau khi upload thành công.

Cách làm này giúp:

- Giảm tải cho Lambda.
- Upload ảnh nhanh hơn.
- Tận dụng khả năng lưu trữ của Amazon S3.
- Dễ kích hoạt xử lý ảnh bằng S3 Event.

---

## 3.2.6. Kết nối ESP32 cảm biến với AWS IoT Core

ESP32 cảm biến gửi dữ liệu lên AWS IoT Core thông qua giao thức MQTT. MQTT phù hợp với hệ thống IoT vì nhẹ, dễ sử dụng và phù hợp với thiết bị có tài nguyên hạn chế.

Quy trình gửi dữ liệu gồm:

```text
ESP32 cảm biến → MQTT → AWS IoT Core → IoT Rule → Lambda → DynamoDB
```

Các bước thực hiện:

1. Tạo IoT Thing đại diện cho thiết bị ESP32 trên AWS IoT Core.
2. Tạo chứng chỉ bảo mật cho thiết bị.
3. Gắn IoT Policy cho chứng chỉ.
4. Cấu hình MQTT endpoint trên ESP32.
5. ESP32 gửi dữ liệu lên topic đã định nghĩa.
6. IoT Rule chuyển dữ liệu đến Lambda xử lý.
7. Lambda ghi dữ liệu vào DynamoDB.

Ví dụ dữ liệu gửi định kỳ:

```json
{
  "device_id": "esp32_sensor_02",
  "slot_id": "B03",
  "status": "available",
  "timestamp": "2026-04-27T10:35:00"
}
```

---

## 3.2.7. Bảo mật thiết bị biên

Bảo mật thiết bị biên là phần quan trọng vì các thiết bị ESP32 kết nối trực tiếp với Internet và gửi dữ liệu lên AWS.

Các biện pháp bảo mật gồm:

- Không lưu thông tin nhạy cảm công khai trong mã nguồn.
- Sử dụng chứng chỉ khi kết nối ESP32 với AWS IoT Core.
- Mỗi thiết bị nên có một mã định danh riêng.
- IoT Policy chỉ cho phép thiết bị publish vào đúng topic của nó.
- API Gateway nên kiểm tra request từ ESP32 Camera.
- Presigned URL chỉ có hiệu lực trong thời gian ngắn.
- Không cấp quyền AWS trực tiếp cho thiết bị ESP32.

Ví dụ nguyên tắc bảo mật:

```text
ESP32 chỉ được gửi dữ liệu vào topic của chính nó.
ESP32 Camera chỉ được upload ảnh thông qua Presigned URL có thời hạn.
```

Việc giới hạn quyền giúp giảm rủi ro nếu một thiết bị bị lỗi hoặc bị truy cập trái phép.

---

## 3.2.8. Xử lý lỗi tại thiết bị biên

Trong quá trình vận hành, thiết bị ESP32 có thể gặp lỗi như mất WiFi, gửi dữ liệu thất bại hoặc upload ảnh không thành công. Vì vậy, cần có cơ chế xử lý lỗi cơ bản tại thiết bị.

Các lỗi thường gặp:

| Lỗi | Cách xử lý |
| :--- | :--- |
| Mất kết nối WiFi | Tự động kết nối lại sau một khoảng thời gian |
| Gửi MQTT thất bại | Gửi lại dữ liệu khi kết nối ổn định |
| Upload ảnh thất bại | Xin lại Presigned URL và upload lại |
| Cảm biến đọc sai | Lọc dữ liệu hoặc kiểm tra nhiều lần trước khi gửi |
| Camera chụp ảnh mờ | Điều chỉnh góc đặt camera và ánh sáng |

Thiết bị có thể lưu tạm dữ liệu trong bộ nhớ nội bộ nếu mất kết nối mạng, sau đó gửi lại khi Internet hoạt động bình thường.

---

## 3.2.9. Kiểm thử thiết bị biên

Trước khi tích hợp hoàn toàn với AWS, cần kiểm thử từng thiết bị ESP32 để đảm bảo hệ thống hoạt động đúng.

Các bước kiểm thử ESP32 Camera:

- Kiểm tra camera có chụp ảnh được không.
- Kiểm tra ảnh có rõ biển số không.
- Kiểm tra ESP32 có gọi được API Gateway không.
- Kiểm tra Presigned URL có được tạo thành công không.
- Kiểm tra ảnh có upload lên S3 thành công không.
- Kiểm tra S3 có kích hoạt Lambda xử lý ảnh không.

Các bước kiểm thử ESP32 cảm biến:

- Kiểm tra cảm biến có đọc đúng trạng thái không.
- Kiểm tra ESP32 có kết nối WiFi không.
- Kiểm tra ESP32 có kết nối AWS IoT Core không.
- Kiểm tra dữ liệu có được gửi đúng topic MQTT không.
- Kiểm tra IoT Rule có kích hoạt Lambda không.
- Kiểm tra DynamoDB có lưu trạng thái mới không.

---

## 3.2.10. Kết luận

Phần thiết bị biên ESP32 là lớp thu thập dữ liệu quan trọng của hệ thống Parking IoT. ESP32 Camera đảm nhiệm việc chụp ảnh phương tiện ra/vào, còn ESP32 cảm biến đảm nhiệm việc ghi nhận trạng thái từng vị trí đỗ xe.

Dữ liệu từ thiết bị được gửi lên AWS thông qua hai luồng chính: ảnh xe được upload lên Amazon S3 bằng Presigned URL, còn dữ liệu cảm biến được gửi lên AWS IoT Core bằng MQTT. Sau đó, AWS Lambda xử lý dữ liệu và lưu kết quả vào DynamoDB.

Việc triển khai thiết bị biên giúp hệ thống Parking IoT có khả năng giám sát bãi xe theo thời gian thực, giảm thao tác thủ công và tạo nền tảng dữ liệu phục vụ các chức năng nâng cao như nhận diện biển số, thống kê bãi xe và hỗ trợ AI.