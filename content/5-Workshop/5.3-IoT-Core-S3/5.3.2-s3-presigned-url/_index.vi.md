---
title: "Tạo S3 Bucket & Presigned URL"
date: 2026-04-26
weight: 2
chapter: false
pre: " <b> 4.3.2. </b> "
---

Để phục vụ lưu trữ hình ảnh chụp phương tiện phục vụ nhận diện biển số xe đầu vào và đầu ra, một hệ thống lưu trữ đối tượng tin cậy trên **Amazon S3** đã được thiết lập cùng cơ chế phân quyền bảo mật truy cập bằng **Presigned URL**.

---

### 1. Cấu trúc lưu trữ trên S3 Bucket
Hình ảnh biển số xe được tổ chức và lưu trữ tập trung tại một S3 Bucket được thiết lập ở trạng thái riêng tư (Private) hoàn toàn nhằm bảo mật dữ liệu cá nhân của người gửi xe:
- **Tên S3 Bucket đã tạo**: `smart-parking-images-075647413376-ap-southeast-1-an`
- **Phân loại cấu trúc thư mục**: Dữ liệu ảnh được phân loại bên trong thư mục chính là `parking/` và phân nhánh thành hai thư mục con:
  - `parking/in/`: Lưu trữ ảnh chụp phương tiện tại thời điểm đi vào bãi đỗ.
  - `parking/out/`: Lưu trữ ảnh chụp phương tiện tại thời điểm rời bãi đỗ.

![Cấu trúc S3 Bucket](/images/5-Workshop/5.3-IoT-Core-S3/5.3.2-create-bucket.png)
*Minh chứng 5.3.2.1: Các thư mục nhánh (in/out) lưu trữ hình ảnh xe được phân cấp rõ ràng trong Amazon S3*

---

### 2. Cấu hình chia sẻ tài nguyên nguồn gốc chéo (S3 CORS)
Do ứng dụng Web Dashboard Frontend và thiết bị biên (ESP32 Camera) gửi các yêu cầu tải ảnh trực tiếp (HTTP PUT) tới S3 Bucket từ các tên miền và nguồn khác nhau, chính sách **CORS (Cross-Origin Resource Sharing)** đã được cấu hình trên S3 Bucket để cho phép các luồng truyền nhận này mà không bị chặn bởi chính sách bảo mật của trình duyệt. 

Cấu hình chi tiết được thiết lập dưới dạng JSON như sau:

```json
[
  {
    "AllowedHeaders": [
      "*"
    ],
    "AllowedMethods": [
      "PUT",
      "POST",
      "GET"
    ],
    "AllowedOrigins": [
      "*"
    ],
    "ExposeHeaders": []
  }
]
```

![Cấu hình CORS S3](/images/5-Workshop/5.3-IoT-Core-S3/5.3.2-cors.png)
*Minh chứng 5.3.2.2: Chính sách CORS cấu hình trên S3 Bucket cho phép các phương thức PUT, POST, GET để tải lên và truy xuất ảnh*

---

### 3. Cơ chế hoạt động của S3 Presigned URL

#### Khái niệm giải pháp bảo mật
S3 Bucket chứa dữ liệu ảnh biển số xe được cấu hình chặn toàn bộ truy cập công khai (Block All Public Access) để ngăn ngừa rò rỉ dữ liệu. Thông thường, để tải ảnh lên S3, thiết bị biên cần sử dụng thông tin tài khoản AWS (Access Key & Secret Key), tuy nhiên việc lưu trữ các khóa này trên phần cứng thiết bị biên (ESP32) mang lại rủi ro bảo mật rất lớn.

Để giải quyết vấn đề này, cơ chế **S3 Presigned URL** được áp dụng. Đây là đường dẫn tải lên tạm thời có chữ ký số xác thực từ AWS IAM của hệ thống Serverless, cho phép thiết bị tải ảnh lên (PUT) hoặc người dùng xem ảnh (GET) trong một thời gian ngắn định trước (ví dụ: 5 phút) mà không cần truyền hay lưu trữ thông tin đăng nhập của tài khoản AWS trên thiết bị biên.

#### Luồng hoạt động của hệ thống:
{{< mermaid >}}
sequenceDiagram
    ESP32->>API Gateway: Yêu cầu upload ảnh (gửi kèm tên file ảnh)
    API Gateway->>Lambda: Kích hoạt Lambda sinh URL
    Lambda->>S3 Bucket: Gọi S3 SDK sinh Presigned URL dạng PUT
    S3 Bucket-->>Lambda: Trả về Presigned URL tạm thời (Hạn 5 phút)
    Lambda-->>API Gateway: Phản hồi Presigned URL
    API Gateway-->>ESP32: Gửi Presigned URL về cho thiết bị biên
    ESP32->>S3 Bucket: Upload trực tiếp file ảnh lên S3 qua Presigned URL
    S3 Bucket-->>ESP32: Phản hồi tải lên thành công (HTTP 200 OK)
{{< /mermaid >}}

Việc sinh các đường dẫn ký trước này được xử lý tự động thông qua hàm Lambda và API Gateway, sẽ được mô tả chi tiết ở các bài viết tiếp theo.
