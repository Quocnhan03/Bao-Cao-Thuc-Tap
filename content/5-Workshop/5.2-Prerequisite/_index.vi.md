---
title: "Chuẩn bị môi trường"
date: 2026-04-26
weight: 2
chapter: false
pre: " <b> 4.2. </b> "
---

### 4.2. Chuẩn bị môi trường

Để triển khai hệ thống Parking IoT thông minh trên môi trường AWS thực tế, quá trình chuẩn bị tài nguyên phần cứng, phần mềm hỗ trợ và thiết lập quyền truy cập được thực hiện như sau.

#### 1. Tài khoản AWS (AWS Account)
- Sử dụng một tài khoản AWS đang hoạt động bình thường để triển khai toàn bộ tài nguyên.
- Khu vực triển khai (Region) được chọn là **`ap-southeast-1` (Singapore)** nhằm tối ưu hóa tốc độ đường truyền và giảm thiểu độ trễ kết nối từ thiết bị ESP32 tại Việt Nam lên Cloud.
- Tài khoản được phân quyền quản trị viên (AdministratorAccess) hoặc được cấp quyền đầy đủ để khởi tạo các tài nguyên liên quan (IAM Roles, S3, IoT Core, Lambda, API Gateway, DynamoDB, Bedrock).

---

#### 2. Chuẩn bị phần cứng (Hardware Tools)

Dưới đây là danh sách các thiết bị phần cứng được sử dụng để đấu nối và xây dựng mô hình bãi đỗ xe:

| Tên thiết bị | Số lượng | Vai trò trong hệ thống |
| :--- | :---: | :--- |
| **ESP32-CAM (kèm mạch nạp)** | 2 | Đặt tại cổng vào và cổng ra để chụp ảnh phương tiện và upload lên S3 |
| **ESP32-S3 DevKitC-1 v1.1** | 1 | Vi điều khiển trung tâm tại khu vực đỗ xe để xử lý dữ liệu từ các cảm biến siêu âm |
| **Cảm biến siêu âm HC-SR04** | 6 | Đo khoảng cách vật cản tại 6 vị trí đỗ (A1-A3, B1-B3) để xác định trạng thái trống/đầy |
| **IC đệm chuyển đổi mức tín hiệu CD74HC4050** | 1 | IC đệm chuyển đổi mức điện áp tín hiệu Echo (5V) từ 6 cảm biến siêu âm về mức 3.3V an toàn cho các chân nhận tín hiệu (GPIO) của ESP32-S3 |
| **Động cơ Servo SG90** | 2 | Mô phỏng cần chắn Barrier đóng/mở tự động tại cổng vào và cổng ra |
| **Cảm biến tiệm cận hồng ngoại E18-D80NK** | 2 | Phát hiện xe đến gần khu vực cổng vào/ra để kích hoạt ESP32-CAM chụp ảnh |
| **Mạch chuyển đổi mức tín hiệu (Level Shifter 5V -> 3.3V)** | 2 | Chuyển đổi điện áp tín hiệu giữa cảm biến E18-D80NK (5V) và ESP32-CAM (3.3V) |
| **Breadboard & Dây nối** | Nhiều | Đấu nối các linh kiện phần cứng |
| **Đèn LED & Điện trở** | 2 | Phát tín hiệu đèn đỏ (đầy chỗ) và xanh (còn chỗ) |

---

#### 3. Chuẩn bị phần mềm (Software Tools)

- **Arduino IDE:** Được cài đặt trên máy tính để thực hiện viết code, cấu hình và nạp chương trình cho các vi điều khiển ESP32 và ESP32-CAM.
- **Các thư viện bổ sung trên Arduino IDE:**
  - `esp32` board manager: Tích hợp driver và nạp code cho dòng chip ESP32.
  - `PubSubClient` (của tác giả Nick O'Leary): Dùng để truyền nhận dữ liệu qua giao thức MQTT với AWS IoT Core.
  - `ArduinoJson` (phiên bản 6.x trở lên): Dùng để đóng gói các bản tin dữ liệu và phân tích dữ liệu JSON trao đổi giữa thiết bị và Cloud.
- **VS Code:** Trình soạn thảo mã nguồn được sử dụng để viết các đoạn script xử lý logic của hàm AWS Lambda (Python).

---

#### 4. Khởi tạo IAM Service Role cho AWS Lambda

Để các hàm Lambda có thể tương tác với các dịch vụ khác như S3, DynamoDB, Rekognition và Bedrock một cách an toàn, một IAM Service Role chung được khởi tạo.

##### Các bước thực hiện:
1. Truy cập vào **IAM Console** -> chọn mục **Roles** -> chọn **Create role**.
2. Chọn **Trusted entity type** là **AWS service**.
3. Chọn **Use case** là **Lambda** và nhấn **Next**.
4. Tiến hành đính kèm các chính sách quyền (Policies) dưới đây:
   - `AmazonS3FullAccess` (quyền đọc/ghi dữ liệu hình ảnh trên S3 Bucket)
   - `AmazonDynamoDBFullAccess` (quyền truy vấn và cập nhật trạng thái bãi xe)
   - `AmazonRekognitionReadOnlyAccess` (quyền gọi API phân tích ảnh xe)
   - `AmazonBedrockFullAccess` (quyền gọi mô hình ngôn ngữ lớn xử lý truy vấn AI)
   - `CloudWatchLogsFullAccess` (quyền ghi log hoạt động phục vụ giám sát)
5. Đặt tên Role là `SmartParking-Lambda-Role`.
6. Nhấn **Create role** để hoàn tất việc khởi tạo.

---
*Sau khi chuẩn bị đầy đủ phần cứng, phần mềm và cấu hình xong IAM Role, bước tiếp theo là: Thiết lập AWS IoT Core & Amazon S3.*
