---
title: "Giám sát hệ thống với CloudWatch"
date: 2026-04-26
weight: 8
chapter: false
pre: " <b> 4.8. </b> "
---

Để duy trì tính ổn định, giám sát hiệu năng vận hành thời gian thực và kịp thời phát hiện các lỗi phát sinh trong kiến trúc Serverless, hệ thống sử dụng dịch vụ giám sát tập trung **Amazon CloudWatch**. Toàn bộ hoạt động ghi nhật ký (Logging) của các thành phần backend và IoT đều được tập hợp về đây để phục vụ công tác giám sát và chẩn đoán.

---

### 1. Phân hệ Log Groups của các hàm AWS Lambda
Mỗi khi một hàm AWS Lambda được kích hoạt để xử lý sự kiện (nhận dạng biển số, cập nhật vị trí đỗ từ cảm biến, xác thực API), một **Log Group** (Nhóm nhật ký) tương ứng sẽ tự động được tạo ra trên Amazon CloudWatch Logs. 

Hiện tại, hệ thống giám sát ghi nhận **13 Log Groups** dành cho các hàm dịch vụ lõi:

![Danh sách Log Groups](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-logs.png)
*Minh chứng 5.8.1: Giao diện quản lý các nhóm nhật ký (Log Groups) của các hàm Lambda trên CloudWatch*

---

### 2. Chi tiết nhật ký thực thi của từng phân hệ lõi
Để đánh giá chi tiết quá trình vận hành, dưới đây là minh chứng cấu hình thực tế và nội dung Nhật ký Sự kiện (Log Events) / Luồng nhật ký (Log Streams) trích xuất từ các Log Groups của toàn bộ 13 hàm Lambda trong hệ thống:

#### 2.1. Phân hệ Nhận diện Biển số xe (`smart-parking-detect-plate`)
Hàm này nhận sự kiện kích hoạt từ S3 khi có ảnh mới, gọi Amazon Rekognition để OCR biển số, điều khiển cổng Barie và lưu thông tin vào DynamoDB.

- **Log Stream được chọn**: `2026/07/09/[$LATEST]a01b705ba4f5495eac53ccc0f4ff250b`

![Nhật ký sự kiện detect-plate](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events.png)
*Minh chứng 5.8.2: Nhật ký xử lý nhận diện biển số xe của AWS Lambda*

**Phân tích nhật ký sự kiện**:
- `EVENT`: Ghi nhận dữ liệu kích hoạt hướng sự kiện (Event-driven) từ S3 Bucket (`ObjectCreated:Put`) khi ảnh xe được tải lên thư mục cổng vào.
- `REKOGNITION`: Kết quả trả về từ Amazon Rekognition nhận dạng chính xác biển số **`29K-258.17`** với độ tin cậy đạt **`97.28%`**.
- `GATE_COMMAND_CREATED`: Sinh lệnh điều khiển mở cổng `OPEN` gửi tới cổng kiểm soát xe vào (`gate-in-01`).
- `SAVED_ITEM`: Lưu trữ bản ghi thành công vào DynamoDB và bật cờ cho phép mở cổng (`"allow_open": true`).
- `REPORT`: Phiên thực thi hoàn tất trong thời gian **`905.45 ms`** (Dưới 1 giây) và chỉ tiêu thụ tối đa **`97 MB`** bộ nhớ RAM trên tổng số `128 MB` được cấu hình.

---

#### 2.2. Phân hệ Cập nhật Ô đỗ cảm biến (`smart-parking-slot-update`)
Hàm Lambda này nhận dữ liệu khoảng cách từ cảm biến siêu âm HC-SR04 được gửi lên bởi ESP32-S3, sau đó phân tích và ghi nhận trạng thái ô đỗ vào DynamoDB.

- **Log Stream được chọn**: `2026/07/09/[$LATEST]430dc2dcf3dd45b48c7bd615aa5b7429`

![Nhật ký sự kiện slot-update](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-slot-update.png)
*Minh chứng 5.8.3: Nhật ký xử lý cập nhật trạng thái ô đỗ từ cảm biến siêu âm*

