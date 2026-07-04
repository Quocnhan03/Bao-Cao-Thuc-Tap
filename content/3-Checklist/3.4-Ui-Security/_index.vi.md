---
title : "Giao diện và bảo mật"
date :  "`r Sys.Date()`" 
weight : 4
chapter : false
pre : " <b> 3.4. </b> "
---

# 3.4. Giao diện và bảo mật

Phần này trình bày cách triển khai giao diện người dùng và các cơ chế bảo mật cho hệ thống **Parking IoT thông minh**. Giao diện Web/App giúp người dùng theo dõi trạng thái bãi đỗ xe, xem lịch sử xe ra/vào, kiểm tra biển số và truy vấn dữ liệu từ hệ thống.

Bên cạnh đó, hệ thống sử dụng các dịch vụ bảo mật như **Amazon Cognito, AWS WAF, IAM, API Gateway Authorizer và CloudFront HTTPS** để đảm bảo người dùng được xác thực, dữ liệu được bảo vệ và các dịch vụ AWS chỉ được cấp đúng quyền cần thiết.

---

## 3.4.1. Tổng quan giao diện Web/App

Giao diện Web/App là nơi người dùng tương tác trực tiếp với hệ thống Parking IoT. Thông qua giao diện này, người dùng có thể xem dữ liệu bãi xe theo thời gian thực, kiểm tra trạng thái từng vị trí đỗ và theo dõi lịch sử xe ra/vào.

Các chức năng chính của giao diện gồm:

- Đăng nhập hệ thống.
- Xem tổng số vị trí đỗ xe.
- Xem số lượng chỗ trống và chỗ đã có xe.
- Xem trạng thái từng vị trí đỗ.
- Xem lịch sử xe vào và xe ra.
- Xem hình ảnh xe đã được lưu trên Amazon S3.
- Xem biển số xe được nhận diện.
- Tìm kiếm xe theo biển số.
- Xem thống kê hoạt động của bãi xe.
- Gửi câu hỏi đến AI Service nếu có tích hợp Amazon Bedrock.

Giao diện có thể được xây dựng bằng HTML/CSS/JavaScript hoặc các framework như React, Next.js. Sau khi build, các file tĩnh sẽ được lưu trữ trên Amazon S3 và phân phối đến người dùng thông qua Amazon CloudFront.

---

## 3.4.2. Triển khai giao diện bằng Amazon S3 Static Website

Amazon S3 được sử dụng để lưu trữ các file tĩnh của giao diện Web/App, bao gồm:

- File HTML.
- File CSS.
- File JavaScript.
- Hình ảnh, icon và các tài nguyên giao diện khác.

Luồng triển khai giao diện:

```text
Source Code Web/App → Build Project → Upload file tĩnh lên Amazon S3 → CloudFront phân phối đến người dùng
```

Ví dụ cấu trúc file giao diện sau khi build:

```text
web-app-build/
├── index.html
├── assets/
│   ├── style.css
│   ├── app.js
│   └── logo.png
└── dashboard/
    └── index.html
```

Amazon S3 giúp lưu trữ giao diện đơn giản, chi phí thấp và phù hợp với mô hình serverless.

---

## 3.4.3. Phân phối website bằng Amazon CloudFront

Amazon CloudFront được sử dụng để phân phối giao diện Web/App đến người dùng với tốc độ nhanh hơn. CloudFront đóng vai trò trung gian giữa người dùng và Amazon S3.

Luồng truy cập website:

```text
User → Route 53 → CloudFront → Amazon S3 Static Website
```

Vai trò của CloudFront:

- Tăng tốc độ truy cập website.
- Giảm độ trễ cho người dùng.
- Hỗ trợ HTTPS để bảo mật kết nối.
- Giảm tải trực tiếp cho Amazon S3.
- Hỗ trợ tích hợp với AWS WAF để bảo vệ website.

Khi người dùng truy cập website, CloudFront sẽ lấy nội dung từ S3 và cache tại các edge location. Điều này giúp website phản hồi nhanh hơn, đặc biệt khi có nhiều người dùng truy cập cùng lúc.

---

## 3.4.4. Quản lý tên miền bằng Amazon Route 53

Amazon Route 53 được sử dụng để quản lý tên miền của hệ thống. Thay vì người dùng phải truy cập bằng đường dẫn CloudFront dài và khó nhớ, Route 53 giúp ánh xạ tên miền thân thiện đến CloudFront.

Ví dụ:

```text
parking.example.com → CloudFront Distribution
```

Vai trò của Route 53:

- Quản lý DNS cho hệ thống.
- Điều hướng người dùng đến CloudFront.
- Giúp website có địa chỉ truy cập dễ nhớ hơn.
- Hỗ trợ cấu hình domain cho môi trường demo hoặc production.

