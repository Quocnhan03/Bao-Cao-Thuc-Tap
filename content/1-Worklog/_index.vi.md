---
title: "Nhật ký công việc"
date: 2026-04-27
weight: 1
pre : " <b> 1. </b> "
---


**Thông tin sinh viên:** Phạm Quốc Nhân  
**Chuyên ngành:** Mạng máy tính  
**Team:** First Cloud Journey

---

### Tuần 1: Thực hành IAM, VPC/VPN & EC2 Web Applications
* **Nội dung:** Hoàn thành Lab 02 (IAM), Lab 03 (VPC & Site-to-Site VPN) và Lab 04 (EC2 & Web Applications & Cost Governance).
* **Công việc đã làm:**
    * **Lab 02 (IAM):** Thiết lập IAM Group, User, Policy, Role, thực hành Switch Role an toàn cho OperatorUser và dọn dẹp tài nguyên.
    * **Lab 03 (VPC/VPN):** Xây dựng VPC, Subnets, Route Table, IGW, NAT Gateway, kiểm thử với Session Manager, CloudWatch, và thiết lập VPN Connection dùng Strongswan với Transit Gateway.
    * **Lab 04 (EC2 & Apps):** Khởi tạo EC2 Windows/Linux, cấu hình AMI/Snapshot, triển khai Web App quản lý người dùng (LAMP, Node.js), và thiết lập các chính sách quản lý chi phí & bảo mật nâng cao qua IAM.

### Tuần 2: Quản trị hệ thống với AWS Systems Manager (SSM)
* **Nội dung:** Tối ưu hóa việc truy cập Instance an toàn.
* **Công việc đã làm:**
    * Triển khai **Session Manager** thay thế cho SSH truyền thống (bảo mật port 22).
    * Cấu hình IAM Role cho EC2 để cấp quyền cho SSM Agent.
    * Thiết lập quản lý log tập trung với CloudWatch.

### Tuần 3: Giám sát, Xây dựng Template và Quản trị Danh tính
* **Nội dung:** Tìm hiểu và thực hành giám sát hệ thống, tự động hóa và quản trị phân quyền.
* **Công việc đã làm:**
    * **Lab 08 (CloudWatch):** Thiết lập Dashboards, Metrics, Logs và Alarms để giám sát EC2.
    * **Lab 10 (CloudFormation & AD):** Khởi tạo hạ tầng tự động bằng CloudFormation, thiết lập AWS Managed Microsoft AD và Route 53 Resolver.
    * **Lab 11 (AWS CLI):** Quản lý tài nguyên, thao tác EC2, S3 và IAM thông qua AWS CLI.

### Tuần 4: Quản lý Tổ chức, Lưu trữ và Sao lưu (Backup)
* **Nội dung:** Mở rộng và bảo mật hạ tầng đa tài khoản, quản lý dữ liệu an toàn.
* **Công việc đã làm:**
    * **Lab 12 (Organizations & Identity Center):** Xây dựng cấu trúc AWS Organizations, phân quyền SSO bằng IAM Identity Center.
    * **Lab 13 (AWS Backup):** Khởi tạo Backup Plan, Backup Vault tự động hóa sao lưu EC2.
    * **Lab 24 (Storage Gateway):** Thiết lập kết nối hybrid storage, đồng bộ dữ liệu lên S3.

### Tuần 5: Bảo mật Web, Quản lý Tài nguyên & Phân quyền Tối thiểu
* **Nội dung:** Triển khai WAF, Resource Groups và thiết lập IAM Restrictive Policy.
* **Công việc đã làm:**
    * **Lab 26 (AWS WAF):** Tạo Web ACL với các Managed Rules bảo vệ ứng dụng, lưu Access Logs trên S3.
    * **Lab 27 (Tags & Resource Groups):** Gắn tag và lọc tài nguyên EC2, quản lý bằng Resource Groups.
    * **Lab 30 (IAM):** Thiết kế JSON Policy giới hạn đặc quyền (Least Privilege) và gán cho User/Group.

---

> **Ghi chú:** Nhật ký này sẽ được cập nhật liên tục theo tiến độ thực tập thực tế của dự án.