**Phân tích nhật ký sự kiện**:
- `Received event: {"device_id": "esp-slot-01", "slot_id": "A1", "occupied": true, "distance": 2.8}`: Cho thấy Lambda nhận thành công payload JSON từ ESP32-S3 gửi về thiết bị kiểm soát slot A1 với khoảng cách đo được là `2.8 cm` (nhỏ hơn ngưỡng 15cm nên xác định trạng thái đỗ `occupied: true`).
- `REPORT`: Thời gian thực hiện lưu DynamoDB và phản hồi của Lambda cực kỳ nhanh, chỉ tốn **`290.02 ms`** với bộ nhớ RAM tiêu thụ tối đa **`94 MB`**.

---

#### 2.3. Phân hệ API lấy trạng thái bãi xe (`Get_Parking_Status`)
Hàm REST API phục vụ Web Dashboard lấy danh sách trạng thái ô đỗ đỗ xe hiện thời để cập nhật bản đồ bãi đỗ thời gian thực.

- **Log Stream được chọn**: `2026/07/10/[$LATEST]e81c07f1a4d7411fb09f22dc6689564e`

![Nhật ký sự kiện Get_Parking_Status](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-parking-status.png)
*Minh chứng 5.8.4: Nhật ký thực thi API lấy trạng thái bãi đỗ xe hiện tại*

**Phân tích nhật ký sự kiện**:
- Log ghi nhận hàng loạt phiên kết nối từ Web Dashboard Client thông qua API Gateway.
- Thời gian xử lý trung bình của API cực thấp, dao động từ **`25.74 ms`** đến **`58.71 ms`**, đảm bảo giao diện người dùng phản hồi mượt mà gần như ngay lập tức.
- Dung lượng bộ nhớ RAM tiêu thụ ổn định ở mức **`97 MB`**.

---

#### 2.4. Phân hệ Trợ lý ảo AI đỗ xe (`smart-parking-ai-assistant`)
Hàm Lambda chịu trách nhiệm xử lý logic chatbot hỗ trợ đỗ xe, liên kết RAG dữ liệu từ DynamoDB và chuyển tiếp câu hỏi tới Amazon Bedrock để suy luận trả lời.

- **Log Stream được chọn**: `2026/07/09/[$LATEST]ea468fd7a69f4a7082765ba878c8d777`

![Nhật ký sự kiện ai-assistant](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-ai-assistant.png)
*Minh chứng 5.8.5: Nhật ký thực thi xử lý chatbot AI tích hợp Amazon Bedrock*

**Phân tích nhật ký sự kiện**:
- `INIT_START Runtime Version: nodejs:24...`: Chạy trên môi trường Node.js v24.
- `REPORT`: Thời gian xử lý phiên suy luận đạt **`2403.76 ms`** (~2.4 giây). Thời gian này lâu hơn các API thông thường do Lambda phải chờ kết quả suy luận từ mô hình AI Bedrock (Claude/LLaMA) và truy xuất dữ liệu ngữ cảnh RAG từ DynamoDB.
- Dung lượng bộ nhớ RAM tiêu thụ thực tế đạt **`111 MB`** trên tổng số `128 MB` cấp phát.

---

#### 2.5. Phân hệ WebSocket Chat hỗ trợ realtime (`OnMessage`)
Hàm quản lý việc định tuyến và đồng bộ tin nhắn realtime giữa khách hàng và quản trị viên thông qua kết nối kết trì WebSockets của API Gateway.

- **Log Stream được chọn**: `2026/06/28/[$LATEST]e00925c02c844c6795dc6a7ee6a1e0f6`

![Nhật ký sự kiện OnMessage](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-events-websocket.png)
*Minh chứng 5.8.6: Nhật ký định tuyến tin nhắn chat qua kết nối WebSockets*

