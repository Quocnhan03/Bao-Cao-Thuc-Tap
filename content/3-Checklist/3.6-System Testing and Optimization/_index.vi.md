---
title : "Kiểm thử và tối ưu hệ thống"
date :  "`r Sys.Date()`" 
weight : 6
chapter : false
pre : " <b> 3.6. </b> "
---

# 3.6. Kiểm thử và tối ưu hệ thống

Phần này trình bày quá trình kiểm thử và tối ưu hệ thống **Parking IoT thông minh** sau khi đã triển khai các thành phần chính như thiết bị ESP32, AWS IoT Core, Amazon S3, AWS Lambda, Amazon Rekognition, DynamoDB, API Gateway, Cognito, CloudFront và CloudWatch.

Mục tiêu của phần kiểm thử là đảm bảo hệ thống hoạt động đúng theo thiết kế, dữ liệu được truyền và xử lý chính xác, giao diện Web/App hiển thị đúng thông tin, đồng thời hệ thống có thể vận hành ổn định, an toàn và tối ưu chi phí.

---

## 3.6.1. Mục tiêu kiểm thử

Quá trình kiểm thử hệ thống nhằm xác minh các chức năng chính của Parking IoT có hoạt động đúng hay không.

Các mục tiêu kiểm thử gồm:

- Kiểm tra ESP32 Camera có chụp và upload ảnh lên Amazon S3 thành công không.
- Kiểm tra ESP32 cảm biến có gửi dữ liệu trạng thái vị trí đỗ lên AWS IoT Core không.
- Kiểm tra AWS IoT Core có kích hoạt Lambda xử lý dữ liệu cảm biến không.
- Kiểm tra S3 Event ObjectCreated có kích hoạt Lambda xử lý ảnh không.
- Kiểm tra Amazon Rekognition có xử lý ảnh và trả kết quả nhận diện không.
- Kiểm tra DynamoDB có lưu dữ liệu chính xác không.
- Kiểm tra API Gateway và Lambda Backend có trả dữ liệu cho Web/App không.
- Kiểm tra Cognito có xác thực người dùng đúng không.
- Kiểm tra CloudWatch có ghi log và hỗ trợ phát hiện lỗi không.
- Kiểm tra chi phí sử dụng AWS có nằm trong giới hạn cho phép không.

---

## 3.6.2. Kiểm thử ESP32 Camera

ESP32 Camera là thiết bị dùng để chụp ảnh xe ra/vào bãi. Vì vậy, cần kiểm tra khả năng chụp ảnh, gửi request lấy Presigned URL và upload ảnh lên Amazon S3.

Luồng kiểm thử:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3
```

Các bước kiểm thử:

1. Cấp nguồn và kết nối WiFi cho ESP32 Camera.
2. Kiểm tra thiết bị có kết nối mạng thành công không.
3. Cho xe hoặc vật thể đi qua khu vực camera.
4. Kiểm tra ESP32 Camera có chụp được ảnh không.
5. Kiểm tra ESP32 Camera có gọi API Gateway để xin Presigned URL không.
6. Kiểm tra Lambda có tạo Presigned URL thành công không.
7. Kiểm tra ảnh có được upload lên Amazon S3 không.
8. Kiểm tra ảnh có nằm đúng thư mục `entrance/` hoặc `exit/` không.

Kết quả mong đợi:

| Nội dung kiểm thử | Kết quả mong đợi |
| :--- | :--- |
| Kết nối WiFi | ESP32 Camera kết nối thành công |
| Chụp ảnh | Ảnh được tạo rõ ràng |
| Gọi API Gateway | Request gửi thành công |
| Tạo Presigned URL | Lambda trả về URL hợp lệ |
| Upload S3 | Ảnh xuất hiện trong S3 Bucket |

---

## 3.6.3. Kiểm thử ESP32 cảm biến

ESP32 cảm biến dùng để xác định trạng thái từng vị trí đỗ xe. Thiết bị sẽ gửi dữ liệu lên AWS IoT Core thông qua MQTT.

Luồng kiểm thử:

```text
ESP32 cảm biến → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Các bước kiểm thử:

