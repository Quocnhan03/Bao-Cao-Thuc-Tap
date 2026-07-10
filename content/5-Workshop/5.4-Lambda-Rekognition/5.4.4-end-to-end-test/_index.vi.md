---
title: "Kiểm thử luồng nhận diện xe (End-to-End Test)"
date: 2026-04-26
weight: 4
chapter: false
pre: " <b> 4.4.4. </b> "
---

Để đánh giá tính chính xác và hiệu năng của hệ thống nhận diện tự động, quy trình kiểm thử toàn diện (End-to-End Test) đã được thực hiện bằng cách mô phỏng các lượt xe đi vào bãi đỗ (chiều IN) và đi ra khỏi bãi đỗ (chiều OUT), từ đó xác minh sự phối hợp hoạt động giữa các dịch vụ Amazon S3, AWS Lambda, Amazon Rekognition và Amazon DynamoDB.

---

### 1. Quy trình kiểm thử xe đi vào bãi đỗ (IN Flow Test)

#### 1.1. Hình ảnh phương tiện thực tế làm dữ liệu đầu vào (Input Image)
Ảnh chụp chiếc xe Mercedes màu đen tại cổng vào được sử dụng để kiểm thử khả năng nhận dạng chữ của hệ thống:

![Ảnh xe Mercedes kiểm thử](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-mercedes-car.jpg)
*Minh chứng 5.4.4.1: Hình ảnh xe Mercedes biển kiểm soát 30E-922.91 làm dữ liệu đầu vào cho luồng nhận diện*

#### 1.2. Quá trình tải ảnh lên Amazon S3 (Upload Image to S3)
Tệp tin hình ảnh xe Mercedes được tải lên S3 tại phân vùng thư mục cổng vào (`parking/in/`) để kích hoạt sự kiện xử lý:

![Tải ảnh vào S3 cổng vào](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-s3-upload.png)
*Minh chứng 5.4.4.2: Tệp tin ảnh mercedes.jpg được tải lên thành công thư mục s3://smart-parking-images-075647413376-ap-southeast-1-an/parking/in/*

#### 1.3. Bản ghi kết quả được tự động khởi tạo trên Amazon DynamoDB
Sau khi ảnh được đẩy lên S3, sự kiện tự động kích hoạt hàm Lambda xử lý. Bản ghi kết quả tại bảng `SmartParking_VehicleHistory` trên AWS Console ghi nhận chiều vào thành công:

![Kết quả kiểm thử trên DynamoDB chiều vào](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-dynamodb-record.png)
*Minh chứng 5.4.4.3: Bản ghi sự kiện xe 30E-922.91 đi vào bãi đỗ (IN) được tự động tạo thành công trong DynamoDB*

---

### 2. Quy trình kiểm thử xe đi ra khỏi bãi đỗ (OUT Flow Test)

#### 2.1. Tải ảnh lên thư mục S3 cổng ra (parking/out/) & Bản ghi kết quả trên DynamoDB
Tương tự luồng đi vào, để kiểm thử luồng xe ra, tệp tin ảnh xe Mercedes được tải lên phân vùng thư mục cổng ra (`parking/out/`). Sự kiện tự động kích hoạt hàm Lambda xử lý trích xuất biển số xe và ghi nhận sự kiện xe ra (OUT) vào cơ sở dữ liệu:

![Kiểm thử chiều xe ra](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-s3-dynamodb-out.png)
*Minh chứng 5.4.4.4: Upload ảnh mercedes.jpg lên cổng ra thành công (trên) và bản ghi sự kiện xe ra bãi (OUT) tương ứng được lưu trong DynamoDB (dưới)*

---

### 3. Phân tích kết quả thực tế
Dựa trên các minh chứng dữ liệu thu thập được từ cơ sở dữ liệu DynamoDB trong cả 2 trường hợp xe vào và xe ra:
- **Độ chính xác của OCR**: Amazon Rekognition đã phân tích ảnh chụp xe Mercedes và trích xuất thành công biển số xe dưới dạng chuỗi ký tự liền mạch là `30E92291` với độ tin cậy đạt mức cao.
- **Tự động phân loại luồng xe**:
  - **Khi xe vào (IN)**: Do tệp tin nằm ở thư mục `parking/in/`, thuộc tính `direction` được lưu là `IN` và trường `allow_open` được gán giá trị `true` để gửi tín hiệu mở cổng chắn tự động cho xe vào bãi đỗ.
  - **Khi xe ra (OUT)**: Do tệp tin nằm ở thư mục `parking/out/`, thuộc tính `direction` được lưu chính xác là `OUT` để ghi nhận sự kiện phương tiện rời bãi đỗ xe và tính toán thời gian gửi xe.
- **Định dạng hiển thị**: Thuật toán xử lý chuỗi trong Lambda đã định dạng lại chính xác từ chuỗi thô `30E92291` sang dạng hiển thị tiêu chuẩn có dấu gạch ngang và dấu chấm là `30E-922.91` (được lưu tại thuộc tính `display_plate_number`) để hiển thị trực quan lên ứng dụng khách.
- **Độ trễ xử lý (Latency)**: Toàn bộ quá trình từ khi tải ảnh lên S3 cho đến khi bản ghi xuất hiện trong DynamoDB chỉ mất dưới **1.5 giây**, đáp ứng tốt yêu cầu vận hành thời gian thực tại cổng kiểm soát.
