---
title: "Đề Xuất Dự Án"
date: 2026-04-27
weight: 2
pre : " <b> 2. </b> "
---

# ĐỀ XUẤT DỰ ÁN: Hệ thống Parking IoT thông minh

**Giải pháp AWS Serverless cho giám sát bãi đỗ xe, nhận diện biển số và hỗ trợ AI**

## 1. Tóm tắt điều hành

Dự án nhằm xây dựng hệ thống **Parking IoT thông minh** giúp tự động hóa quá trình giám sát bãi đỗ xe, nhận diện phương tiện và quản lý dữ liệu theo thời gian thực. Hệ thống sử dụng các thiết bị IoT như **ESP32 Camera** và **ESP32 cảm biến** để thu thập hình ảnh xe ra/vào, trạng thái vị trí đỗ và dữ liệu từ bãi xe.

Dữ liệu từ thiết bị được gửi lên AWS thông qua các dịch vụ như **AWS IoT Core**, **Amazon S3**, **Amazon API Gateway** và được xử lý bằng **AWS Lambda**. Hình ảnh phương tiện được lưu trữ trong Amazon S3, sau đó kích hoạt Lambda để xử lý ảnh và gọi **Amazon Rekognition** nhằm nhận diện biển số xe. Kết quả nhận diện và dữ liệu cảm biến được lưu vào **Amazon DynamoDB** để phục vụ việc tra cứu, quản lý và hiển thị trên Web/App.

Ngoài ra, hệ thống còn tích hợp **Amazon Bedrock** thông qua lớp **Lambda AI Service** để hỗ trợ phân tích dữ liệu, trả lời các truy vấn thông minh và cung cấp trải nghiệm quản lý bãi đỗ xe hiện đại hơn. Với kiến trúc AWS Serverless, hệ thống có khả năng mở rộng linh hoạt, giảm chi phí vận hành và không cần quản lý máy chủ truyền thống.

---

## 2. Tuyên bố vấn đề

### 2.1. Thách thức hiện tại

Các bãi đỗ xe truyền thống thường gặp nhiều hạn chế trong quá trình vận hành và quản lý. Việc kiểm soát xe ra/vào còn phụ thuộc nhiều vào con người, dễ xảy ra sai sót khi ghi nhận biển số, thời gian vào bãi hoặc trạng thái chỗ đỗ. Khi số lượng phương tiện tăng lên, việc quản lý thủ công sẽ trở nên khó khăn, thiếu tính chính xác và mất nhiều thời gian.

Một số vấn đề chính có thể kể đến như:

* Khó kiểm tra nhanh tình trạng còn trống hoặc đã đầy của từng vị trí đỗ xe.
* Việc ghi nhận xe ra/vào còn thủ công, dễ nhầm lẫn biển số hoặc thời gian.
* Dữ liệu hình ảnh, biển số và trạng thái bãi xe chưa được quản lý tập trung.
* Người quản lý khó theo dõi lịch sử hoạt động của phương tiện.
* Khó mở rộng hệ thống khi số lượng camera, cảm biến hoặc vị trí đỗ tăng lên.
* Việc xây dựng hệ thống riêng có thể tốn chi phí nếu phải đầu tư máy chủ vật lý.

### 2.2. Giải pháp đề xuất

Dự án đề xuất xây dựng hệ thống **Parking IoT thông minh trên nền tảng AWS Serverless**. Hệ thống sử dụng ESP32 Camera để chụp ảnh xe ra/vào, ESP32 cảm biến để ghi nhận trạng thái chỗ đỗ, sau đó gửi dữ liệu lên AWS để xử lý và lưu trữ tập trung.

Giải pháp bao gồm các chức năng chính:

* ESP32 Camera chụp ảnh phương tiện khi xe ra hoặc vào bãi.
* ESP32 cảm biến phát hiện trạng thái từng vị trí đỗ xe.
* Ảnh xe được tải lên Amazon S3 thông qua Presigned URL.
* AWS Lambda xử lý sự kiện khi có ảnh mới được upload lên S3.
* Amazon Rekognition phân tích hình ảnh và hỗ trợ nhận diện biển số xe.
* DynamoDB lưu thông tin xe, biển số, thời gian, trạng thái và dữ liệu cảm biến.
* Web/App cho người dùng truy cập, đăng nhập, xem trạng thái bãi xe và lịch sử xe ra/vào.
* Amazon Cognito hỗ trợ xác thực và phân quyền người dùng.
* Amazon Bedrock hỗ trợ lớp AI để phân tích dữ liệu và trả lời câu hỏi thông minh.
* Amazon CloudWatch giám sát log, lỗi và trạng thái hoạt động của hệ thống.

