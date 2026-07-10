---
title: "Bản đề xuất"
date: 2026-04-26
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# Nền tảng Parking IoT thông minh với AWS Serverless

> **Giải pháp AWS Serverless cho giám sát bãi đỗ xe, nhận diện biển số và hỗ trợ AI**

---

## 1. Tóm tắt điều hành

Dự án nhằm xây dựng hệ thống **Parking IoT thông minh** giúp tự động hóa quá trình giám sát bãi đỗ xe, nhận diện phương tiện và quản lý dữ liệu theo thời gian thực. Hệ thống sử dụng các thiết bị IoT như **ESP32 Camera** và **ESP32 cảm biến** để thu thập hình ảnh xe ra/vào, trạng thái vị trí đỗ và dữ liệu từ bãi xe.

Dữ liệu từ thiết bị được gửi lên AWS thông qua các dịch vụ như **AWS IoT Core**, **Amazon S3**, **Amazon API Gateway** và được xử lý bằng **AWS Lambda**. Hình ảnh phương tiện được lưu trữ trong **Amazon S3**, sau đó kích hoạt Lambda để xử lý ảnh và gọi **Amazon Rekognition** nhằm nhận diện biển số xe. Kết quả nhận diện và dữ liệu cảm biến được lưu vào **Amazon DynamoDB** để phục vụ việc tra cứu, quản lý và hiển thị trên Web/App.

Ngoài ra, hệ thống còn tích hợp **Amazon Bedrock** thông qua lớp **Lambda AI Service** để hỗ trợ phân tích dữ liệu, trả lời các truy vấn thông minh và cung cấp trải nghiệm quản lý bãi đỗ xe hiện đại hơn. Với kiến trúc AWS Serverless, hệ thống có khả năng mở rộng linh hoạt, giảm chi phí vận hành và không cần quản lý máy chủ truyền thống.

---

## 2. Tuyên bố vấn đề

### 2.1. Thách thức hiện tại

Các bãi đỗ xe truyền thống thường gặp nhiều hạn chế trong quá trình vận hành và quản lý. Việc kiểm soát xe ra/vào còn phụ thuộc nhiều vào con người, dễ xảy ra sai sót khi ghi nhận biển số, thời gian vào bãi hoặc trạng thái chỗ đỗ. Khi số lượng phương tiện tăng lên, việc quản lý thủ công sẽ trở nên khó khăn, thiếu tính chính xác và mất nhiều thời gian.

Một số vấn đề chính có thể kể đến như:
- Khó kiểm tra nhanh tình trạng còn trống hoặc đã đầy của từng vị trí đỗ xe.
- Việc ghi nhận xe ra/vào còn thủ công, dễ nhầm lẫn biển số hoặc thời gian.
- Dữ liệu hình ảnh, biển số và trạng thái bãi xe chưa được quản lý tập trung.
- Người quản lý khó theo dõi lịch sử hoạt động của phương tiện.
- Khó mở rộng hệ thống khi số lượng camera, cảm biến hoặc vị trí đỗ tăng lên.
- Việc xây dựng hệ thống riêng có thể tốn chi phí nếu phải đầu tư máy chủ vật lý.

### 2.2. Giải pháp đề xuất

Dự án đề xuất xây dựng hệ thống Parking IoT thông minh trên nền tảng AWS Serverless. Hệ thống sử dụng ESP32 Camera để chụp ảnh xe ra/vào, ESP32 cảm biến để ghi nhận trạng thái chỗ đỗ, sau đó gửi dữ liệu lên AWS để xử lý và lưu trữ tập trung.

