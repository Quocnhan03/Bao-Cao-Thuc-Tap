---
title: "Quản lý Session Logs"
date :  "`r Sys.Date()`"
weight: 4
chapter : false
pre: " <b> 4. </b> "
---

Phần này thiết lập cơ chế giám sát tập trung, cho phép truy vết mọi hành vi và sự cố trong hệ thống.  
Hệ thống sử dụng kết hợp Amazon S3, CloudWatch và Amazon SNS để lưu trữ, phân tích và cảnh báo log.


### Nội dung triển khai:

4.1. [Thiết lập S3 Bucket cho Logs (Long-term Archiving)](4.1-s3/) \
4.2. [Cấu hình CloudWatch Logs (CloudWatch Logs Configuration)](4.2-cloudwatch/) \
4.3. [Truy xuất Logs với Logs Insights (Log Analysis)](4.3-insights/) \
4.4. [Thiết lập Alert với Amazon SNS (Alert Setup)](4.4-alert/)