---
title : "Tổng quan về Workshop"
date : 2026-04-26
weight : 1
chapter : false
pre : " <b> 4.1. </b> "
---

### 4.1. Tổng quan & Kiến trúc hệ thống

#### Tổng quan dự án

**Hệ thống Parking IoT thông minh** được xây dựng trên nền tảng AWS Serverless nhằm giải quyết bài toán tự động hóa quản lý bãi đỗ xe hiện đại. Hệ thống tích hợp các cảm biến và camera biên để thu thập dữ liệu về phương tiện, xử lý tự động trên môi trường Cloud, và cung cấp khả năng tương tác thông minh thông qua Trí tuệ nhân tạo (AI).

Hệ thống được chia thành 3 phần chính:
- **Thiết bị biên (Edge Devices):**
  - **ESP32 Camera:** Đặt tại cổng ra/vào để tự động chụp ảnh phương tiện khi phát hiện xe và tải lên Cloud.
  - **ESP32 Cảm biến:** Sử dụng cảm biến siêu âm gắn tại mỗi vị trí đỗ để phát hiện trạng thái trống/đầy và gửi dữ liệu lên Cloud.
- **Hạ tầng AWS Cloud (Backend):** Tiếp nhận dữ liệu, xử lý ảnh bằng AI (nhận diện biển số), lưu cơ sở dữ liệu và cung cấp API.
- **Giao diện người dùng (Frontend):** Dashboard thời gian thực cho người quản lý và giao diện hỗ trợ truy vấn thông qua chatbot AI (Amazon Bedrock).

---

#### Sơ đồ kiến trúc tổng thể

*Hệ thống áp dụng kiến trúc Serverless 100%, tự động mở rộng theo lưu lượng thực tế:*

![Sơ đồ kiến trúc tổng thể](/images/2-Proposal/2-proposal-architecture.png)

---

#### Sơ đồ đấu dây phần cứng (Wiring Diagrams)

##### 1. Khu vực cổng ra/vào (ESP32 Camera)
Sử dụng vi điều khiển ESP32-CAM kết hợp cảm biến tiệm cận/nút bấm để kích hoạt chụp ảnh và điều khiển servo làm cổng chắn (barrier).

![Sơ đồ đấu dây cổng](/images/2-Proposal/1.sơ%20đồ%20đấu%20dây%20cổng.png)

##### 2. Khu vực đỗ xe (ESP32 Cảm biến)
Sử dụng vi điều khiển ESP32 kết hợp cảm biến siêu âm HC-SR04 để đo khoảng cách và xác định xe có đang đỗ tại vị trí đó hay không.

![Sơ đồ đấu dây bãi xe](/images/2-Proposal/2.sơ%20đồ%20dây%20bãi%20xe.png)

---

#### Danh sách dịch vụ AWS sử dụng

| Dịch vụ | Vai trò trong hệ thống |
| :--- | :--- |
| **AWS IoT Core** | Tiếp nhận dữ liệu MQTT từ ESP32 cảm biến ở bãi xe theo thời gian thực. |
| **Amazon S3** | Lưu trữ hình ảnh xe chụp từ cổng ra/vào. Đồng thời làm hosting cho Web Dashboard tĩnh. |
| **AWS Lambda** | Đóng vai trò xử lý logic nghiệp vụ chính (cấp presigned URL, xử lý sự kiện S3, gọi Rekognition, cập nhật DynamoDB, gọi Bedrock). |
| **Amazon Rekognition** | Tự động phân tích hình ảnh xe để nhận diện biển số chữ và số. |
| **Amazon DynamoDB** | Cơ sở dữ liệu NoSQL lưu lịch sử xe ra/vào bãi đỗ và trạng thái chi tiết của từng vị trí đỗ xe. |
| **Amazon API Gateway** | Cung cấp các RESTful API endpoints phục vụ Web/App và thiết bị biên. |
| **Amazon Cognito** | Quản lý đăng nhập, cấp token xác thực cho Web Dashboard để gọi API. |
| **Amazon Bedrock** | Hỗ trợ mô hình ngôn ngữ lớn (LLM) để trả lời các câu hỏi truy vấn dữ liệu bãi xe bằng ngôn ngữ tự nhiên. |
| **Amazon CloudWatch** | Giám sát toàn bộ log hệ thống, theo dõi lỗi và hoạt động của Lambda. |