1. Cấp nguồn cho ESP32 cảm biến.
2. Kiểm tra thiết bị có kết nối WiFi không.
3. Kiểm tra thiết bị có kết nối đến AWS IoT Core không.
4. Đặt vật thể hoặc xe vào vị trí cảm biến.
5. Kiểm tra cảm biến có xác định trạng thái `occupied` không.
6. Lấy vật thể hoặc xe ra khỏi vị trí cảm biến.
7. Kiểm tra cảm biến có xác định trạng thái `available` không.
8. Kiểm tra dữ liệu có được publish lên đúng MQTT topic không.
9. Kiểm tra IoT Rule có kích hoạt Lambda không.
10. Kiểm tra DynamoDB có cập nhật trạng thái mới nhất không.

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

Kết quả mong đợi:

| Nội dung kiểm thử | Kết quả mong đợi |
| :--- | :--- |
| Kết nối WiFi | ESP32 kết nối thành công |
| Kết nối IoT Core | Thiết bị publish MQTT thành công |
| Dữ liệu cảm biến | Trạng thái đúng `available` hoặc `occupied` |
| IoT Rule | Lambda được kích hoạt |
| DynamoDB | Dữ liệu được cập nhật chính xác |

---

## 3.6.4. Kiểm thử xử lý ảnh và nhận diện biển số

Sau khi ESP32 Camera upload ảnh lên Amazon S3, hệ thống cần kiểm tra quá trình kích hoạt Lambda và xử lý ảnh bằng Amazon Rekognition.

Luồng kiểm thử:

```text
Amazon S3 → S3 ObjectCreated → Lambda Image Processing → Amazon Rekognition → DynamoDB
```

Các bước kiểm thử:

1. Upload ảnh xe lên S3 bằng ESP32 Camera hoặc upload thủ công để kiểm tra.
2. Kiểm tra S3 Event ObjectCreated có được kích hoạt không.
3. Kiểm tra Lambda Image Processing có chạy không.
4. Kiểm tra Lambda có đọc được ảnh từ S3 không.
5. Kiểm tra Lambda có gọi Amazon Rekognition không.
6. Kiểm tra kết quả nhận diện có được trả về không.
7. Kiểm tra dữ liệu có được ghi vào bảng VehicleLogs trong DynamoDB không.

Ví dụ dữ liệu sau xử lý:

```json
{
  "log_id": "LOG001",
  "plate_number": "51A-12345",
  "confidence": 92.5,
  "direction": "in",
  "image_url": "s3://parking-image-bucket/entrance/car_001.jpg",
  "timestamp": "2026-04-27T10:30:00"
}
```

Kết quả mong đợi:

| Nội dung kiểm thử | Kết quả mong đợi |
| :--- | :--- |
| Upload ảnh | Ảnh được lưu trong S3 |
| S3 Event | Lambda được kích hoạt |
| Rekognition | Ảnh được phân tích |
| DynamoDB | Kết quả được lưu vào VehicleLogs |
| CloudWatch | Có log xử lý thành công |

---

## 3.6.5. Kiểm thử API Gateway và Lambda Backend

API Gateway và Lambda Backend là lớp trung gian giữa Web/App và dữ liệu trong DynamoDB. Cần kiểm tra các API có hoạt động đúng không.

Luồng kiểm thử:

```text
Web/App → API Gateway → Lambda Backend → DynamoDB
```

Các API cần kiểm thử:

| API Endpoint | Mục đích kiểm thử |
| :--- | :--- |
| `GET /parking/slots` | Lấy danh sách vị trí đỗ |
| `GET /vehicle/logs` | Lấy lịch sử xe ra/vào |
| `POST /upload-url` | Tạo Presigned URL |
| `GET /vehicle/search` | Tìm kiếm xe theo biển số |
| `POST /ai/query` | Gửi câu hỏi đến AI Service |

Các bước kiểm thử:

1. Gửi request đến từng API Endpoint.
2. Kiểm tra API Gateway có nhận request không.
3. Kiểm tra Lambda Backend có được gọi không.
4. Kiểm tra Lambda có truy vấn DynamoDB đúng không.
5. Kiểm tra response trả về có đúng định dạng JSON không.
6. Kiểm tra lỗi 4xx hoặc 5xx nếu có.

Ví dụ response API:

```json
{
  "total_slots": 50,
  "available": 18,
  "occupied": 32
}
```

Kết quả mong đợi:

| Nội dung kiểm thử | Kết quả mong đợi |
| :--- | :--- |
| API nhận request | Request gửi thành công |
| Lambda Backend | Lambda xử lý đúng |
| DynamoDB Query | Truy vấn dữ liệu chính xác |
| Response | Trả về JSON đúng định dạng |
| Error Handling | Có log lỗi nếu request sai |

---

