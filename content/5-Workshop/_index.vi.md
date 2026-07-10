---
title: "Workshop"
date: 2026-04-26
weight: 4
chapter: false
pre: " <b> 4. </b> "
---

# Hệ thống Parking IoT thông minh — Hướng dẫn triển khai chi tiết

#### Tổng quan

**Hệ thống Parking IoT thông minh** là giải pháp tự động hóa quản lý bãi đỗ xe toàn diện được xây dựng trên kiến trúc **AWS Serverless**. Hệ thống kết hợp thiết bị IoT biên (ESP32 Camera và cảm biến siêu âm) để nhận diện phương tiện ra/vào bãi đỗ, phát hiện trạng thái trống/đầy của các vị trí đỗ xe theo thời gian thực, lưu trữ và xử lý dữ liệu tự động, đồng thời cung cấp giao diện dashboard web và chatbot hỗ trợ AI.

Nội dung phần này trình bày chi tiết quá trình thiết kế, cấu hình và triển khai thực tế của toàn bộ hệ thống từ đầu đến cuối — bao gồm thiết lập hạ tầng dịch vụ AWS, lập trình nạp code cho thiết bị phần cứng, xây dựng giao diện người dùng và cấu hình giám sát vận hành.

#### Nội dung

1. [Tổng quan về workshop](5.1-workshop-overview/)
2. [Chuẩn bị môi trường](5.2-prerequisite/)
3. [AWS IoT Core & Amazon S3](5.3-iot-core-s3/)
   * 3.1. [Cấu hình AWS IoT Core](5.3-iot-core-s3/5.3.1-iot-core-setup/)
   * 3.2. [Tạo S3 Bucket & Presigned URL](5.3-iot-core-s3/5.3.2-s3-presigned-url/)
4. [Lambda & Amazon Rekognition](5.4-lambda-rekognition/)
   * 4.1. [Lambda xử lý ảnh](5.4-lambda-rekognition/5.4.1-lambda-image-processing/)
   * 4.2. [Tích hợp Amazon Rekognition](5.4-lambda-rekognition/5.4.2-rekognition-integration/)
   * 4.3. [Thiết kế DynamoDB Tables](5.4-lambda-rekognition/5.4.3-dynamodb-setup/)
   * 4.4. [Kiểm thử luồng nhận diện](5.4-lambda-rekognition/5.4.4-end-to-end-test/)
5. [API Gateway, Cognito & Bedrock](5.5-api-cognito-bedrock/)
6. [Phần cứng ESP32](5.6-hardware-esp32/)
7. [Web Dashboard](5.7-web-dashboard/)
8. [Giám sát với CloudWatch](5.8-monitoring-cloudwatch/)
9. [Dọn dẹp tài nguyên](5.9-cleanup/)
