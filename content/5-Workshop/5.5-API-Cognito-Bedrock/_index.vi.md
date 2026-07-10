---
title: "API Gateway, Cognito & Bedrock"
date: 2026-04-26
weight: 5
chapter: false
pre: " <b> 4.5. </b> "
---

Để cung cấp các điểm kết nối (Endpoints) cho ứng dụng Web Dashboard và hệ thống biên IoT, đồng thời đảm bảo an ninh thông tin và tích hợp trí tuệ nhân tạo, ba dịch vụ **AWS API Gateway**, **Amazon Cognito** và **Amazon Bedrock** đã được tích hợp chặt chẽ.

---

### 1. Kiến trúc luồng xử lý và Bảo mật (API Architecture)
Hệ thống sử dụng kiến trúc tuần tự bảo mật nhiều lớp để kiểm soát quyền truy cập, xác thực và điều phối yêu cầu từ phía người dùng khi giao tiếp với các dịch vụ backend và AI:

{{< mermaid >}}
sequenceDiagram
    participant User as Web Dashboard
    participant Cognito as Amazon Cognito
    participant APIGW as AWS API Gateway
    participant Lambda as AWS Lambda (ai-assistant)
    participant Dynamo as Amazon DynamoDB
    participant Bedrock as Amazon Bedrock
    
    User->>Cognito: 1. Gửi thông tin đăng nhập
    Cognito-->>User: 2. Trả JWT Token xác thực thành công
    User->>APIGW: 3. Gửi câu hỏi / yêu cầu dữ liệu (kèm JWT Token)
    APIGW->>Lambda: 4. Xác thực token và chuyển tiếp yêu cầu
    Lambda->>Dynamo: 5. Truy vấn trạng thái bãi xe và lịch sử xe (ngữ cảnh RAG)
    Dynamo-->>Lambda: 6. Trả dữ liệu thô thời gian thực từ bãi đỗ
    Lambda->>Bedrock: 7. Gửi câu hỏi kèm dữ liệu bãi xe (Claude LLM)
    Bedrock-->>Lambda: 8. Trả lời bằng tiếng Việt tự nhiên
    Lambda-->>APIGW: 9. Trả kết quả xử lý (HTTP 200 OK)
    APIGW-->>User: 10. Phản hồi và hiển thị kết quả trên Dashboard
{{< /mermaid >}}

---

### 2. Cấu hình xác thực với Amazon Cognito
Nhằm ngăn chặn truy cập trái phép vào Dashboard quản lý bãi xe, hệ thống triển khai dịch vụ **Amazon Cognito User Pool** để quản lý danh tính người dùng (Quản trị viên và nhân viên bãi đỗ):
- **User Pool Name**: `User pool - ahlii`
- **User Pool ID**: `ap-southeast-1_syJgrpSKt`
- **Kênh xác thực**: Đăng nhập bằng tên tài khoản/email và mật khẩu bảo mật cao. Sau khi đăng nhập thành công, Cognito sẽ cấp mã định danh bảo mật dạng **JSON Web Token (JWT)** cho trình duyệt để đính kèm vào tiêu đề (Header) của mỗi yêu cầu API.

![Cấu hình Cognito User Pool](/images/5-Workshop/5.5-API-Cognito-Bedrock/5.5-cognito.png)
*Minh chứng 5.5.1: Giao diện quản lý User Pool của Amazon Cognito xác thực người dùng*

---

### 3. Thiết kế các tuyến API trên AWS API Gateway
**AWS API Gateway** đóng vai trò cổng giao tiếp trung tâm (API Gateway), tiếp nhận và định tuyến các cuộc gọi HTTP API từ Web Dashboard đến các hàm Lambda xử lý tương ứng ở Backend.

#### 3.1. Danh sách các tuyến đường (Routes) được cấu hình trên `smart-parking-api` (ID: `ebhguaykmc`):
- **Tuyến `/parking/status` (Phương thức `GET`)**:
  - *Chức năng*: Truy vấn trạng thái trống/đầy hiện thời của các vị trí đỗ xe trong bãi.
  - *Tích hợp*: Gọi hàm Lambda xử lý để đọc thông tin từ bảng `SmartParking_Slots`.
- **Tuyến `/vehicle/history` (Phương thức `GET`)**:
  - *Chức năng*: Lấy nhật ký danh sách các lượt phương tiện ra vào bãi đỗ phục vụ thống kê.
  - *Tích hợp*: Gọi hàm Lambda xử lý để truy vấn bảng lịch sử `SmartParking_VehicleHistory`.
