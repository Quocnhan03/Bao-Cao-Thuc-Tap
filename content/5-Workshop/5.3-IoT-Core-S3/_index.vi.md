---
title: "AWS IoT Core & Amazon S3"
date: 2026-04-26
weight: 3
chapter: false
pre: " <b> 4.3. </b> "
---

# Thiết lập Giao tiếp Thiết bị & Lưu trữ Hình ảnh

Trong chương này, chúng ta bắt đầu xây dựng tầng vật lý của hệ thống đỗ xe thông minh bằng cách kết nối thiết bị với đám mây AWS và chuẩn bị kho lưu trữ ảnh biển số xe.

### Kiến trúc Tương tác

1. **AWS IoT Core**: Đóng vai trò là MQTT Broker trung tâm, chịu trách nhiệm nhận dữ liệu trạng thái chỗ đỗ xe từ các cảm biến siêu âm thông qua giao thức MQTT bảo mật, đồng thời quản lý các thông tin xác thực thiết bị biên thông qua chứng chỉ X.509.
2. **Amazon S3**: Lưu trữ hình ảnh chụp biển số xe từ camera. Để đảm bảo tính bảo mật và tối ưu tài nguyên thiết bị biên, hệ thống áp dụng cơ chế **Presigned URL** giúp camera gửi ảnh thẳng lên S3 mà không cần lưu trữ khóa truy cập AWS trên phần cứng.

---

### Nội dung chi tiết:

* **5.3.1.** [Cấu hình AWS IoT Core](5.3.1-iot-core-setup/)
* **5.3.2.** [Tạo S3 Bucket & Presigned URL](5.3.2-s3-presigned-url/)
