---
title : "Hạ tầng cốt lõi (AWS CDK)"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 3.1 </b> "
---


-  **3.1.1. Khởi tạo AWS CDK Project:** 
     -  Cấu hình môi trường phát triển (TypeScript/Python), cài đặt các thư viện cần thiết.

-  **3.1.2. Thiết lập VPC & Mạng:** 
     - Cấu hình VPC, Subnets (Public/Private), Internet Gateway.
     - Tạo Security Groups kiểm soát luồng truy cập cho Lambda và các dịch vụ nội bộ.

-  **3.1.3. Cấu hình IAM Roles & Policies:** 
     -  Thiết lập cơ chế "Least Privilege" (quyền tối thiểu) cho từng dịch vụ.