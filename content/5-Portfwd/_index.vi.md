---
title: "Kết nối từ xa an toàn"
date :  "`r Sys.Date()`"
weight: 5
chapter : false
pre: " <b> 5. </b> "
---


Kỹ thuật này cho phép quản trị viên truy cập an toàn vào các tài nguyên nội bộ (Private Subnet) mà không cần mở các cổng public ra Internet.

- **5.1. Giới thiệu AWS SSM Session Manager:**  
  Sử dụng tính năng Port Forwarding của AWS Systems Manager Session Manager để tạo một “đường hầm” kết nối an toàn, thay thế cho phương pháp SSH truyền thống.

- **5.2. Hướng dẫn thiết lập:**  
  - Cài đặt AWS CLI và Session Manager Plugin trên máy cá nhân.  
  - Sử dụng lệnh CLI sau:
    ```bash
    aws ssm start-session \
      --target <instance-id> \
      --document-name AWS-StartPortForwardingSession \
      --parameters '{"portNumber":["80"],"localPortNumber":["8080"]}'
    ```

- **5.3. Kiểm thử:**  
  Truy cập địa chỉ `http://localhost:8080` trên trình duyệt để xác nhận kết nối thành công tới dịch vụ bên trong VPC.