## 3.6.6. Kiểm thử giao diện Web/App

Giao diện Web/App là nơi người dùng xem dữ liệu bãi xe. Vì vậy, cần kiểm tra giao diện có hiển thị đúng dữ liệu từ backend không.

Các chức năng cần kiểm thử:

- Đăng nhập người dùng.
- Hiển thị tổng số vị trí đỗ xe.
- Hiển thị số chỗ trống và số chỗ đã có xe.
- Hiển thị trạng thái từng vị trí đỗ.
- Hiển thị lịch sử xe ra/vào.
- Hiển thị hình ảnh xe từ S3.
- Tìm kiếm xe theo biển số.
- Hiển thị thông báo lỗi nếu API gặp sự cố.

Luồng kiểm thử giao diện:

```text
User → CloudFront → S3 Static Website → API Gateway → Lambda → DynamoDB
```

Kết quả mong đợi:

| Chức năng | Kết quả mong đợi |
| :--- | :--- |
| Đăng nhập | Người dùng đăng nhập thành công |
| Dashboard | Hiển thị đúng số chỗ trống và chỗ đã có xe |
| Parking Slots | Trạng thái vị trí đỗ được cập nhật |
| Vehicle Logs | Hiển thị lịch sử xe ra/vào |
| Search | Tìm kiếm biển số trả về đúng kết quả |
| Error Message | Giao diện hiển thị lỗi dễ hiểu |

---

## 3.6.7. Kiểm thử bảo mật

Kiểm thử bảo mật giúp đảm bảo hệ thống không cho phép truy cập trái phép và các dịch vụ AWS chỉ được cấp quyền cần thiết.

Các nội dung cần kiểm thử:

- Người dùng chưa đăng nhập không được gọi API bảo vệ.
- Token Cognito hết hạn sẽ bị API Gateway từ chối.
- Người dùng thường không được truy cập chức năng Admin.
- ESP32 Camera không có quyền AWS trực tiếp.
- Presigned URL chỉ có hiệu lực trong thời gian ngắn.
- ESP32 cảm biến chỉ được publish vào topic MQTT được cấp quyền.
- Lambda chỉ có quyền đúng với nhiệm vụ của nó.

Ví dụ kiểm thử API không có token:

```text
Web/App → API Gateway → Không có Cognito Token → Request bị từ chối
```

Kết quả mong đợi:

| Nội dung kiểm thử | Kết quả mong đợi |
| :--- | :--- |
| Gọi API không token | Bị từ chối |
| Token sai hoặc hết hạn | Bị từ chối |
| User truy cập Admin API | Bị từ chối nếu không có quyền |
| Presigned URL hết hạn | Không upload được |
| Sai MQTT topic | Thiết bị không được publish |

---

## 3.6.8. Kiểm thử giám sát và log

CloudWatch được sử dụng để kiểm tra log của các thành phần trong hệ thống. Việc kiểm thử log giúp đảm bảo khi xảy ra lỗi, người quản trị có thể nhanh chóng tìm nguyên nhân.

Các log cần kiểm tra:

| Thành phần | Log cần kiểm tra |
| :--- | :--- |
| Lambda Backend | Request từ Web/App, lỗi truy vấn dữ liệu |
| Lambda Image Processing | Lỗi đọc ảnh, lỗi gọi Rekognition |
| Lambda Sensor Processing | Payload MQTT, lỗi ghi DynamoDB |
| API Gateway | Request, response, lỗi 4xx/5xx |
| IoT Core | Dữ liệu MQTT từ ESP32 |
| CloudFront/WAF | Request bị chặn hoặc bất thường |

Các bước kiểm thử:

1. Tạo một request hợp lệ và kiểm tra log thành công.
2. Tạo một request sai định dạng và kiểm tra log lỗi.
3. Gửi payload MQTT thiếu trường dữ liệu và kiểm tra Lambda log.
4. Upload ảnh sai định dạng và kiểm tra Lambda Image Processing log.
5. Kiểm tra CloudWatch Log Groups của từng Lambda.

Kết quả mong đợi:

```text
CloudWatch ghi nhận đầy đủ log thành công và log lỗi.
Người quản trị có thể truy vết lỗi theo từng dịch vụ.
```

---

## 3.6.9. Tối ưu hiệu năng hệ thống

Sau khi kiểm thử chức năng, hệ thống cần được tối ưu để hoạt động nhanh hơn, ổn định hơn và phù hợp với số lượng người dùng hoặc thiết bị tăng lên.