### 2.3. Hiệu quả kỳ vọng

Hệ thống giúp giảm thao tác thủ công, tăng độ chính xác trong quản lý bãi xe, hỗ trợ giám sát theo thời gian thực và tạo nền tảng dữ liệu phục vụ phân tích AI trong tương lai. Nhờ sử dụng kiến trúc Serverless, hệ thống có thể mở rộng linh hoạt theo số lượng thiết bị, số lượng xe và nhu cầu sử dụng thực tế.

---

## 3. Kiến trúc giải pháp

Hệ thống áp dụng kiến trúc **AWS Serverless** nhằm giảm chi phí quản lý hạ tầng, tăng khả năng mở rộng và dễ dàng tích hợp với các dịch vụ AI, IoT và cơ sở dữ liệu trên AWS.

![Sơ đồ kiến trúc Parking IoT](/images/2-proposal-architecture.png)

### 3.1. Các dịch vụ AWS chủ chốt

#### Giao diện người dùng

* **Amazon Route 53:** Quản lý tên miền cho hệ thống.
* **Amazon CloudFront:** Phân phối nội dung website với tốc độ cao.
* **AWS WAF:** Bảo vệ website khỏi các truy cập độc hại.
* **Amazon S3 Static Website:** Lưu trữ giao diện Web/App tĩnh.

#### Xác thực và phân quyền

* **Amazon Cognito:** Quản lý đăng nhập, xác thực người dùng và phân quyền truy cập.
* **IAM:** Quản lý quyền truy cập giữa các dịch vụ AWS.

#### API và xử lý backend

* **Amazon API Gateway:** Nhận request từ Web/App hoặc thiết bị.
* **AWS Lambda API Backend:** Xử lý nghiệp vụ chính của hệ thống.
* **AWS Lambda xử lý ảnh:** Xử lý ảnh sau khi được tải lên S3.
* **AWS Lambda xử lý dữ liệu cảm biến:** Xử lý dữ liệu gửi từ ESP32 cảm biến.
* **AWS Lambda AI Service:** Kết nối với Amazon Bedrock để xử lý các chức năng AI.

#### IoT và thiết bị biên

* **ESP32 Camera:** Chụp ảnh xe ra/vào.
* **ESP32 cảm biến:** Gửi trạng thái chỗ đỗ xe.
* **AWS IoT Core:** Nhận dữ liệu từ thiết bị IoT thông qua giao thức MQTT.

#### Lưu trữ và cơ sở dữ liệu

* **Amazon S3:** Lưu trữ hình ảnh xe.
* **Amazon DynamoDB:** Lưu dữ liệu biển số, lịch sử xe ra/vào, trạng thái chỗ đỗ và thông tin người dùng.

#### Xử lý ảnh và AI

* **Amazon Rekognition:** Phân tích hình ảnh, hỗ trợ nhận diện biển số xe.
* **Amazon Bedrock:** Hỗ trợ phân tích dữ liệu và trả lời truy vấn thông minh bằng AI.

#### Giám sát hệ thống

* **Amazon CloudWatch:** Ghi log, theo dõi lỗi, giám sát Lambda, API Gateway, IoT Core và các thành phần liên quan.

---

## 4. Luồng hoạt động của hệ thống

### 4.1. Luồng người dùng truy cập Web/App

Người dùng truy cập hệ thống thông qua trình duyệt web hoặc thiết bị di động. Website được lưu trữ trên Amazon S3 Static Website và phân phối thông qua Amazon CloudFront. Route 53 đảm nhiệm vai trò quản lý tên miền, còn AWS WAF giúp bảo vệ hệ thống khỏi các truy cập không hợp lệ.

**Luồng xử lý:**

Người dùng → Route 53 → CloudFront → AWS WAF → Amazon S3 Static Website → API Gateway → Lambda Backend → DynamoDB

Trong đó:

