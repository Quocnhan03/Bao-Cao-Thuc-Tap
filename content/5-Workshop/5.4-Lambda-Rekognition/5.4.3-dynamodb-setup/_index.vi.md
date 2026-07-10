---
title: "Thiết kế cơ sở dữ liệu DynamoDB"
date: 2026-04-26
weight: 3
chapter: false
pre: " <b> 4.4.3. </b> "
---

Để lưu trữ trạng thái hoạt động của các chỗ đỗ xe và lịch sử phương tiện ra vào theo thời gian thực, dịch vụ cơ sở dữ liệu NoSQL **Amazon DynamoDB** được sử dụng làm kho lưu trữ trung tâm của hệ thống.

---

### 1. Danh sách các bảng dữ liệu trong hệ thống
Hệ thống thiết lập 3 bảng cơ sở dữ liệu chính trên Amazon DynamoDB để quản lý thông tin:
- `SmartParking_Slots`: Lưu trữ thông tin và trạng thái trống/đầy của từng chỗ đỗ xe.
- `SmartParking_VehicleHistory`: Lưu trữ nhật ký chi tiết các lượt xe ra/vào bãi đỗ.
- `SmartParking_GateCommands`: Lưu trữ lịch sử lệnh điều khiển cổng chắn (Barrier).

![Danh sách Bảng DynamoDB](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.3-dynamodb.png)
*Minh chứng 5.4.3.1: Các bảng dữ liệu của hệ thống Parking IoT trên giao diện quản lý Amazon DynamoDB*

---

### 2. Thiết kế lược đồ bảng (Schema Design)

#### 2.1. Bảng Trạng thái Chỗ đỗ (`SmartParking_Slots`)
Bảng này quản lý danh sách các chỗ đỗ xe trong bãi và trạng thái trống/đầy hiện tại của chúng.
- **Partition Key (Khóa phân vùng)**: `slot_id` (Kiểu dữ liệu String - S)
- **Cấu trúc thuộc tính mẫu**:
```json
{
  "slot_id": "slot-01",
  "occupied": true,
  "last_updated": 1783683112000
}
```

#### 2.2. Bảng Lịch sử Phương tiện (`SmartParking_VehicleHistory`)
Bảng này lưu nhật ký mọi sự kiện xe ra vào bãi đỗ, hỗ trợ việc đối soát và hiển thị trên giao diện người dùng.
- **Partition Key (Khóa phân vùng)**: `plate_number` (Kiểu dữ liệu String - S, biển số xe viết liền không dấu).
- **Sort Key (Khóa sắp xếp)**: `timestamp` (Kiểu dữ liệu Number - N, thời gian Unix tính bằng mili-giây).
- **Các thuộc tính chi tiết cấu hình thực tế**:
  - `allow_open` (Boolean): Cho phép mở barie (True/False).
  - `bucket` (String): S3 bucket lưu trữ ảnh.
  - `camera_id` (String): Định danh camera chụp.
  - `confidence` (Number): Độ tin cậy của thuật toán nhận diện chữ (phần trăm).
  - `created_at` (String): Định dạng thời gian dạng chuỗi đọc được (`YYYY-MM-DD HH:MM:SS`).
  - `device_id` (String): Định danh thiết bị điều khiển cổng.
  - `direction` (String): Chiều di chuyển (`IN` hoặc `OUT`).
  - `display_plate_number` (String): Định dạng biển số hiển thị (Ví dụ: `29A-179.38`).
  - `event_id` (String): ID duy nhất sinh ra cho sự kiện.
  - `image_key` (String): Đường dẫn tệp ảnh trên S3.

Lược đồ dữ liệu thực tế lưu trữ trong cơ sở dữ liệu:
```json
{
  "plate_number": "29A17938",
  "timestamp": 1782032316749,
  "allow_open": true,
  "bucket": "smart-parking-images-075647413376-ap-southeast-1-an",
  "camera_id": "gate-in-01",
  "confidence": 98.23297882080078,
  "created_at": "2026-06-21 14:05:16",
  "device_id": "gate-in-01",
  "direction": "IN",
  "display_plate_number": "29A-179.38",
  "event_id": "evt_29A17938_1782032316",
  "image_key": "parking/in/29A17938.jpg"
}
```

#### 2.3. Bảng Lệnh điều khiển Cổng chắn (`SmartParking_GateCommands`)
Bảng này lưu giữ các lệnh điều khiển cổng chắn được gửi đi từ hệ thống điều khiển trung tâm hoặc từ hành vi bấm nút thủ công trên web.
- **Partition Key (Khóa phân vùng)**: `device_id` (Kiểu dữ liệu String - S, định danh cổng kiểm soát).
- **Sort Key (Khóa sắp xếp)**: `created_at` (Kiểu dữ liệu Number - N, thời gian gửi lệnh).
- **Cấu trúc thuộc tính mẫu**:
```json
{
  "device_id": "gate-controller-01",
  "created_at": 1783683112000,
  "command": "OPEN",
  "status": "PENDING"
}
```

---

### 3. Lý do lựa chọn giải pháp
**Amazon DynamoDB** được lựa chọn làm cơ sở dữ liệu cho dự án nhờ vào các đặc tính kỹ thuật phù hợp với mô hình IoT:
1. **Hiệu năng cao và độ trễ thấp**: DynamoDB cung cấp tốc độ phản hồi đọc/ghi dưới 10 mili-giây, giúp trạm kiểm soát xử lý mở cổng chắn gần như ngay lập tức khi có kết quả phân tích biển số.
2. **Kiến trúc Serverless hoàn toàn**: Không cần quản trị máy chủ cơ sở dữ liệu, tự động mở rộng tài nguyên lưu trữ và thanh toán theo số lượng yêu cầu đọc/ghi thực tế (On-demand capacity mode).
3. **Mô hình Schema-less linh hoạt**: Dễ dàng thêm bớt các thuộc tính của dữ liệu IoT (như tọa độ bounding box của biển số xe, mã số thẻ từ phụ) mà không cần thực hiện di chuyển cơ sở dữ liệu phức tạp.