Các hướng tối ưu:

- Tối ưu thời gian thực thi của Lambda.
- Tối ưu kích thước ảnh trước khi upload lên S3.
- Sử dụng Presigned URL để giảm tải cho Lambda.
- Thiết kế DynamoDB Partition Key phù hợp.
- Giảm số lần gọi API không cần thiết từ Web/App.
- Sử dụng CloudFront cache để tăng tốc website.
- Thiết lập timeout phù hợp cho Lambda.
- Giảm log không cần thiết để tiết kiệm chi phí CloudWatch.

Ví dụ tối ưu ảnh:

```text
ESP32 Camera giảm kích thước ảnh trước khi upload lên S3.
Điều này giúp upload nhanh hơn và giảm chi phí lưu trữ.
```

Ví dụ tối ưu API:

```text
Web/App chỉ gọi API cập nhật trạng thái bãi xe theo chu kỳ phù hợp,
không gọi API liên tục quá nhiều lần trong thời gian ngắn.
```

---

## 3.6.10. Tối ưu chi phí AWS

Do hệ thống sử dụng nhiều dịch vụ AWS, việc tối ưu chi phí là cần thiết, đặc biệt trong môi trường học tập hoặc demo.

Các cách tối ưu chi phí:

- Xóa ảnh cũ trong S3 nếu không còn cần thiết.
- Cấu hình S3 Lifecycle Rule để chuyển hoặc xóa dữ liệu cũ.
- Giới hạn số lần gọi Amazon Rekognition.
- Giới hạn số lần gọi Amazon Bedrock nếu có dùng AI Service.
- Theo dõi chi phí bằng AWS Budgets.
- Chỉ bật log cần thiết trong CloudWatch.
- Xóa tài nguyên không sử dụng sau khi demo.
- Sử dụng DynamoDB On-Demand cho môi trường thử nghiệm nhỏ.

Ví dụ cấu hình ngân sách:

```text
Monthly Budget: 10 USD
Alert at 50%, 80%, and 100%
Send alert to administrator email
```

Kết quả mong đợi:

```text
Hệ thống vận hành trong mức chi phí dự kiến.
Người quản trị nhận cảnh báo khi chi phí tăng bất thường.
```

---

## 3.6.11. Kết quả kiểm thử tổng hợp

Sau khi kiểm thử từng thành phần, có thể tổng hợp kết quả theo bảng sau:

| Hạng mục kiểm thử | Kết quả mong đợi | Trạng thái |
| :--- | :--- | :--- |
| ESP32 Camera | Chụp và upload ảnh lên S3 | Đạt |
| ESP32 cảm biến | Gửi trạng thái lên AWS IoT Core | Đạt |
| S3 Event | Kích hoạt Lambda xử lý ảnh | Đạt |
| Rekognition | Phân tích ảnh và trả kết quả | Đạt |
| DynamoDB | Lưu dữ liệu chính xác | Đạt |
| API Gateway | Trả dữ liệu cho Web/App | Đạt |
| Cognito | Xác thực người dùng | Đạt |
| CloudWatch | Ghi log hệ thống | Đạt |
| AWS Budgets | Theo dõi chi phí | Đạt |

Bảng này có thể được cập nhật theo kết quả thực tế trong quá trình triển khai và demo.

---

## 3.6.12. Kết luận

Phần kiểm thử và tối ưu hệ thống giúp đảm bảo hệ thống Parking IoT hoạt động đúng theo thiết kế, dữ liệu được truyền từ ESP32 lên AWS chính xác, các Lambda xử lý đúng nhiệm vụ và giao diện Web/App hiển thị dữ liệu đầy đủ.

Thông qua quá trình kiểm thử, nhóm có thể phát hiện lỗi trong từng luồng như upload ảnh, gửi dữ liệu cảm biến, xử lý ảnh, truy vấn API hoặc xác thực người dùng. Bên cạnh đó, việc tối ưu hiệu năng và chi phí giúp hệ thống vận hành ổn định, tiết kiệm và phù hợp với môi trường thực tế.

Sau khi hoàn thành kiểm thử, hệ thống Parking IoT có thể đáp ứng các chức năng chính như giám sát vị trí đỗ xe theo thời gian thực, lưu lịch sử xe ra/vào, nhận diện biển số, hiển thị dữ liệu trên Web/App và hỗ trợ quản trị hệ thống thông qua CloudWatch và AWS Budgets.