* Người dùng truy cập vào tên miền của hệ thống.
* Route 53 điều hướng request đến CloudFront.
* CloudFront phân phối giao diện website từ Amazon S3.
* AWS WAF kiểm tra và chặn các request độc hại.
* Web/App gọi API Gateway để lấy dữ liệu.
* Lambda Backend xử lý request và truy vấn DynamoDB.
* DynamoDB trả dữ liệu về cho Web/App để hiển thị.

---

### 4.2. Luồng xác thực người dùng

Hệ thống sử dụng Amazon Cognito để xác thực người dùng trước khi cho phép truy cập vào các chức năng quản lý. Người dùng có thể đăng nhập bằng tài khoản đã được cấp. Sau khi đăng nhập thành công, Cognito cấp token để Web/App gửi kèm trong các request đến API Gateway.

**Luồng xử lý:**

Người dùng → Amazon Cognito → API Gateway → Lambda Backend → DynamoDB

Trong đó:

* Người dùng nhập tài khoản và mật khẩu trên Web/App.
* Amazon Cognito xác thực thông tin đăng nhập.
* Nếu đăng nhập thành công, Cognito trả về token.
* Web/App gửi token trong request đến API Gateway.
* API Gateway sử dụng Cognito Authorizer để kiểm tra quyền truy cập.
* Lambda Backend xử lý chức năng tương ứng nếu người dùng hợp lệ.

---

### 4.3. Luồng ESP32 Camera gửi ảnh xe

Khi có xe đi vào hoặc đi ra bãi đỗ, ESP32 Camera sẽ chụp ảnh phương tiện. Thay vì upload ảnh trực tiếp qua Lambda, thiết bị sẽ xin **Presigned URL** từ API Gateway. Sau đó ESP32 Camera dùng URL này để upload ảnh JPEG trực tiếp lên Amazon S3.

Cách làm này giúp giảm tải cho Lambda, tăng hiệu quả upload ảnh và phù hợp với kiến trúc AWS.

**Luồng xử lý:**

ESP32 Camera → API Gateway → Lambda Backend → Presigned URL → ESP32 Camera upload ảnh lên S3 → S3 Trigger Lambda → Amazon Rekognition → DynamoDB

Các bước chi tiết:

1. ESP32 Camera phát hiện xe hoặc được kích hoạt để chụp ảnh.
2. ESP32 Camera gửi request đến API Gateway để xin Presigned URL.
3. API Gateway chuyển request đến Lambda Backend.
4. Lambda Backend tạo Presigned URL cho phép upload ảnh lên Amazon S3.
5. ESP32 Camera nhận Presigned URL.
6. ESP32 Camera upload ảnh JPEG trực tiếp lên Amazon S3.
7. Khi ảnh mới được upload, S3 phát sinh sự kiện ObjectCreated.
8. S3 Trigger kích hoạt Lambda xử lý ảnh.
9. Lambda gọi Amazon Rekognition để phân tích hình ảnh.
10. Kết quả nhận diện biển số được lưu vào DynamoDB.

Ví dụ dữ liệu ảnh được lưu:

```json
{
  "image_id": "car_001.jpg",
  "plate_number": "51A-12345",
  "direction": "in",
  "timestamp": "2026-04-27T10:30:00",
  "s3_url": "s3://parking-image-bucket/car_001.jpg"
}
```

---

### 4.4. Luồng ESP32 cảm biến gửi dữ liệu vị trí đỗ

ESP32 cảm biến được dùng để phát hiện trạng thái của từng vị trí đỗ xe. Cảm biến có thể là cảm biến siêu âm, hồng ngoại hoặc cảm biến từ, tùy theo thiết kế thực tế. Dữ liệu cảm biến được gửi lên AWS IoT Core bằng giao thức MQTT.

**Luồng xử lý:**

ESP32 cảm biến → AWS IoT Core → Lambda xử lý dữ liệu cảm biến → DynamoDB

Các bước chi tiết:

1. ESP32 cảm biến đọc trạng thái vị trí đỗ.
2. Thiết bị gửi dữ liệu lên AWS IoT Core bằng MQTT.
3. AWS IoT Core nhận dữ liệu từ thiết bị.
4. IoT Rule chuyển dữ liệu đến Lambda xử lý dữ liệu cảm biến.
5. Lambda kiểm tra, chuẩn hóa và lưu dữ liệu vào DynamoDB.
6. Web/App truy vấn DynamoDB để hiển thị trạng thái bãi xe theo thời gian thực.

Ví dụ dữ liệu cảm biến:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