**Giải pháp bao gồm các chức năng chính:**
- **ESP32 Camera** chụp ảnh phương tiện khi xe ra hoặc vào bãi.
- **ESP32 cảm biến** phát hiện trạng thái từng vị trí đỗ xe.
- Ảnh xe được tải lên **Amazon S3** thông qua Presigned URL.
- **AWS Lambda** xử lý sự kiện khi có ảnh mới được upload lên S3.
- **Amazon Rekognition** phân tích hình ảnh và hỗ trợ nhận diện biển số xe.
- **DynamoDB** lưu thông tin xe, biển số, thời gian, trạng thái và dữ liệu cảm biến.
- **Web/App** cho người dùng truy cập, đăng nhập, xem trạng thái bãi xe và lịch sử xe ra/vào.
- **Amazon Cognito** hỗ trợ xác thực và phân quyền người dùng.
- **Amazon Bedrock** hỗ trợ lớp AI để phân tích dữ liệu và trả lời câu hỏi thông minh.
- **Amazon CloudWatch** giám sát log, lỗi và trạng thái hoạt động của hệ thống.

### 2.3. Hiệu quả kỳ vọng

Hệ thống giúp giảm thao tác thủ công, tăng độ chính xác trong quản lý bãi xe, hỗ trợ giám sát theo thời gian thực và tạo nền tảng dữ liệu phục vụ phân tích AI trong tương lai. Nhờ sử dụng kiến trúc Serverless, hệ thống có thể mở rộng linh hoạt theo số lượng thiết bị, số lượng xe và nhu cầu sử dụng thực tế.

### 2.4. Phạm vi dự án

Việc xác định rõ giới hạn của dự án giúp tập trung vào các tính năng cốt lõi và đảm bảo tính khả thi trong quá trình triển khai:
- **Trong phạm vi:** Nhận diện biển số xe bằng AI, ghi nhận trạng thái chỗ đỗ bằng cảm biến, tự động lưu lịch sử ra/vào, ra quyết định mở cổng, hiển thị dashboard giám sát trên Web App và hỗ trợ truy vấn bằng trợ lý ảo Bedrock.
- **Ngoài phạm vi:** Tạm thời chưa tích hợp module thanh toán phí đỗ xe trực tuyến, chưa làm ứng dụng Mobile App native (chỉ tập trung tối ưu trên nền tảng Web App).

### 2.5. Mục tiêu cụ thể (KPIs)

Dự án đặt ra các mục tiêu kỹ thuật cụ thể có thể đo lường được để đánh giá sự thành công:
- **Độ trễ (Latency):** Thời gian từ lúc chụp ảnh đến lúc lưu dữ liệu, phân tích biển số và ra lệnh mở cổng dưới 2-3 giây.
- **Độ chính xác (Accuracy):** Tỷ lệ nhận diện đúng biển số xe (Confidence score) đạt trên 95% trong điều kiện ánh sáng tốt.
- **Độ ổn định:** Hạ tầng AWS Serverless đảm bảo thời gian hoạt động (uptime) lên đến 99.9%, tự động mở rộng khi lưu lượng tăng đột biến.

---

## 3. Kiến trúc giải pháp

Hệ thống áp dụng kiến trúc **AWS Serverless** nhằm giảm chi phí quản lý hạ tầng, tăng khả năng mở rộng và dễ dàng tích hợp với các dịch vụ AI, IoT và cơ sở dữ liệu trên AWS.

*Sơ đồ kiến trúc tổng thể (AWS Serverless Architecture):*

![Sơ đồ kiến trúc tổng thể - Smart Parking IoT](/images/2-Proposal/2-proposal-architecture.png)

### 3.1. Các dịch vụ AWS chủ chốt

