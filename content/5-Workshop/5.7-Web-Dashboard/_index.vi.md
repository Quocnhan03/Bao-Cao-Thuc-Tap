---
title: "Web Dashboard quản trị hệ thống"
date: 2026-04-26
weight: 7
chapter: false
pre: " <b> 4.7. </b> "
---

Nhằm hỗ trợ công tác giám sát, thống kê và vận hành bãi đỗ xe trực quan, một ứng dụng Web Dashboard quản trị toàn diện được xây dựng bằng công nghệ **React/Next.js** kết hợp với thư viện thiết kế hiện đại, triển khai phân phối qua **Amazon CloudFront** (`https://d3imp0j8sdburp.cloudfront.net/`). 

Hệ thống phân tách thành hai cổng thông tin (Portals) hoạt động song song dựa trên phân quyền người dùng từ Amazon Cognito: **Admin Portal (Cổng quản trị viên)** và **User Portal (Cổng dành cho khách hàng)**.

---

### 1. Kiến trúc tích hợp hạ tầng AWS của Web Dashboard
Để đảm bảo khả năng mở rộng, tính bảo mật cao và thời gian phản hồi thấp, Web Dashboard không sử dụng máy chủ truyền thống mà được triển khai theo kiến trúc **Serverless** trên đám mây AWS.

{{< mermaid >}}
graph TD
    User[Khách hàng / Admin] -->|1. HTTPS| CF[Amazon CloudFront]
    CF -->|Phân phối web| S3Web[Amazon S3 Static Hosting]
    S3Web -->|Tải React App về trình duyệt| WebApp[React Web Dashboard]
    
    WebApp -->|2. Đăng nhập / Lấy JWT| Cognito[Amazon Cognito User Pool]
    WebApp -->|3. Gọi REST API + JWT| APIGW[Amazon API Gateway]
    WebApp -->|4. Kết nối WebSocket| AppSync[Amazon AppSync GraphQL]
    
    APIGW -->|Kích hoạt Lambda| Lambda[AWS Lambda Backend]
    Lambda -->|Đọc/Ghi dữ liệu| DDB[Amazon DynamoDB]
    Lambda -->|Prompt RAG| Bedrock[Amazon Bedrock AI]
    
    AppSync -->|Đồng bộ tin nhắn| DDB_Chat[Amazon DynamoDB Chat Logs]
{{< /mermaid >}}

#### 1.1. Lưu trữ và Phân phối Static Web (S3 + CloudFront)
Toàn bộ mã nguồn đóng gói của ứng dụng React/Next.js được lưu trữ tại S3 Bucket và phân phối toàn cầu qua Amazon CloudFront CDN.

- **S3 Bucket lưu trữ web**:
  - Tên Bucket: `smart-parking-fe-prod-075647413376-ap-southeast-1-an`
  - Vùng tài nguyên (Region): `ap-southeast-1` (Singapore).
  - Tệp cấu trúc chính chứa mã nguồn Vite/React được đẩy lên bao gồm: thư mục `assets/` chứa các tệp mã nguồn JS/CSS đóng gói, cùng tệp `index.html` làm điểm vào (Entry point).

![Danh sách S3 Buckets](/images/5-Workshop/5.7-Web-Dashboard/aws-s3-list.png)
*Minh chứng 5.7.1a: Danh sách S3 Buckets trong hệ thống lưu trữ*

![Các tệp tin web trên S3](/images/5-Workshop/5.7-Web-Dashboard/aws-s3-objects.png)
*Minh chứng 5.7.1b: Các tệp mã nguồn đóng gói của Web App lưu trữ trên S3*

- **Amazon CloudFront Distribution**:
  - ID phân phối: `EHS22PYCLM5X0`
  - Domain phân phối mặc định: `d3imp0j8sdburp.cloudfront.net`
  - Origin: Trỏ trực tiếp về S3 Bucket chứa mã nguồn tĩnh (`smart-parking-fe-prod...`).
  - Giao thức hỗ trợ: Tự động tối ưu hóa SSL/TLS, định tuyến chuyển tiếp cổng `HTTP` sang `HTTPS` bảo mật cao và trỏ tệp mặc định (Default root object) là `index.html`.

![Danh sách CloudFront](/images/5-Workshop/5.7-Web-Dashboard/aws-cloudfront.png)
*Minh chứng 5.7.1c: Danh sách các phân phối CloudFront CDN trong hệ thống*