Trong đó:

* `slot_id`: Mã vị trí đỗ xe.
* `status`: Trạng thái vị trí đỗ, ví dụ `available` hoặc `occupied`.
* `timestamp`: Thời gian ghi nhận dữ liệu.

---

### 4.5. Luồng xử lý AI Service

Hệ thống tích hợp lớp AI để hỗ trợ người dùng và quản trị viên truy vấn dữ liệu bãi đỗ xe bằng ngôn ngữ tự nhiên. Web/App gửi câu hỏi đến API Gateway, sau đó Lambda AI Service xử lý yêu cầu, lấy dữ liệu từ DynamoDB nếu cần và gọi Amazon Bedrock để tạo phản hồi.

**Luồng xử lý:**

Web/App → API Gateway → Lambda AI Service → Amazon Bedrock → DynamoDB → Web/App

Các chức năng AI có thể hỗ trợ:

* Hỏi số lượng chỗ trống hiện tại.
* Tóm tắt số lượng xe đang có trong bãi.
* Phân tích khung giờ bãi xe đông nhất.
* Gợi ý khu vực còn chỗ trống.
* Hỗ trợ quản trị viên tra cứu lịch sử xe ra/vào.
* Tóm tắt tình trạng hoạt động của bãi xe trong ngày.

Ví dụ câu hỏi:

> Hiện tại còn bao nhiêu chỗ trống trong bãi xe?

Ví dụ phản hồi:

> Hiện tại bãi xe còn 12 chỗ trống, trong đó khu A còn 5 chỗ và khu B còn 7 chỗ.

---

### 4.6. Luồng giám sát hệ thống

Amazon CloudWatch được sử dụng để ghi log và giám sát hoạt động của các dịch vụ trong hệ thống. CloudWatch có thể nhận log từ Lambda, API Gateway, IoT Core và các thành phần xử lý dữ liệu.

**Luồng giám sát:**

API Gateway / Lambda / IoT Core / Rekognition / DynamoDB → CloudWatch

CloudWatch giúp:

* Theo dõi lỗi khi Lambda xử lý thất bại.
* Kiểm tra request đến API Gateway.
* Theo dõi dữ liệu từ thiết bị IoT.
* Ghi nhận log xử lý ảnh và dữ liệu cảm biến.
* Hỗ trợ phát hiện sự cố trong quá trình vận hành.

---

## 5. Triển khai kỹ thuật

### 5.1. Giai đoạn 1: Phân tích và thiết kế hệ thống

Trong giai đoạn đầu, nhóm thực hiện khảo sát yêu cầu hệ thống và xác định phạm vi triển khai. Các công việc chính bao gồm:

* Xác định số lượng cổng ra/vào cần lắp ESP32 Camera.
* Xác định số lượng vị trí đỗ cần theo dõi bằng cảm biến.
* Thiết kế sơ đồ kiến trúc hệ thống.
* Thiết kế luồng dữ liệu giữa thiết bị IoT và AWS.
* Thiết kế cấu trúc bảng DynamoDB.
* Xác định quyền truy cập cho người dùng, quản lý và quản trị viên.

### 5.2. Giai đoạn 2: Triển khai thiết bị IoT

Giai đoạn này tập trung vào việc cấu hình và kiểm thử thiết bị ESP32.

Các công việc chính:

* Cấu hình ESP32 Camera để chụp ảnh phương tiện.
* Cấu hình ESP32 cảm biến để đọc trạng thái vị trí đỗ.
* Kết nối ESP32 cảm biến với AWS IoT Core bằng MQTT.
* Kiểm thử gửi dữ liệu cảm biến lên AWS IoT Core.
* Kiểm thử ESP32 Camera xin Presigned URL và upload ảnh lên Amazon S3.
* Kiểm tra chất lượng hình ảnh biển số trong các điều kiện ánh sáng khác nhau.

### 5.3. Giai đoạn 3: Xây dựng backend trên AWS

Backend của hệ thống được xây dựng bằng các dịch vụ serverless của AWS.

Các công việc chính:

