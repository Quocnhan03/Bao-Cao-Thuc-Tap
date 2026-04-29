---
title: "Dọn dẹp tài nguyên"
date :  "`r Sys.Date()`"
weight: 6
chapter : false
pre: " <b> 6. </b> "
---


Đây là bước bắt buộc để kết thúc quy trình vận hành, giúp tối ưu hóa chi phí AWS cho các dự án nghiên cứu.

- **6.1. Xóa hạ tầng bằng CDK:**  
  - Di chuyển vào thư mục dự án CDK  
  - Chạy lệnh:
    ```bash
    cdk destroy --all
    ```

- **6.2. Dọn dẹp tài nguyên thủ công:**  
  - Xóa các S3 buckets còn dữ liệu  
  - Xóa IAM Roles / Cognito nếu không dùng  

- **6.3. Kiểm tra chi phí:**  
  - Truy cập: https://console.aws.amazon.com/billing/  
  - Đảm bảo không còn tài nguyên đang chạy