![Chi tiết CloudFront](/images/5-Workshop/5.7-Web-Dashboard/aws-cloudfront-details.png)
*Minh chứng 5.7.1d: Cấu hình chi tiết của CloudFront trỏ nguồn về S3 hosting*

---

#### 1.2. Xác thực người dùng (Amazon Cognito)
Hệ thống sử dụng Amazon Cognito User Pool để kiểm soát danh tính và thực hiện cơ chế phân quyền (Role-based access control).

- **Cognito User Pool**:
  - Tên User Pool: `User pool - ahlii`
  - ID: `ap-southeast-1_syJgrpSKt`
  - ARN: `arn:aws:cognito-idp:ap-southeast-1:075647413376:userpool/ap-southeast-1_syJgrpSKt`

![Chi tiết Cognito User Pool](/images/5-Workshop/5.7-Web-Dashboard/aws-cognito-details.png)
*Minh chứng 5.7.2a: Thông tin tổng quan cấu hình User Pool trên AWS*

- **App client integration**:
  - Tên App Client: `OTP GMAIL`
  - Client ID kết nối: `5mvc3hhro0ic13s6c1sm2dd9o2`
  - Mô tả: Mã Client ID này được cấu hình trực tiếp vào ứng dụng frontend nhằm gọi API đăng nhập, lấy Token dạng JWT phục vụ xác thực khi gọi các REST API biên.

![Chi tiết App Client Cognito](/images/5-Workshop/5.7-Web-Dashboard/aws-cognito-clients.png)
*Minh chứng 5.7.2b: Cấu hình App Client ID phục vụ kết nối tích hợp từ Frontend web*

---

#### 1.3. Đồng bộ hội thoại hỗ trợ thời gian thực (AWS AppSync)
Trang hỗ trợ khách hàng chat realtime sử dụng **AWS AppSync** (GraphQL API) với cơ chế WebSocket Subscription giúp truyền nhận tin nhắn tức thời mà không cần duy trì máy chủ EC2 truyền thống.

- **GraphQL API AppSync**:
  - Tên API: `smart-parking-chat-api`
  - API ID: `5dlkezm2rbdgfl6k2oprzh5m4m`
  - Phương thức xác thực chính (Primary authorization mode): `API_KEY`
  - Real-time Endpoint (WebSocket): `wss://lospzfnpsvbwdcd34p3cubphvm.appsync-realtime-api.ap-southeast-1.amazonaws.com/graphql`

![Danh sách AppSync API](/images/5-Workshop/5.7-Web-Dashboard/aws-appsync-list.png)
*Minh chứng 5.7.3a: Danh sách các API GraphQL tích hợp trên AWS AppSync*

![Cấu hình AppSync settings](/images/5-Workshop/5.7-Web-Dashboard/aws-appsync-settings.png)
*Minh chứng 5.7.3b: Cấu hình Endpoint GraphQL và cơ chế xác thực bảo mật API Key của trạm Chat*

---

#### 1.4. Luồng xử lý và đồng bộ trạng thái chỗ đỗ xe thời gian thực (Slots Flow)
Để hiển thị sơ đồ bãi xe trực quan gồm các ô đỗ Xanh (Trống) / Đỏ (Có xe), hệ thống thực hiện luồng đồng bộ từ cảm biến siêu âm qua hệ quản trị cơ sở dữ liệu lên giao diện người dùng:

{{< mermaid >}}
sequenceDiagram
    participant Sensor as ESP32-S3 (Bãi đỗ)
    participant local as Local Backend Server
    participant DDB as Amazon DynamoDB
    participant Web as Web Dashboard (Client)
    participant APIGW as AWS API Gateway
    participant Lambda as AWS Lambda
    
    Sensor->>local: 1. POST /device/slot/update (Gửi khoảng cách đo được)
    local->>DDB: 2. Cập nhật trạng thái occupied (true/false) vào bảng SmartParking_Slots
    loop Định kỳ Polling cập nhật giao diện
        Web->>APIGW: 3. GET /parking/status (Yêu cầu trạng thái bãi đỗ)
        APIGW->>Lambda: 4. Xác thực và chuyển tiếp yêu cầu
        Lambda->>DDB: 5. Scan/Query bảng SmartParking_Slots
        DDB-->>Lambda: 6. Trả về danh sách trạng thái các ô đỗ (A1-A3, B1-B3)
        Lambda-->>APIGW: 7. Trả về dữ liệu dạng JSON (HTTP 200 OK)
        APIGW-->>Web: 8. Cập nhật màu sắc ô đỗ: Đỏ (Có xe) / Xanh (Trống)
    end
{{< /mermaid >}}