* Tạo Amazon API Gateway để nhận request từ Web/App và thiết bị.
* Tạo Lambda Backend xử lý nghiệp vụ.
* Tạo chức năng cấp Presigned URL cho ESP32 Camera.
* Tạo Amazon S3 Bucket để lưu ảnh xe.
* Cấu hình S3 Event ObjectCreated để trigger Lambda xử lý ảnh.
* Tích hợp Amazon Rekognition để phân tích hình ảnh.
* Tạo bảng DynamoDB để lưu dữ liệu bãi xe.
* Tạo Lambda xử lý dữ liệu cảm biến từ AWS IoT Core.
* Cấu hình IAM Role cho các dịch vụ có quyền truy cập phù hợp.

### 5.4. Giai đoạn 4: Xây dựng giao diện Web/App

Giao diện Web/App giúp người dùng và quản trị viên theo dõi trạng thái bãi đỗ xe.

Các chức năng chính:

* Đăng nhập và xác thực người dùng.
* Hiển thị sơ đồ bãi đỗ xe.
* Hiển thị trạng thái từng vị trí đỗ.
* Hiển thị danh sách xe ra/vào.
* Hiển thị biển số xe, hình ảnh và thời gian ghi nhận.
* Tìm kiếm lịch sử xe theo biển số.
* Xem thống kê số lượng xe trong bãi.
* Quản lý người dùng theo vai trò.

### 5.5. Giai đoạn 5: Tích hợp AI và giám sát

Giai đoạn cuối tập trung vào việc tích hợp AI và hoàn thiện hệ thống giám sát.

Các công việc chính:

* Xây dựng Lambda AI Service.
* Tích hợp Amazon Bedrock để hỗ trợ truy vấn thông minh.
* Kết nối AI Service với DynamoDB.
* Tạo dashboard hoặc chức năng thống kê dữ liệu bãi xe.
* Cấu hình CloudWatch để theo dõi log.
* Thiết lập cảnh báo lỗi hệ thống.
* Thiết lập cảnh báo chi phí bằng AWS Budgets.
* Kiểm thử toàn bộ hệ thống trước khi vận hành.

---

## 6. Ước tính ngân sách

Chi phí triển khai hệ thống Parking IoT phụ thuộc vào số lượng thiết bị, số lượng ảnh xử lý, số request API, dung lượng lưu trữ ảnh và mức độ sử dụng AI.

### 6.1. Chi phí phần cứng

| Hạng mục | Số lượng | Mục đích sử dụng |
| :--- | :---: | :--- |
| ESP32 Camera | Theo số cổng ra/vào | Chụp ảnh xe và biển số |
| ESP32 cảm biến | Theo số vị trí đỗ | Gửi trạng thái chỗ đỗ |
| Cảm biến siêu âm / hồng ngoại | Theo số vị trí đỗ | Phát hiện xe tại vị trí đỗ |
| Nguồn điện | Theo thiết bị | Cấp nguồn cho ESP32 |
| Dây nối, hộp bảo vệ | Theo nhu cầu | Bảo vệ thiết bị khi lắp đặt |
| Router / WiFi | 1 hoặc nhiều | Kết nối thiết bị với Internet |

### 6.2. Chi phí dịch vụ AWS

Các dịch vụ AWS có thể phát sinh chi phí bao gồm:

| Dịch vụ AWS | Mục đích sử dụng |
| :--- | :--- |
| AWS IoT Core | Nhận dữ liệu MQTT từ ESP32 cảm biến |
| Amazon S3 | Lưu trữ ảnh xe |
| AWS Lambda | Xử lý backend, xử lý ảnh và dữ liệu cảm biến |
| Amazon API Gateway | Nhận request từ Web/App và thiết bị |
| Amazon Rekognition | Phân tích hình ảnh, hỗ trợ nhận diện biển số |
| Amazon DynamoDB | Lưu dữ liệu xe, biển số, trạng thái chỗ đỗ |
| Amazon CloudFront | Phân phối giao diện website |
| Amazon Cognito | Xác thực và quản lý người dùng |
| Amazon CloudWatch | Ghi log và giám sát hệ thống |
| Amazon Bedrock | Hỗ trợ chức năng AI nâng cao |
| AWS Budgets | Theo dõi và cảnh báo chi phí |

Đối với mô hình demo hoặc triển khai quy mô nhỏ, chi phí có thể được kiểm soát bằng cách giới hạn số lượng ảnh xử lý, giảm thời gian lưu ảnh trên S3, tối ưu số lần gọi API Gateway và chỉ sử dụng Amazon Bedrock khi cần thiết.

---

## 7. Đánh giá rủi ro và chiến lược giảm thiểu

