---
title: "Tuần 3"
date: 2026-05-04
weight: 3
pre : " <b> 1.3. </b> "
---

# NHẬT KÝ CÔNG VIỆC - TUẦN 3

**Thời gian:** 04/05/2026 - 10/05/2026  
**Chuyên ngành:** Mạng máy tính  
**Nhóm:** First Cloud Journey

---

## 1. Mục tiêu tuần
* Triển khai AWS CloudWatch để giám sát tài nguyên, quản lý logs và thiết lập cảnh báo tự động (Lab 8).
* Xây dựng Microsoft AD và cấu hình Route 53 DNS để kết nối an toàn qua RD Gateway (Lab 10).
* Thực hành sử dụng AWS CLI để quản lý các dịch vụ S3, SNS, IAM, VPC và khởi tạo EC2 (Lab 11).

## 2. Công việc & Lịch trình
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| :--- | :--- | :--- | :--- | :--- |
| Thứ 2 | Tìm hiểu về AWS CloudWatch (Metrics, Logs, Alarms) | 04/05/2026 | 04/05/2026 | [AWS Study Group - Lab 08](https://000008.awsstudygroup.com/) |
| Thứ 3 | Thực hành Lab 8: Giám sát tài nguyên với CloudWatch | 05/05/2026 | 05/05/2026 | [AWS Study Group - Lab 08](https://000008.awsstudygroup.com/) |
| Thứ 4 | Chuẩn bị Lab 10: Khởi tạo CloudFormation cho RDGW | 06/05/2026 | 06/05/2026 | [AWS Study Group - Lab 10](https://000010.awsstudygroup.com/) |
| Thứ 5 | Thực hành Lab 10: Triển khai Microsoft AD & Thiết lập DNS | 07/05/2026 | 07/05/2026 | [AWS Study Group - Lab 10](https://000010.awsstudygroup.com/) |
| Thứ 6 | Tìm hiểu AWS CLI và thực hành quản lý S3, SNS, IAM, VPC (Lab 11) | 08/05/2026 | 08/05/2026 | [AWS Study Group - Lab 11](https://000011.awsstudygroup.com/) |
| Thứ 7 | Thực hành Lab 11: Khởi tạo EC2 bằng CLI và Xử lý sự cố | 09/05/2026 | 09/05/2026 | [AWS Study Group - Lab 11](https://000011.awsstudygroup.com/) |
| Chủ Nhật | Tổng kết, dọn dẹp tài nguyên và hoàn thiện Document Tuần 3 | 10/05/2026 | 10/05/2026 | Nội bộ |

## 3. Kết quả đạt được

### 3.1. Lab 8 - Giám sát hệ thống với Amazon CloudWatch
* Xem và phân tích các chỉ số tài nguyên qua CloudWatch Metrics.
* Tìm kiếm, phân tích log sự kiện với CloudWatch Logs.
* Thiết lập CloudWatch Alarms để cảnh báo khi tài nguyên vượt ngưỡng.
* Xây dựng CloudWatch Dashboards để theo dõi trực quan các metrics quan trọng.

### 3.2. Lab 10 - Xây dựng Active Directory và kết nối RD Gateway
* Khởi tạo CloudFormation template để xây dựng hạ tầng cơ bản.
* Triển khai thành công AWS Managed Microsoft AD (Directory Service).
* Thiết lập các Endpoints và Resolver Rules trên Route 53 để phân giải DNS nội bộ.

### 3.3. Lab 11 - Quản lý tài nguyên qua AWS CLI
* Cài đặt và cấu hình thành công AWS CLI trên môi trường local/CloudShell.
* Thực hiện thành công các lệnh tương tác với Amazon S3, SNS, IAM, và VPC.
* Khởi tạo máy chủ EC2 hoàn toàn bằng lệnh thông qua AWS CLI.

> **Ghi chú:** Các tài nguyên thực hành Lab 8, 10, 11 sẽ được dọn dẹp sạch sẽ sau khi hoàn thành để tránh phát sinh chi phí.

{{% expand "Lab 08: Giám sát hệ thống với Amazon CloudWatch" %}}

## 1. Các chỉ số CloudWatch (CloudWatch Metrics)
![Xem chỉ số](/images/WorklogT3/lab08-31-viewing-metrics.png)
![Biểu thức tìm kiếm](/images/WorklogT3/lab08-32-search-expressions.png)

## 2. Nhật ký CloudWatch (CloudWatch Logs)
![Nhật ký CloudWatch](/images/WorklogT3/lab08-41-cloudwatch-logs.png)

## 3. Cảnh báo CloudWatch (CloudWatch Alarms)
![Cảnh báo CloudWatch](/images/WorklogT3/lab08-5-cloudwatch-alarms.png)

## 4. Bảng điều khiển CloudWatch (CloudWatch Dashboards)
![Bảng điều khiển CloudWatch](/images/WorklogT3/lab08-6-cloudwatch-dashboards.png)
{{% /expand %}}

{{% expand "Lab 10: Active Directory và kết nối RD Gateway" %}}

## 1. Chuẩn bị
![Tạo Key Pair](/images/WorklogT3/lab10-21-generate-key-pair.png)
![Tải lên Template](/images/WorklogT3/lab10-22-initialize-cloudformation-template-upload.png)
![Xem lại](/images/WorklogT3/lab10-22-initialize-cloudformation-template-review.png)
![Đang tiến hành](/images/WorklogT3/lab10-22-initialize-cloudformation-template-inprogress.png)
![Cấu hình Security Group](/images/WorklogT3/lab10-23-configuring-security-group.png)

## 2. Kết nối tới RDGW
![Kết nối tới RDGW](/images/WorklogT3/lab10-3-connecting-to-rdgw.png)

## 3. Triển khai Microsoft AD
![Triển khai AD](/images/WorklogT3/lab10-4-microsoft-ad-deployment.png)

## 4. Cài đặt DNS
![Outbound Endpoint](/images/WorklogT3/lab10-51-create-route-53-outbound-endpoint.png)
![Resolver Rules](/images/WorklogT3/lab10-52-create-route-53-resolver-rules.png)
![Inbound Endpoints](/images/WorklogT3/lab10-53-create-route-53-inbound-endpoints.png)
![Kết quả kiểm tra](/images/WorklogT3/lab10-54-test-results.png)
{{% /expand %}}

{{% expand "Lab 11: Quản lý tài nguyên qua AWS CLI" %}}

## 1. Xem tài nguyên qua CLI
![Xem tài nguyên](/images/WorklogT3/lab11-04-view-resource-cli.png)

## 2. AWS CLI với Amazon S3
![Kết quả S3](/images/WorklogT3/lab11-05-aws-cli-with-s3.png)

## 3. AWS CLI với Amazon SNS
![Kết quả SNS](/images/WorklogT3/lab11-06-aws-cli-with-sns.png)

## 4. AWS CLI với IAM
![Kết quả IAM](/images/WorklogT3/lab11-07-aws-cli-with-iam.png)

## 5. AWS CLI với VPC
![Kết quả VPC](/images/WorklogT3/lab11-08-aws-cli-with-vpc.png)
![Kết quả IGW](/images/WorklogT3/lab11-082-aws-cli-with-internet-gateway.png)

## 6. Tạo EC2 bằng AWS CLI
![Kết quả tạo EC2](/images/WorklogT3/lab11-09-creating-ec2-using-aws-cli.png)
{{% /expand %}}
