---
title: "Dọn dẹp tài nguyên"
date: 2026-04-26
weight: 9
chapter: false
pre: " <b> 4.9. </b> "
---

Sau khi kết thúc thực nghiệm workshop và hoàn thành báo cáo, để tránh phát sinh các chi phí ngoài ý muốn từ các tài nguyên AWS đã khởi tạo, người thực hiện cần tiến hành dọn dẹp (Cleanup) theo trình tự bài bản dưới đây.

---

### 1. Dọn dẹp Cổng phân phối & Lưu trữ tĩnh (CloudFront & S3)
Vì CloudFront và S3 được liên kết trực tiếp, cần vô hiệu hóa phân phối trước khi xóa Buckets.

1. **Amazon CloudFront**:
   - Truy cập giao diện console CloudFront.
   - Chọn Distribution ID `EHS22PYCLM5X0`.
   - Nhấp nút **Disable** (Vô hiệu hóa) và đợi hệ thống chuyển trạng thái sang *Disabled*.
   - Sau khi vô hiệu hóa hoàn tất, chọn distribution và nhấn **Delete** (Xóa).
2. **Amazon S3**:
   - S3 không cho phép xóa bucket khi còn chứa dữ liệu bên trong. Do đó, truy cập vào từng bucket:
     - `smart-parking-fe-prod-075647413376-ap-southeast-1-an`
     - `smart-parking-images-075647413376-ap-southeast-1-an`
   - Nhấp **Empty** (Làm rỗng) để xóa toàn bộ các tệp tin mã nguồn tĩnh và ảnh biển số xe lưu trữ.
   - Sau khi bucket đã rỗng, chọn bucket và nhấp **Delete** (Xóa) để loại bỏ hoàn toàn.

---

### 2. Xóa các điểm API & Trạm xác thực (API Gateway & Cognito)
1. **Amazon Cognito**:
   - Truy cập dịch vụ Cognito, chọn User Pool `User pool - ahlii` (ID: `ap-southeast-1_syJgrpSKt`).
   - Nhấp **Delete** để xóa toàn bộ cơ sở dữ liệu tài khoản người dùng và liên kết App Client.
2. **Amazon API Gateway**:
   - Chọn các API REST phục vụ nghiệp vụ đỗ xe.
   - Chọn **Actions** -> **Delete** để gỡ bỏ các Endpoint công khai khỏi Internet.

---

### 3. Giải phóng tầng logic và đồng bộ realtime (Lambda & AppSync)
1. **AWS AppSync**:
   - Truy cập dịch vụ AppSync, chọn API GraphQL `smart-parking-chat-api`.
   - Chọn **Settings** -> **Delete API** để chấm dứt kết nối WebSocket thời gian thực của cổng chat.
2. **AWS Lambda**:
   - Chọn và xóa toàn bộ các hàm Lambda đã triển khai (ví dụ: `smart-parking-detect-plate`, `smart-parking-slot-update`, `Get_Parking_Status`, v.v.).
3. **IAM Roles**:
   - Truy cập IAM Console -> Roles.
   - Tìm kiếm và xóa các vai trò (Roles) đã cấp quyền cho các hàm Lambda thực thi để giữ sạch tài nguyên bảo mật.

---

### 4. Xóa Cơ sở dữ liệu NoSQL (Amazon DynamoDB)
1. **DynamoDB Tables**:
   - Truy cập DynamoDB Console -> Tables.
   - Chọn các bảng dữ liệu sau:
     - `SmartParking_Slots` (Trạng thái ô đỗ)
     - `SmartParking_VehicleHistory` (Nhật ký xe vào/ra)
     - `SmartParking_ChatLogs` (Lịch sử hội thoại chat)
   - Nhấp **Delete** và xác nhận xóa (nhập `delete` vào ô xác nhận).

---

### 5. Hủy liên kết thiết bị và quy tắc định tuyến (IoT Core & CloudWatch)
1. **AWS IoT Core**:
   - **Quy tắc (Rules)**: Truy cập *Message Routing* -> *Rules*, xóa quy tắc tự động đẩy dữ liệu sang S3/Lambda.
   - **Vật thể (Things)**: Truy cập *Manage* -> *Things*, chọn thiết bị ESP32 và xóa.
   - **Chứng chỉ (Certificates)**: Vô hiệu hóa (Deactivate) và xóa các chứng chỉ SSL được cấp cho ESP32.
2. **Amazon CloudWatch Logs**:
   - Truy cập CloudWatch -> Log Groups.
   - Chọn các nhóm log của các hàm Lambda cũ và nhấp **Delete log group** để tránh lưu trữ log quá hạn gây phát sinh phí dung lượng lưu trữ.