| Rủi ro | Mức độ | Chiến lược giảm thiểu |
| :--- | :---: | :--- |
| ESP32 mất kết nối mạng | Trung bình | Lưu tạm dữ liệu cục bộ và gửi lại khi có mạng |
| Ảnh biển số bị mờ | Cao | Điều chỉnh góc camera, ánh sáng và khoảng cách chụp |
| Nhận diện biển số sai | Trung bình | Kết hợp kiểm tra thủ công và cải thiện chất lượng ảnh |
| Thiết bị bị hỏng do môi trường | Trung bình | Dùng hộp bảo vệ, kiểm tra định kỳ thiết bị |
| API Gateway hoặc Lambda bị lỗi | Trung bình | Theo dõi log bằng CloudWatch và xử lý lỗi |
| Vượt chi phí AWS | Trung bình | Thiết lập AWS Budgets và cảnh báo chi phí |
| Dữ liệu bị truy cập trái phép | Cao | Dùng Cognito, IAM, WAF và phân quyền chặt chẽ |
| Hệ thống khó mở rộng | Thấp | Thiết kế serverless, dễ thêm thiết bị và dịch vụ |

---

## 8. Kết quả kỳ vọng

### 8.1. Về kỹ thuật

Sau khi hoàn thành, hệ thống dự kiến đạt được các kết quả sau:

* Xây dựng được hệ thống Parking IoT hoạt động theo thời gian thực.
* ESP32 Camera có thể chụp ảnh xe ra/vào và upload ảnh lên Amazon S3.
* ESP32 cảm biến có thể gửi trạng thái vị trí đỗ xe lên AWS IoT Core.
* AWS Lambda xử lý dữ liệu tự động, không cần máy chủ riêng.
* Amazon Rekognition hỗ trợ phân tích ảnh và nhận diện biển số.
* DynamoDB lưu trữ dữ liệu tập trung, hỗ trợ truy vấn nhanh.
* Web/App hiển thị trạng thái bãi xe, lịch sử xe ra/vào và thông tin biển số.
* Amazon Bedrock hỗ trợ chức năng AI, giúp người dùng truy vấn dữ liệu thông minh.
* CloudWatch hỗ trợ giám sát lỗi và theo dõi hoạt động hệ thống.

### 8.2. Về vận hành

Hệ thống giúp quá trình quản lý bãi đỗ xe trở nên tự động và hiệu quả hơn. Người quản lý có thể theo dõi trạng thái bãi xe từ xa, kiểm tra lịch sử xe ra/vào và giảm phụ thuộc vào thao tác thủ công.

Các lợi ích vận hành gồm:

* Giảm thời gian kiểm tra xe ra/vào.
* Tăng độ chính xác khi quản lý biển số và trạng thái chỗ đỗ.
* Hỗ trợ giám sát bãi xe theo thời gian thực.
* Dễ dàng mở rộng thêm camera hoặc cảm biến.
* Giảm nhu cầu vận hành máy chủ truyền thống.
* Tăng tính bảo mật thông qua xác thực và phân quyền người dùng.

---

## 9. Kết luận

Dự án **Parking IoT thông minh sử dụng AWS Serverless** là giải pháp phù hợp để hiện đại hóa việc quản lý bãi đỗ xe. Hệ thống kết hợp các công nghệ IoT, xử lý ảnh, lưu trữ dữ liệu, xác thực người dùng và trí tuệ nhân tạo nhằm tạo ra một nền tảng quản lý bãi xe tự động, linh hoạt và có khả năng mở rộng.

Với các dịch vụ như **AWS IoT Core**, **Amazon S3**, **AWS Lambda**, **Amazon API Gateway**, **Amazon Rekognition**, **Amazon DynamoDB**, **Amazon Cognito**, **Amazon CloudFront**, **AWS WAF**, **Amazon CloudWatch** và **Amazon Bedrock**, hệ thống có thể đáp ứng tốt các yêu cầu về giám sát thời gian thực, nhận diện biển số, quản lý người dùng và phân tích dữ liệu thông minh.

Dự án không chỉ giúp giải quyết các hạn chế của mô hình quản lý bãi xe thủ công mà còn tạo nền tảng để phát triển các chức năng nâng cao trong tương lai như dự báo mật độ xe, tối ưu vị trí đỗ, cảnh báo bất thường và hỗ trợ quản lý bằng AI.