- **Tuyến `/chat` (Phương thức `ANY` - CORS enabled)**:
  - *Chức năng*: Giao tiếp trực tiếp với Trợ lý ảo AI đỗ xe thông minh.
  - *Tích hợp*: Kết nối với hàm Lambda `smart-parking-ai-assistant`.

![Danh sách Tuyến API Gateway](/images/5-Workshop/5.5-API-Cognito-Bedrock/5.5-routes.png)
*Minh chứng 5.5.2: Định nghĩa các Routes trên AWS API Gateway cho hệ thống đỗ xe*

---

### 4. Tích hợp Trợ lý ảo AI với Amazon Bedrock

#### 4.1. Hàm Lambda điều phối AI (`smart-parking-ai-assistant`)
Hàm Lambda chạy trên môi trường **Node.js 20** tiếp nhận câu hỏi tự nhiên từ người dùng trên Web Dashboard, sau đó tự động thu thập ngữ cảnh bãi xe và gửi tới mô hình ngôn ngữ lớn để trả lời.

![Mã nguồn Lambda AI Assistant](/images/5-Workshop/5.5-API-Cognito-Bedrock/5.5-bedrock-lambda.png)
*Minh chứng 5.5.3: Cấu trúc mã nguồn điều phối AI trợ lý bãi đỗ xe liên kết với API Gateway*

#### 4.2. Quy trình xử lý RAG (Retrieval-Augmented Generation) và tích hợp Bedrock
Để trợ lý AI có thể trả lời chính xác số lượng xe hiện tại hoặc lịch sử ra vào mà không cần huấn luyện lại mô hình, quy trình xử lý ngữ cảnh (RAG) được thực hiện như sau:

1. **Nhận câu hỏi**: Hàm Lambda tiếp nhận câu hỏi tiếng Việt của người dùng (Ví dụ: *"Hiện tại trong bãi còn chỗ trống nào không?"*).
2. **Truy vấn ngữ cảnh thời gian thực (Context Retrieval)**: Lambda thực hiện quét (Scan/Query) dữ liệu từ hai bảng DynamoDB `SmartParking_Slots` và `SmartParking_VehicleHistory` để lấy danh sách số chỗ đỗ xe đang trống và các xe ra vào gần nhất.
3. **Xây dựng Prompt tích hợp dữ liệu**: Lambda lồng dữ liệu thực tế thu được từ cơ sở dữ liệu vào khung Prompt chuẩn bị gửi cho AI:
   ```text
   Bạn là Trợ lý ảo thông minh của bãi đỗ xe Smart Parking.
   Dữ liệu thời gian thực từ cơ sở dữ liệu của bãi xe:
   - Tổng số chỗ đỗ: 10 chỗ.
   - Trạng thái hiện tại: slot-01 đang BẬN, slot-02 đang TRỐNG, slot-03 đang TRỐNG.
   - Nhật ký xe ra vào gần nhất: Xe 30E-922.91 vào lúc 14:05.

   Hãy trả lời câu hỏi sau của người dùng bằng tiếng Việt ngắn gọn và lịch sự:
   [Câu hỏi người dùng]
   ```
4. **Gọi mô hình qua Amazon Bedrock**: Sử dụng AWS SDK để gọi dịch vụ Amazon Bedrock (sử dụng mô hình nền tảng như Anthropic Claude 3.5 Sonnet hoặc Claude 3 Haiku) bằng API `InvokeModel`:
   ```javascript
   const { BedrockRuntimeClient, InvokeModelCommand } = require("@aws-sdk/client-bedrock-runtime");
   const client = new BedrockRuntimeClient({ region: "ap-southeast-1" });
   
   const command = new InvokeModelCommand({
     modelId: "anthropic.claude-3-5-sonnet-20241022-v2:0",
     contentType: "application/json",
     body: JSON.stringify({
       anthropic_version: "bedrock-2023-05-31",
       max_tokens: 500,
       messages: [{ role: "user", content: formattedPrompt }]
     })
   });
   const response = await client.send(command);
   ```
5. **Trả về kết quả**: Trích xuất nội dung văn bản trả lời từ phản hồi của Bedrock và gửi ngược lại cho giao diện người dùng Web Dashboard qua API Gateway.
