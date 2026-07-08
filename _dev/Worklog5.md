# Worklog Tuần 5: Triển Khai Chi Tiết Các Bài Lab AWS (26, 27, 30)

Báo cáo này tổng hợp chi tiết toàn bộ các bước thao tác (từng bước một) để triển khai 3 bài lab trong tuần 5, kèm theo hình ảnh minh chứng cụ thể cho từng thao tác nhỏ nhất trên AWS Console.

---

## 🛡️ Lab 26: Sử dụng AWS WAF (Web Application Firewall)

### 1. Chuẩn bị: Tạo S3 Bucket cho WAF Logs
Để lưu trữ Access Logs (nhật ký truy cập) mà WAF nhận được, ta cần tạo một S3 Bucket.
- Tên bucket bắt buộc phải bắt đầu bằng `aws-waf-logs-` theo quy định của AWS WAF.
- Tiến hành thiết lập các thông số cơ bản cho S3 Bucket.

![Bước thiết lập S3 Bucket](./static/images/WorklogT5/lab26-s3-create.png)

Kết quả tạo S3 Bucket thành công:
![S3 Bucket Created](./static/images/WorklogT5/lab26-s3-created.png)

### 2. Triển khai Web ACL
Chuyển sang dịch vụ AWS WAF, tiến hành tạo một Web ACL (Access Control List) mới.
- **Step 1:** Thiết lập thông tin chung cho Web ACL (Tên, CloudWatch metric name).
![WAF Step 1 - General Info](./static/images/WorklogT5/lab26-waf-step1.png)

- **Step 2:** Thêm tài nguyên AWS (Add AWS resources) cần bảo vệ vào Web ACL.
![WAF Step 2 - Add Resources](./static/images/WorklogT5/lab26-waf-step2-resources.png)

### 3. Cấu hình Rules (Các Quy Tắc Bảo Vệ)
Tiếp theo, ta cấu hình các **Managed Rules** (các rule được quản lý và cung cấp sẵn bởi AWS và các đối tác).
![WAF Managed Rules Vendor Selection](./static/images/WorklogT5/lab26-waf-managed-vendor.png)
![WAF Managed Rules Configuration](./static/images/WorklogT5/lab26-waf-managed-rules.png)

Cụ thể, bật bộ rule **Core rule set** (CRS) - đây là bộ rule cực kỳ quan trọng giúp chặn các dạng tấn công web phổ biến như được định nghĩa trong OWASP Top 10.
![WAF Core Rules Enable](./static/images/WorklogT5/lab26-waf-core-rule.png)

Sau khi thêm, rule sẽ xuất hiện trong danh sách Rules của Web ACL.
![WAF Rules Added](./static/images/WorklogT5/lab26-waf-rules-added.png)
![WAF Rules List](./static/images/WorklogT5/lab26-waf-rules.png)

### 4. Hoàn tất cấu hình và Kiểm tra Web ACL
Sau khi review toàn bộ cấu hình (bao gồm cả việc trỏ Logging về S3 Bucket), nhấn Create để hoàn tất quá trình tạo Web ACL.
![WAF Creation Success](./static/images/WorklogT5/lab26-waf-success.png)

Giao diện chi tiết của Web ACL vừa tạo, hiển thị lưu lượng truy cập và các rule đã cấu hình:
![WAF Detail View](./static/images/WorklogT5/lab26-waf-detail.png)

---

## 🏷️ Lab 27: Quản lý Tài nguyên với AWS Tags & Resource Groups

### 1. Tạo EC2 Instance và gắn Tag ngay lúc khởi tạo
Tags giúp phân loại và quản lý chi phí tài nguyên rất hiệu quả. Bước đầu tiên là tạo một EC2 Instance và gắn tag cho nó.
- Khởi tạo EC2 Instance (`t3.micro`).
![Launch EC2 UI](./static/images/WorklogT5/lab27-launch-ec2-page.png)
![Configuring EC2](./static/images/WorklogT5/lab27-ec2-top.png)

- Tại phần cấu hình Tag, tiến hành nhập 2 tag quan trọng:
  - `Name` : `WebServer`
  - `Environment` : `Production`
![EC2 Tags Config](./static/images/WorklogT5/lab27-ec2-tags.png)
![EC2 Tags Expanded](./static/images/WorklogT5/lab27-ec2-tags-expanded.png)

