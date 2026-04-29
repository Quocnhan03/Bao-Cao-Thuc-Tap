---
title : "Giám sát & Quản trị"
date :  "`r Sys.Date()`" 
weight : 5
chapter : false
pre : " <b> 3.5. </b> "
---


- **3.5.1. Giám sát:**  
  Cấu hình CloudWatch Log Groups cho các dịch vụ như Lambda và Glue nhằm thu thập và lưu trữ log hệ thống.  
  Thiết lập CloudWatch Dashboard để theo dõi hiệu năng, lỗi và trạng thái hoạt động của toàn hệ thống.

- **3.5.2. Cảnh báo:**  
  Thiết lập Amazon SNS để gửi thông báo qua Email hoặc SMS khi phát hiện sự cố hoặc khi các chỉ số vượt ngưỡng (ví dụ: lỗi Lambda, thất bại ETL, hoặc vượt ngân sách).