---

#### 1.5. Luồng truy vấn thông tin xe đăng ký và lịch sử gửi xe cá nhân (User Vehicle & History Flow)
Đối với Cổng thông tin khách hàng (User Portal), để hiển thị biển số xe đã đăng ký và 5 lượt ra vào gần nhất của phương tiện đó, hệ thống thực hiện luồng xác thực và truy vấn an toàn:

{{< mermaid >}}
sequenceDiagram
    participant Web as Web Dashboard (User Portal)
    participant Cognito as Amazon Cognito
    participant APIGW as AWS API Gateway
    participant Lambda as AWS Lambda
    participant DDB as Amazon DynamoDB
    
    Web->>Cognito: 1. Đăng nhập tài khoản khách hàng
    Cognito-->>Web: 2. Trả về JWT ID Token (chứa email người dùng)
    Web->>APIGW: 3. GET /vehicle/history (gửi kèm JWT Token trong Header Authorization)
    APIGW->>Cognito: 4. Kiểm tra chữ ký & thời hạn của JWT Token
    Cognito-->>APIGW: 5. Xác nhận Token hợp lệ
    APIGW->>Lambda: 6. Chuyển tiếp yêu cầu (kèm thông tin email trích xuất từ Token)
    Lambda->>DDB: 7. Query lịch sử trong bảng SmartParking_VehicleHistory theo email/biển số xe
    DDB-->>Lambda: 8. Trả về danh sách các lượt ra vào
    Lambda-->>APIGW: 9. Trả kết quả mảng JSON lịch sử (HTTP 200 OK)
    APIGW-->>Web: 10. Hiển thị biển số xe đã đăng ký, vị trí xe hiện tại và danh sách lịch sử
{{< /mermaid >}}


---

### 2. Phân hệ Cổng thông tin Quản trị viên (Admin Portal)
Dành cho nhân viên vận hành và quản lý bãi đỗ xe để giám sát toàn cục hệ thống.

#### 2.1. Bảng điều khiển tổng quan (Dashboard Admin)
Cung cấp các chỉ số vận hành KPIs thời gian thực bao gồm: chỗ trống còn lại, tỉ lệ lấp đầy, tổng lượt xe ra vào trong ngày và biểu đồ trực quan vị trí đỗ (`A1-A3`, `B1-B3`) chuyển trạng thái xanh/đỏ tự động thông qua tín hiệu cảm biến.
![Giao diện Dashboard chính](/images/5-Workshop/5.7-Web-Dashboard/5.7-dashboard.png)
*Minh chứng 5.7.4: Bảng điều khiển tổng quan và sơ đồ bãi xe thời gian thực của Admin*

#### 2.2. Nhật ký phương tiện toàn bãi đỗ (Vehicles Log)
Lưu lịch sử xe vào/ra, tích hợp tìm kiếm theo biển số, chiều xe chạy (vào/ra), camera chụp ảnh kiểm soát, độ tin cậy Rekognition và liên kết xem ảnh gốc lưu trên S3.
![Giao diện nhật ký phương tiện](/images/5-Workshop/5.7-Web-Dashboard/5.7-vehicles.png)
*Minh chứng 5.7.5: Trang tra cứu nhật ký phương tiện toàn bãi đỗ*

#### 2.3. Thống kê & Dự báo lưu lượng (Analytics)
Phân tích lưu lượng xe theo tháng/giờ bằng các biểu đồ trực quan và tích hợp tính năng dự báo lưu lượng 7 ngày tới thông qua Amazon Bedrock.
![Giao diện phân tích và biểu đồ](/images/5-Workshop/5.7-Web-Dashboard/5.7-analytics.png)
*Minh chứng 5.7.6: Trang biểu đồ thống kê lưu lượng xe và dự báo AI*

