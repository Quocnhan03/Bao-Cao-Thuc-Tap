---
title: "Cấu hình AWS IoT Core"
date: 2026-04-26
weight: 1
chapter: false
pre: " <b> 4.3.1. </b> "
---

Trong quá trình xây dựng hệ thống đỗ xe thông minh, việc thiết lập kênh truyền thông tin cậy và bảo mật giữa thiết bị biên (ESP32) và đám mây được thực hiện thông qua cấu hình các thành phần quản lý định danh, xác thực và phân quyền trên **AWS IoT Core**.

---

### 1. Đăng ký thiết bị biên (Thing Registration)
Để định danh thiết bị vật lý trên môi trường đám mây, một đối tượng thiết bị (**Thing**) đã được khởi tạo trong Registry của AWS IoT Core:
- **Tên thiết bị (Thing Name)**: `ESP32_SmartParking`
- **Vai trò**: Đại diện cho trạm kiểm soát vật lý tại cổng bãi đỗ xe, chịu trách nhiệm gửi dữ liệu trạng thái chỗ đỗ từ cảm biến siêu âm và hình ảnh từ camera về hệ thống trung tâm.

![Đăng ký IoT Thing](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-create-thing.png)
*Minh chứng 5.3.1.1: Trạng thái thiết bị ESP32_SmartParking được đăng ký thành công trên AWS IoT Core*

---

### 2. Cơ chế xác thực và chứng chỉ bảo mật (Certificates)
Giao tiếp giữa thiết bị ESP32 và AWS IoT Core được bảo vệ bằng cơ chế mã hóa và xác thực hai chiều dựa trên tiêu chuẩn chứng chỉ số **X.509**:
- **Device Certificate**: Chứng chỉ dùng để xác thực danh tính duy nhất của thiết bị ESP32 với AWS IoT Core MQTT Broker.
- **Private Key**: Khóa riêng tư dùng để thiết lập kết nối mã hóa TLS bảo mật, được lưu trữ an toàn để nạp vào bộ nhớ của vi điều khiển và không thể tải lại từ console AWS.
- **Amazon Root CA 1**: Chứng chỉ gốc của Amazon giúp thiết bị xác minh tính chính thống của máy chủ AWS IoT Core đang kết nối.

Các chứng chỉ này được kích hoạt ở trạng thái **Active** để sẵn sàng cho quá trình xác thực khi thiết bị khởi động và kết nối mạng.

![Trạng thái Chứng chỉ](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-certificates.png)
*Minh chứng 5.3.1.2: Các chứng chỉ bảo mật liên kết với thiết bị ở trạng thái Active*

---

### 3. Phân quyền và kiểm soát truy cập (AWS IoT Policy)
Chính sách bảo mật **AWS IoT Policy** được thiết lập với tên gọi `esp-slot-01-policy` và gắn trực tiếp với chứng chỉ xác thực của thiết bị. Nhằm tuân thủ nguyên tắc đặc quyền tối thiểu (Least Privilege), chính sách này chỉ mở ra các quyền hạn tối thiểu cần thiết cho hoạt động của trạm kiểm soát:
- **iot:Connect**: Giới hạn quyền kết nối của thiết bị, chỉ cho phép kết nối thành công khi sử dụng đúng Client ID là `esp-slot-01`.
- **iot:Publish**: Chỉ cho phép thiết bị gửi (Publish) dữ liệu trạng thái lên một topic duy nhất là `smart-parking/slots/update`.

Tài liệu cấu hình JSON của chính sách bảo mật được thiết lập như sau:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:aws:iot:ap-southeast-1:075647413376:client/esp-slot-01"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": "arn:aws:iot:ap-southeast-1:075647413376:topic/smart-parking/slots/update"
    }
  ]
}
```

![Cấu hình IoT Policy](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-iot-policy.png)
*Minh chứng 5.3.1.3: Cấu hình chi tiết mã nguồn JSON của Policy esp-slot-01-policy*

---

### 4. Điểm cuối kết nối thiết bị (MQTT Endpoint)
Địa chỉ **Device data endpoint** của tài khoản được xác định tại mục cấu hình hệ thống trên AWS IoT Core. Đây là địa chỉ IP/Domain định danh duy nhất mà chip ESP32 sẽ gọi tới thông qua thư viện kết nối MQTT:
- **Địa chỉ Endpoint**: `a9vg0jjmuaycb-ats.iot.ap-southeast-1.amazonaws.com`
- Địa chỉ này sử dụng chứng chỉ mã hóa chuẩn **ATS (Amazon Trust Services)** để đảm bảo độ tin cậy kết nối và khả năng tương thích cao nhất với các thư viện kết nối trên chip ESP32.

![MQTT Endpoint](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-endpoint.png)
*Minh chứng 5.3.1.4: Địa chỉ Endpoint kết nối MQTT của hệ thống được ghi nhận tại mục Domain Configurations*

---

### 5. Luồng hoạt động kết nối và gửi dữ liệu (IoT Core Flow)
Để giúp hiểu rõ hơn cách thức vận hành của trạm kiểm soát IoT Core, dưới đây là sơ đồ mô tả tuần tự các bước từ khi thiết bị khởi động đến khi dữ liệu được truyền tải thành công lên đám mây:

{{< mermaid >}}
sequenceDiagram
    ESP32->>AWS IoT Core: Gửi kết nối TLS qua cổng 8883 (Client ID: esp-slot-01)
    AWS IoT Core->>AWS IoT Core: Xác thực bằng chứng chỉ X.509 & Policy
    AWS IoT Core-->>ESP32: Chấp nhận kết nối thành công (MQTT Connack)
    ESP32->>AWS IoT Core: Publish trạng thái đỗ xe (Topic: smart-parking/slots/update)
    AWS IoT Core->>AWS IoT Core: Định tuyến gói tin sang Lambda / Database
{{< /mermaid >}}