- Hoàn tất quá trình tạo Instance.
![Launch Success](./static/images/WorklogT5/lab27-launch-success.png)

Khi quay lại danh sách Instances, ta thấy các EC2 Instance đã được khởi chạy với các tag hiển thị đầy đủ trên bảng.
![Instances Running](./static/images/WorklogT5/lab27-instances-created.png)

### 2. Quản lý Tags (Thêm/Sửa/Xóa Tag sau khi tạo)
Trong thực tế, ta thường phải cập nhật Tag cho các tài nguyên đang chạy.
- Chọn tab **Tags** của Instance và bấm **Manage tags**.
![Manage Tags Overview](./static/images/WorklogT5/lab27-manage-tags.png)

- Tại màn hình Manage Tags, thêm một tag mới: `Dept` = `IT` và nhấn Save.
![Manage Tags Editing UI](./static/images/WorklogT5/lab27-manage-tags-ui.png)

- Kết quả: Tag mới đã được thêm thành công vào Instance.
![Tag Added Result](./static/images/WorklogT5/lab27-tag-added.png)

### 3. Lọc tài nguyên bằng Tag
Với số lượng lớn tài nguyên, ta có thể dùng Tag để tìm kiếm. 
- Tại thanh tìm kiếm, nhập cú pháp `tag:Environment=Production` để lọc ra đúng Instance thuộc môi trường Production.
![Filter EC2 by Tag](./static/images/WorklogT5/lab27-filter-by-tag.png)

### 4. Tạo Resource Group
Resource Groups giúp gom nhóm các tài nguyên có chung một bộ tag để dễ dàng thao tác hàng loạt.
- Chọn tạo nhóm dựa trên tag (Tag based), điều kiện: Loại tài nguyên là `AWS::EC2::Instance` và Tag là `Environment` = `Production`.
![Resource Group Config](./static/images/WorklogT5/lab27-resource-group.png)

- Kết quả tạo thành công nhóm **ProductionResourceGroup**.
![Resource Group Created](./static/images/WorklogT5/lab27-resource-group-created.png)

---

## 🔐 Lab 30: Quản lý IAM - Khởi Tạo Policy & User Giới Hạn

Tuân thủ nguyên tắc quyền tối thiểu (Least Privilege), lab này hướng dẫn cách tạo User bị giới hạn quyền truy cập thay vì cấp toàn quyền Admin.

### 1. Tạo IAM Policy Giới Hạn
Truy cập dịch vụ IAM > Policies. Chuyển sang JSON Editor để tạo một Policy giới hạn (ví dụ chỉ cho phép List/Describe tài nguyên EC2, không có quyền sửa đổi).
- Đặt tên Policy là **Lab30RestrictedPolicy**.
![Creating IAM Policy](./static/images/WorklogT5/lab30-iam-policy.png)

- Tạo Policy thành công.
![Policy Created Success](./static/images/WorklogT5/lab30-policy-created.png)

### 2. Tạo IAM User và Gán Quyền
- Truy cập IAM > Users và tạo một User mới tên là **Lab30RestrictedUser**.
- Kích hoạt quyền truy cập AWS Management Console (Console password).
- Tại bước phân quyền, gán Policy vừa tạo (hoặc policy tương đương tùy theo kịch bản) trực tiếp vào User.

- Kết quả tạo User thành công và có kèm theo đường dẫn đăng nhập.
![User Created Success](./static/images/WorklogT5/lab30-user-created.png)

---

## 🧹 Quy Trình Dọn Dẹp (Clean Up & Cost Optimization)

Do có các dịch vụ tính phí (như EC2, WAF, S3), toàn bộ tài nguyên đã được tiến hành **dọn dẹp triệt để** ngay sau khi ghi nhận đủ logs & hình ảnh minh chứng:
- **Xóa S3 Bucket**: Xóa sạch toàn bộ logs bên trong (Empty) và xóa luôn bucket `aws-waf-logs-demo-bucket`.
- **Hủy WAF Web ACL**: Gỡ liên kết và xóa Web ACL.
- **Terminate EC2**: Các Instances phục vụ cho Lab 27 đã được chuyển sang trạng thái *Shutting-down* / *Terminated*.
- **Xóa Resource Group & IAM**: Xóa nhóm ProductionResourceGroup, xóa IAM User và Policy để trả lại không gian quản lý tinh gọn nhất.
