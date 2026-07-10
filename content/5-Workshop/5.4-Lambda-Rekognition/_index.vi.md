---
title: "Lambda & Amazon Rekognition"
date: 2026-04-26
weight: 4
chapter: false
pre: " <b> 4.4. </b> "
---

Chương này trình bày chi tiết về quá trình thiết kế, cấu hình và triển khai hệ thống xử lý dữ liệu tự động ở phía Backend của bãi đỗ xe thông minh. Kiến trúc này sử dụng mô hình lập trình hướng sự kiện (Event-Driven Architecture) nhằm liên kết các dịch vụ Serverless bao gồm **AWS Lambda**, **Amazon Rekognition** và **Amazon DynamoDB**.

#### Các nội dung chính được triển khai:

1. **[Lambda xử lý ảnh và kích hoạt sự kiện (5.4.1)](5.4.1-lambda-image-processing/)**: Thiết lập hàm Lambda nhận diện biển số xe tự động kích hoạt bởi sự kiện thêm ảnh trên S3.
2. **[Tích hợp Amazon Rekognition (5.4.2)](5.4.2-rekognition-integration/)**: Cấu hình kết nối API thị giác máy tính của AWS để nhận diện và trích xuất chữ viết từ ảnh thô mà không cần cài đặt máy chủ AI.
3. **[Thiết kế cơ sở dữ liệu DynamoDB (5.4.3)](5.4.3-dynamodb-setup/)**: Xây dựng cấu trúc lược đồ các bảng NoSQL để quản lý trạng thái chỗ đỗ xe, nhật ký phương tiện và các lệnh điều khiển cổng tự động.
4. **[Kiểm thử luồng nhận diện xe (5.4.4)](5.4.4-end-to-end-test/)**: Đánh giá và xác minh thực tế quá trình vận hành tự động của luồng xử lý nhận diện biển số xe từ lúc xe vào/ra cho đến khi ghi nhận thành công dữ liệu.