Luồng truy cập khi có Route 53:

```text
User nhập tên miền → Route 53 → CloudFront → S3 Static Website
```

---

## 3.4.5. Bảo vệ website bằng AWS WAF

AWS WAF được đặt trước CloudFront để bảo vệ website khỏi các request bất thường hoặc độc hại. WAF giúp tăng mức độ an toàn cho hệ thống khi website được public ra Internet.

Luồng bảo vệ website:

```text
User → Route 53 → CloudFront + AWS WAF → Amazon S3 Static Website
```

AWS WAF có thể hỗ trợ:

- Chặn IP đáng ngờ.
- Chặn request có định dạng bất thường.
- Giới hạn số lượng request từ một nguồn.
- Bảo vệ website khỏi một số dạng tấn công phổ biến.
- Tạo rule để lọc request không hợp lệ.

Trong hệ thống Parking IoT, WAF giúp bảo vệ lớp giao diện trước khi request được chuyển đến Web/App hoặc API.

---

## 3.4.6. Xác thực người dùng bằng Amazon Cognito

Amazon Cognito được sử dụng để xác thực người dùng trước khi cho phép truy cập vào các chức năng quản lý bãi xe. Người dùng cần đăng nhập bằng tài khoản đã được cấp.

Luồng xác thực:

```text
User → Web/App → Amazon Cognito → Nhận Token → API Gateway → Lambda Backend
```

Các bước xử lý:

1. Người dùng mở Web/App.
2. Người dùng nhập tài khoản và mật khẩu.
3. Web/App gửi thông tin đăng nhập đến Amazon Cognito.
4. Cognito kiểm tra thông tin người dùng.
5. Nếu đăng nhập thành công, Cognito trả về token.
6. Web/App gửi token kèm theo các request đến API Gateway.
7. API Gateway kiểm tra token bằng Cognito Authorizer.
8. Nếu token hợp lệ, request được chuyển đến Lambda Backend.

Amazon Cognito giúp hệ thống quản lý đăng nhập tập trung, an toàn và dễ tích hợp với API Gateway.

---

## 3.4.7. Phân quyền người dùng

Hệ thống có thể chia người dùng thành nhiều vai trò khác nhau để kiểm soát quyền truy cập. Mỗi vai trò sẽ được phép sử dụng các chức năng khác nhau trên Web/App.

Ví dụ phân quyền:

| Vai trò | Quyền truy cập |
| :--- | :--- |
| User | Xem trạng thái bãi xe và số chỗ trống |
| Manager | Xem lịch sử xe ra/vào, thống kê và dữ liệu biển số |
| Admin | Quản lý người dùng, cấu hình hệ thống và kiểm tra toàn bộ dữ liệu |

Việc phân quyền giúp hạn chế người dùng truy cập vào các chức năng không phù hợp. Ví dụ, người dùng thông thường chỉ có quyền xem trạng thái bãi xe, trong khi Admin có quyền quản lý tài khoản và cấu hình hệ thống.

---

## 3.4.8. Bảo mật API bằng API Gateway Authorizer

API Gateway là cổng giao tiếp giữa Web/App và Lambda Backend. Để bảo vệ API, hệ thống sử dụng Cognito Authorizer nhằm kiểm tra token của người dùng trước khi cho phép gọi API.

Luồng bảo mật API:

```text
Web/App → API Gateway → Cognito Authorizer → Lambda Backend → DynamoDB
```

Cách hoạt động:

1. Web/App gửi request đến API Gateway.
2. Request có kèm token từ Amazon Cognito.
3. API Gateway kiểm tra token bằng Cognito Authorizer.
4. Nếu token hợp lệ, request được chuyển đến Lambda.
5. Nếu token không hợp lệ, API Gateway từ chối request.

Một số API cần bảo vệ:

| API Endpoint | Mục đích |
| :--- | :--- |
| `/parking/slots` | Lấy trạng thái vị trí đỗ |
| `/vehicle/logs` | Xem lịch sử xe ra/vào |
| `/vehicle/search` | Tìm kiếm xe theo biển số |
| `/ai/query` | Gửi câu hỏi đến AI Service |
| `/admin/users` | Quản lý người dùng |

Cách làm này giúp hạn chế truy cập trái phép vào dữ liệu bãi xe.

---

## 3.4.9. Bảo mật quyền truy cập bằng IAM

IAM được sử dụng để kiểm soát quyền giữa các dịch vụ AWS. Mỗi dịch vụ chỉ được cấp đúng quyền cần thiết theo nguyên tắc **Least Privilege**.

Ví dụ phân quyền IAM:

