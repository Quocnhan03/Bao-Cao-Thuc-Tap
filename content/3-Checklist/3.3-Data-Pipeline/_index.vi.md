---
title : "Đường ống dữ liệu"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 3.3. </b> "
---

-  **3.3.1. Lưu trữ dữ liệu thô:** 
    - Tạo S3 Bucket làm "Data Lake" và thiết lập IoT Rule để tự động lưu thông điệp MQTT vào S3.

-  **3.3.2. Quy trình xử lý tự động (ETL):**
    - Cấu hình Lambda trigger khi có dữ liệu mới.
    - Sử dụng Glue Crawler đọc cấu trúc và Glue ETL Jobs chuẩn hóa định dạng (Parquet).

-  **3.3.3. Lưu trữ dữ liệu phân tích:** 
    - Tạo S3 Bucket dành riêng cho dữ liệu đã làm sạch.