| Phân hệ | Dịch vụ AWS | Chức năng |
| :--- | :--- | :--- |
| **Giao diện người dùng** | Amazon Route 53 <br> Amazon CloudFront <br> AWS WAF <br> Amazon S3 Static Website | Quản lý tên miền. <br> Phân phối nội dung website. <br> Bảo vệ website khỏi truy cập độc hại. <br> Lưu trữ giao diện Web/App tĩnh. |
| **Xác thực & Phân quyền** | Amazon Cognito <br> IAM | Quản lý đăng nhập, xác thực. <br> Quản lý quyền truy cập giữa các dịch vụ. |
| **API & Backend** | Amazon API Gateway <br> AWS Lambda | Nhận request từ Web/App/Thiết bị. <br> Xử lý nghiệp vụ chính, xử lý ảnh, dữ liệu cảm biến và AI. |
| **IoT & Thiết bị biên** | AWS IoT Core <br> ESP32 Camera / Cảm biến | Nhận dữ liệu MQTT từ thiết bị IoT. <br> Thu thập hình ảnh và trạng thái chỗ đỗ. |
| **Lưu trữ & Database** | Amazon S3 <br> Amazon DynamoDB | Lưu trữ hình ảnh xe. <br> Lưu dữ liệu biển số, lịch sử, trạng thái chỗ đỗ. |
| **Xử lý ảnh & AI** | Amazon Rekognition <br> Amazon Bedrock | Phân tích ảnh, nhận diện biển số. <br> Hỗ trợ phân tích dữ liệu, truy vấn thông minh. |
| **Giám sát hệ thống** | Amazon CloudWatch | Ghi log, theo dõi lỗi, giám sát các thành phần liên quan. |

---

## 4. Luồng hoạt động của hệ thống

### 4.1. Luồng truy cập Web/App

Người dùng truy cập hệ thống thông qua trình duyệt web hoặc thiết bị di động. Website được lưu trữ trên Amazon S3 Static Website và phân phối thông qua Amazon CloudFront.

```text
Người dùng → Route 53 → CloudFront → AWS WAF → Amazon S3 Static Website → API Gateway → Lambda Backend → DynamoDB
```

### 4.2. Luồng xác thực người dùng

Hệ thống sử dụng Amazon Cognito để xác thực người dùng. Cognito cấp token để Web/App gửi kèm trong các request đến API Gateway.

```text
Người dùng → Amazon Cognito → API Gateway (Cognito Authorizer) → Lambda Backend → DynamoDB
```

### 4.3. Sơ đồ mạch điện khu vực cổng ra/vào (ESP32 Camera)

Khu vực cổng được trang bị vi điều khiển ESP32 kết hợp Camera module để nhận diện phương tiện ra vào bãi đỗ.

![Sơ đồ đấu dây cổng](/images/2-Proposal/1.sơ%20đồ%20đấu%20dây%20cổng.png)


**Ví dụ dữ liệu lịch sử xe ra/vào được lưu:**
```json
{
  "plate_number": "29A17938",
  "timestamp": 1782032316749,
  "allow_open": true,
  "bucket": "smart-parking-images-075647413376-ap-southeast-1-an",
  "camera_id": "gate-in-01",
  "confidence": 98.23,
  "created_at": "2026-06-21T15:58:36.749547+07:00",
  "device_id": "gate-in-01",
  "direction": "IN",
  "display_plate_number": "29A-179.38",
  "event_id": "evt_29A17938_1782032316749_IN_21668d9a",
  "image_key": "parking/in/photo-1782032314126-8770cde7.jpg",
  "raw_plate_number": "29A-179.38",
  "status": "ALLOWED",
  "vehicle_type": "GUEST"
}
```

### 4.4. Sơ đồ mạch điện khu vực đỗ xe (ESP32 Cảm biến)

Các vị trí đỗ xe được trang bị cảm biến (siêu âm/hồng ngoại) kết nối với vi điều khiển ESP32 để theo dõi trạng thái trống/đầy.

![Sơ đồ đấu dây bãi xe](/images/2-Proposal/2.sơ%20đồ%20dây%20bãi%20xe.png)


**Ví dụ dữ liệu cảm biến lưu trữ cho mỗi vị trí đỗ:**
```json
{
  "slot_id": "A1",
  "distance_cm": 2.8,
  "is_occupied": 1,
  "sensor_id": "esp-slot-01",
  "threshold_cm": 3.5,
  "updated_at": "2026-07-09T17:33:56.017039+07:00",
  "zone": "Zone_A",
  "zone_id": "A"
}
```