#### 2.4. Trợ lý ảo AI đỗ xe (AI Assistant - Admin)
Chatbot **ParkAI** (được cung cấp bởi Amazon Bedrock) hỗ trợ người quản trị truy vấn thông tin bãi xe bằng ngôn ngữ tự nhiên tiếng Việt qua dữ liệu RAG.
![Giao diện trợ lý ảo AI](/images/5-Workshop/5.7-Web-Dashboard/5.7-ai-assistant.png)
*Minh chứng 5.7.7: Chatbot trợ lý ảo ParkAI trên giao diện quản trị*

#### 2.5. Quản lý vai trò thành viên (Role Management)
Quản trị tài khoản nhân viên, phân quyền vai trò (`admin` / `user`), khóa/mở tài khoản và đổi mật khẩu an toàn.
![Giao diện quản lý vai trò](/images/5-Workshop/5.7-Web-Dashboard/5.7-roles.png)
*Minh chứng 5.7.8: Giao diện quản lý tài khoản và phân quyền thành viên*

#### 2.6. Hỗ trợ khách hàng thời gian thực (Support Chat - Admin)
Tiếp nhận danh sách các yêu cầu hỗ trợ và trò chuyện trực tiếp thời gian thực với khách hàng thông qua hạ tầng AWS AppSync và Amplify.
![Giao diện chat hỗ trợ realtime admin](/images/5-Workshop/5.7-Web-Dashboard/5.7-support.png)
*Minh chứng 5.7.9: Hệ thống hỗ trợ khách hàng đồng bộ realtime trên giao diện Admin*

---

### 3. Phân hệ Cổng thông tin Khách hàng (User Portal)
Dành cho người gửi xe (Khách hàng) đăng nhập để quản lý phương tiện cá nhân và yêu cầu trợ giúp.

#### 3.1. Tổng quan trạng thái (User Dashboard)
Hiển thị trạng thái bãi xe hiện thời (còn chỗ hay hết chỗ), số lượng chỗ đỗ trống tổng quan và hiệu suất lấp đầy của từng phân khu để khách hàng chủ động chọn khu vực đỗ xe.
![Giao diện tổng quan phía User](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-dashboard.png)
*Minh chứng 5.7.10: Giao diện tổng quan trạng thái bãi xe phía khách hàng*

#### 3.2. Xe của tôi (My Vehicle Status)
Hiển thị thông tin trạng thái xe hiện tại của khách hàng đang ở trong hay ngoài bãi, vị trí nhìn thấy lần cuối cùng, camera ghi nhận và lịch sử 5 lượt ra vào gần nhất của xe.
![Giao diện quản lý xe của tôi](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-mycar.png)
*Minh chứng 5.7.11: Trang theo dõi trạng thái xe hiện tại của khách hàng*

#### 3.3. Hỗ trợ sự cố trực tuyến (Support Chat - User)
Cho phép khách hàng tạo ticket yêu cầu trợ giúp trực tiếp và nhắn tin trao đổi trực tiếp thời gian thực với quản trị viên bãi xe khi có sự cố.
![Giao diện chat hỗ trợ phía User](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-support.png)
*Minh chứng 5.7.12: Khung chat hỗ trợ trực tuyến realtime của khách hàng*

#### 3.4. Trợ lý tư vấn vị trí đỗ AI (AI Assistant - User)
Trợ lý ảo thông minh giải đáp các thắc mắc về vị trí đỗ xe trống và các dịch vụ bãi xe cho người dùng bằng ngôn ngữ tự nhiên.
![Giao diện trợ lý AI phía User](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-ai.png)
*Minh chứng 5.7.13: Chatbot AI tư vấn vị trí đỗ thời gian thực cho người dùng*

#### 3.5. Lịch sử gửi xe cá nhân (User History)
Bảng tra cứu toàn bộ lịch sử gửi xe cá nhân của tài khoản khách hàng kèm hình ảnh minh chứng và độ tin cậy Rekognition.
![Giao diện lịch sử gửi xe phía User](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-history.png)
*Minh chứng 5.7.14: Lịch sử chi tiết các lượt xe ra vào bãi của tài khoản khách hàng*

#### 3.6. Cài đặt tài khoản & Biển số xe đăng ký (User Profile Settings)
Trang quản lý hồ sơ khách hàng, cập nhật biển số xe đăng ký chính thức để kích hoạt cơ chế nhận dạng tự động, và thay đổi mật khẩu đăng nhập cá nhân.
![Giao diện cài đặt tài khoản User](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-profile.png)
*Minh chứng 5.7.15: Trang cài đặt thông tin cá nhân và đăng ký biển số xe*