**Phân tích nhật ký sự kiện**:
- `INFO Event: { "requestContext": { "routeKey": "sendMessage", "messageId": "gSW-..." } }`: Ghi nhận sự kiện khi có tin nhắn chat mới gửi lên thông qua route `sendMessage`. Tin nhắn sẽ được đồng bộ ngay lập tức tới client còn lại qua kết nối WebSocket Client.
- Thời gian định tuyến tin nhắn chỉ mất trung bình khoảng **`62.52 ms`** đến **`90.59 ms`**, giúp cuộc hội thoại realtime diễn ra mượt mà và không bị trễ.

---

#### 2.6. Phân hệ API lấy lịch sử xe gửi (`Get_Vehicle_History`)
Nhóm nhật ký ghi lại các yêu cầu gọi từ ứng dụng Web Dashboard Client để lấy danh sách lịch sử xe vào ra bãi của người dùng hoặc admin.

![Nhật ký Get_Vehicle_History](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-vehicle-history.png)
*Minh chứng 5.8.7: Luồng nhật ký thực thi của API Get_Vehicle_History*

---

#### 2.7. Phân hệ WebSocket OnConnect (`OnConnect`)
Xử lý các sự kiện thiết lập kết nối WebSocket ban đầu từ giao diện web chat hỗ trợ.

![Nhật ký OnConnect](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-onconnect.png)
*Minh chứng 5.8.8: Luồng nhật ký thực thi kết nối WebSockets của OnConnect*

---

#### 2.8. Phân hệ WebSocket OnDisconnect (`OnDisconnect`)
Xử lý các sự kiện ngắt kết nối WebSocket khi người dùng tắt trình duyệt hoặc mất kết nối.

![Nhật ký OnDisconnect](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-ondisconnect.png)
*Minh chứng 5.8.9: Luồng nhật ký thực thi ngắt kết nối WebSockets của OnDisconnect*

---

#### 2.9. Phân hệ API Quản lý Tài khoản (`account-api`)
Nhật ký thực thi của API quản lý thông tin người dùng, đổi mật khẩu và đăng ký biển số.

![Nhật ký account-api](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-account-api.png)
*Minh chứng 5.8.10: Luồng nhật ký thực thi của phân hệ quản trị tài khoản account-api*

---

#### 2.10. Phân hệ gửi lệnh cổng chắn (`smart-parking-gate-command`)
Xử lý việc gửi các sự kiện điều khiển đóng/mở cổng Barie trực tiếp đến ESP32-CAM tại trạm vật lý.

![Nhật ký smart-parking-gate-command](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-gate-command.png)
*Minh chứng 5.8.11: Luồng nhật ký thực thi gửi lệnh điều khiển tới cổng chắn*

---

#### 2.11. Phân hệ Tự động Tạo người dùng (`smart-parking-save-user-to-db`)
Tự động kích hoạt khi có tài khoản mới đăng ký thành công trên Cognito để sao lưu thông tin tài khoản người dùng tương ứng vào DynamoDB.

![Nhật ký smart-parking-save-user-to-db](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-save-user.png)
*Minh chứng 5.8.12: Luồng nhật ký lưu trữ thông tin tài khoản mới đăng ký*

---

#### 2.12. Phân hệ Quản lý upload ảnh lên S3 (`smart-parking-upload-lambda`)
Xử lý tiến trình tạo mã chữ ký Presigned URL và tải ảnh chụp từ ESP32-CAM lên S3 Bucket lưu trữ.

![Nhật ký smart-parking-upload-lambda](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-upload-lambda.png)
*Minh chứng 5.8.13: Luồng nhật ký tiến trình Lambda upload ảnh lên S3*

---

#### 2.13. Phân hệ Bắt sự kiện phương tiện (`smart-parking-vehicle-event`)
Theo dõi, xử lý và định tuyến các luồng sự kiện trạng thái xe ra vào trong bãi đỗ.

![Nhật ký smart-parking-vehicle-event](/images/5-Workshop/5.8-Monitoring-CloudWatch/aws-cloudwatch-log-streams-vehicle-event.png)
*Minh chứng 5.8.14: Luồng nhật ký tiến trình Lambda smart-parking-vehicle-event*