### 4.5. Luồng xử lý AI Service

Hệ thống tích hợp lớp AI để hỗ trợ người dùng và quản trị viên truy vấn dữ liệu bãi đỗ xe bằng ngôn ngữ tự nhiên.

```text
Web/App → API Gateway → Lambda AI Service → Amazon Bedrock → DynamoDB → Web/App
```

### 4.6. Luồng giám sát hệ thống

Amazon CloudWatch được sử dụng để ghi log và giám sát hoạt động của toàn bộ các dịch vụ.

```text
API Gateway / Lambda / IoT Core / Rekognition / DynamoDB → CloudWatch
```

---

## 5. Triển khai kỹ thuật

| Giai đoạn | Nội dung |
| :--- | :--- |
| **Giai đoạn 1: Phân tích & thiết kế** | Xác định phạm vi triển khai, số lượng camera/cảm biến, thiết kế sơ đồ kiến trúc và cơ sở dữ liệu. |
| **Giai đoạn 2: Triển khai IoT** | Cấu hình ESP32 Camera chụp ảnh và ESP32 cảm biến kết nối MQTT với AWS IoT Core. |
| **Giai đoạn 3: AWS Backend** | Tạo API Gateway, Lambda Functions, S3 Buckets, DynamoDB tables và tích hợp Rekognition. |
| **Giai đoạn 4: Xây dựng Web/App** | Phát triển giao diện người dùng, tích hợp Cognito xác thực và hiển thị trạng thái bãi xe. |
| **Giai đoạn 5: AI & Giám sát** | Cấu hình Amazon Bedrock, thiết lập CloudWatch logging và báo động (Alarms). |

---

## 6. Ước tính ngân sách

### 6.1. Chi phí phần cứng
- **ESP32 Camera**: Theo số cổng ra/vào.
- **ESP32 cảm biến & Cảm biến siêu âm**: Theo số vị trí đỗ.
- **Phụ kiện**: Nguồn điện, dây nối, hộp bảo vệ, Router/WiFi.

### 6.2. Chi phí dịch vụ AWS (Pay-as-you-go)
- **Tính toán & Xử lý**: AWS Lambda, Amazon Rekognition, Amazon Bedrock.
- **Lưu trữ**: Amazon S3 (Ảnh), Amazon DynamoDB (Dữ liệu).
- **Mạng & API**: AWS IoT Core, Amazon API Gateway, Amazon CloudFront.
- **Quản lý**: Amazon Cognito, Amazon CloudWatch, AWS Budgets.

---

## 7. Đánh giá rủi ro & Phương án dự phòng

| Rủi ro | Mức độ | Phương án dự phòng |
| :--- | :--- | :--- |
| **Thiết bị mất kết nối mạng** | Trung bình | Lưu tạm dữ liệu cục bộ và gửi lại khi có mạng. |
| **Ảnh biển số bị mờ** | Cao | Điều chỉnh góc camera, ánh sáng và khoảng cách chụp. |
| **Nhận diện biển số sai** | Trung bình | Kết hợp kiểm tra thủ công và nâng cao chất lượng ảnh. |
| **Lỗi dịch vụ AWS (Lambda, API)**| Trung bình | Theo dõi CloudWatch Alarms để xử lý kịp thời. |
| **Vượt ngân sách AWS** | Trung bình | Thiết lập AWS Budgets để tự động cảnh báo. |

---

## 8. Kết luận

Dự án **Parking IoT thông minh** sử dụng AWS Serverless là giải pháp phù hợp để hiện đại hóa việc quản lý bãi đỗ xe. Sự kết hợp giữa **IoT, Serverless và AI (Rekognition, Bedrock)** tạo ra nền tảng quản lý tự động, độ chính xác cao và khả năng mở rộng không giới hạn mà không cần duy trì máy chủ vật lý.