| Thành phần | Quyền cần có |
| :--- | :--- |
| Lambda Backend | Đọc/ghi DynamoDB |
| Lambda Image Processing | Đọc ảnh từ S3, gọi Rekognition, ghi DynamoDB |
| Lambda Presigned URL | Tạo Presigned URL cho S3 |
| Lambda Sensor Processing | Ghi dữ liệu cảm biến vào DynamoDB |
| Lambda AI Service | Đọc DynamoDB và gọi Amazon Bedrock |
| API Gateway | Gọi Lambda |
| IoT Rule | Kích hoạt Lambda xử lý cảm biến |

Nguyên tắc quan trọng:

```text
Không cấp quyền quá rộng.
Mỗi Lambda chỉ được cấp quyền đúng với nhiệm vụ của nó.
Thiết bị ESP32 không được lưu Access Key hoặc Secret Key trực tiếp.
```

IAM giúp giảm rủi ro bảo mật nếu một thành phần bị lỗi hoặc bị truy cập trái phép.

---

## 3.4.10. Bảo mật upload ảnh bằng Presigned URL

ESP32 Camera không được cấp quyền AWS trực tiếp để upload ảnh lên S3. Thay vào đó, hệ thống sử dụng Presigned URL.

Luồng upload ảnh an toàn:

```text
ESP32 Camera → API Gateway → Lambda tạo Presigned URL → ESP32 Camera upload ảnh lên S3
```

Lợi ích của Presigned URL:

- Không cần lưu Access Key trên ESP32 Camera.
- URL chỉ có hiệu lực trong thời gian ngắn.
- Chỉ cho phép upload đúng file hoặc đúng bucket được chỉ định.
- Giảm rủi ro khi thiết bị bị truy cập trái phép.

Ví dụ:

```text
Presigned URL có hiệu lực trong 5 phút.
ESP32 Camera chỉ được upload ảnh vào thư mục entrance/ hoặc exit/.
```

Cách làm này phù hợp với hệ thống IoT vì thiết bị biên thường có tài nguyên hạn chế và cần hạn chế lưu thông tin nhạy cảm.

---

## 3.4.11. Bảo mật kết nối thiết bị IoT

Đối với ESP32 cảm biến, thiết bị gửi dữ liệu lên AWS IoT Core thông qua MQTT. Để bảo mật kết nối, mỗi thiết bị cần có chứng chỉ riêng và IoT Policy phù hợp.

Các thành phần bảo mật gồm:

- IoT Thing đại diện cho thiết bị.
- Device Certificate.
- Private Key.
- IoT Policy.
- MQTT Topic riêng cho từng thiết bị.

Ví dụ topic:

```text
parking/slot/A01/status
```

Ví dụ nguyên tắc phân quyền:

```text
ESP32 Sensor A01 chỉ được publish vào topic parking/slot/A01/status.
ESP32 Sensor B03 chỉ được publish vào topic parking/slot/B03/status.
```

Việc giới hạn topic giúp giảm rủi ro khi một thiết bị gửi sai dữ liệu hoặc bị truy cập trái phép.

---

## 3.4.12. Luồng bảo mật tổng thể

Luồng truy cập người dùng:

```text
User → Route 53 → CloudFront → AWS WAF → S3 Static Website → Cognito → API Gateway → Lambda → DynamoDB
```

Luồng upload ảnh từ ESP32 Camera:

```text
ESP32 Camera → API Gateway → Lambda Presigned URL → Amazon S3 → Lambda Image Processing
```

Luồng gửi dữ liệu cảm biến:

```text
ESP32 Sensor → AWS IoT Core → IoT Rule → Lambda Sensor Processing → DynamoDB
```

Các lớp bảo mật chính:

| Lớp bảo mật | Dịch vụ sử dụng |
| :--- | :--- |
| Bảo vệ website | CloudFront, AWS WAF, HTTPS |
| Xác thực người dùng | Amazon Cognito |
| Bảo vệ API | API Gateway Authorizer |
| Phân quyền dịch vụ | IAM |
| Bảo mật upload ảnh | Presigned URL |
| Bảo mật thiết bị IoT | IoT Certificate và IoT Policy |
| Theo dõi lỗi bảo mật | CloudWatch Logs |

---

## 3.4.13. Kết luận

Phần giao diện và bảo mật giúp hệ thống Parking IoT có khả năng phục vụ người dùng một cách trực quan, an toàn và dễ quản lý. Giao diện Web/App được lưu trữ trên Amazon S3 và phân phối qua CloudFront, giúp người dùng truy cập nhanh chóng và ổn định.

Các dịch vụ như Amazon Cognito, AWS WAF, IAM, API Gateway Authorizer và Presigned URL giúp bảo vệ hệ thống khỏi truy cập trái phép, bảo vệ dữ liệu bãi xe và kiểm soát quyền truy cập giữa các thành phần. Với thiết kế này, hệ thống có thể vận hành an toàn, dễ mở rộng và phù hợp với mô hình AWS Serverless.