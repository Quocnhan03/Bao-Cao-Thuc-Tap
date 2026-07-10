---
title: "Workshop"
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

## HỆ THỐNG BÃI ĐỖ XE THÔNG MINH IOT — HƯỚNG DẪN TRIỂN KHAI CHI TIẾT

### Tổng quan

**Hệ thống Bãi đỗ xe thông minh IoT** (Smart Parking IoT System) là một giải pháp tự động hóa quản lý bãi đỗ xe toàn diện được xây dựng trên kiến trúc **AWS Serverless**. Hệ thống tích hợp các thiết bị IoT biên (ESP32 Camera và cảm biến siêu âm) để nhận diện phương tiện ra/vào, phát hiện trạng thái chỗ đỗ xe trống/đầy theo thời gian thực, tự động lưu trữ, xử lý dữ liệu và cung cấp giao diện quản trị web tích hợp chatbot AI.

Trong phần Workshop này, chúng ta sẽ đi qua chi tiết toàn bộ các bước triển khai từ đầu đến cuối — bao gồm cấu hình hạ tầng AWS, nạp code cho phần cứng, xây dựng giao diện người dùng và thiết lập giám sát.

### Mục lục

1. [Tổng quan Workshop](../5-workshop/1-overview/)
2. [Điều kiện tiên quyết](../5-workshop/2-prerequisites/)
3. [AWS IoT Core & Amazon S3](../5-workshop/3-iot-s3/)
   * [Cấu hình AWS IoT Core](../5-workshop/3-iot-s3/1-iot-core/)
   * [Tạo S3 Bucket & Presigned URL](../5-workshop/3-iot-s3/2-s3/)
4. [Lambda & Amazon Rekognition](../5-workshop/4-lambda-rekognition/)
   * [Xử lý ảnh bằng Lambda](../5-workshop/4-lambda-rekognition/1-lambda-image/)
   * [Tích hợp Amazon Rekognition](../5-workshop/4-lambda-rekognition/2-rekognition/)
   * [Thiết kế bảng DynamoDB](../5-workshop/4-lambda-rekognition/3-dynamodb/)
   * [Kiểm thử nhận diện End-to-End](../5-workshop/4-lambda-rekognition/4-end-to-end/)
5. [API Gateway, Cognito & Bedrock](../5-workshop/5-api-cognito-bedrock/)
6. [Cài đặt phần cứng ESP32](../5-workshop/6-esp32/)
7. [Web Dashboard](../5-workshop/7-dashboard/)
8. [Giám sát với CloudWatch](../5-workshop/8-monitoring/)
9. [Dọn dẹp tài nguyên](../5-workshop/9-cleanup/)
