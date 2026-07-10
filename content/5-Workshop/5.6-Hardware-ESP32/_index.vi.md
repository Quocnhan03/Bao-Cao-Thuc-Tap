---
title: "Lập trình và Cấu hình Phần cứng ESP32"
date: 2026-04-26
weight: 6
chapter: false
pre: " <b> 4.6. </b> "
---

Chương này trình bày chi tiết về sơ đồ kết nối và mã nguồn lập trình điều khiển các thiết bị phần cứng biên (Edge Devices). Hệ thống phân tách thành hai khu vực xử lý độc lập sử dụng vi điều khiển ESP32 chạy trên nền tảng **ESP-IDF** kết hợp thư viện FreeRTOS để tối ưu hiệu năng thời gian thực.

---

### 1. Trạm kiểm soát cổng ra/vào (ESP32-CAM & Gate Control)

#### 1.1. Sơ đồ đấu nối dây phần cứng
Thiết bị kiểm soát cổng sử dụng board mạch **ESP32-CAM** tích hợp camera OV2640, liên kết với cảm biến tiệm cận hồng ngoại E18-D80NK để phát hiện xe dừng trước cổng chắn, và điều khiển động cơ Servo SG90 để đóng/mở barie.

![Sơ đồ đấu dây cổng](/images/2-Proposal/1.sơ%20đồ%20đấu%20dây%20cổng.png)
*Minh chứng 5.6.1: Sơ đồ kết nối chân linh kiện tại trạm kiểm soát cổng vào/ra*

##### Phân tích chi tiết sơ đồ kết nối cổng vào/ra:
1. **Nguồn điện hệ thống**: Hệ thống sử dụng một bộ nguồn trung tâm **5V DC (4A - 5A)** để cấp dòng điện đủ lớn cho động cơ Servo SG90 hoạt động ổn định và cấp nguồn cho vi điều khiển ESP32-CAM (nối vào chân `5V`). Toàn bộ hệ thống được nối chung cực âm (**GND**).
2. **Cảm biến tiệm cận hồng ngoại E18-D80NK**:
   - Dây màu Nâu nối trực tiếp với nguồn điện dương `+5V`.
   - Dây màu Xanh nối với cực âm chung `GND`.
   - Dây tín hiệu màu Đen xuất ra mức điện áp `5V` (High khi không có vật và Low khi phát hiện vật cản). Tín hiệu này không được nối trực tiếp vào ESP32-CAM vì điện áp vận hành của GPIO trên chip ESP32 tối đa chỉ là `3.3V`.
3. **Mạch chuyển đổi mức logic (Level Shifter 5V -> 3.3V)**:
   - **Phía điện áp cao (HV Side)**: Chân `HV` nối với nguồn `5V`, chân `GND` nối cực âm. Chân tín hiệu `HV1` nhận tín hiệu đầu vào `5V` từ dây Đen của cảm biến E18-D80NK.
   - **Phía điện áp thấp (LV Side)**: Chân `LV` nối với ngõ ra `3V3` lấy từ board ESP32-CAM để làm điện áp tham chiếu. Chân tín hiệu tương ứng `LV1` xuất ra mức điện áp hạ áp an toàn `3.3V` và nối vào chân **GPIO 13** (`IO13`) của ESP32-CAM.
4. **Động cơ Servo SG90**:
   - Dây nguồn màu Đỏ kết nối trực tiếp với nguồn dương `+5V` của hệ thống để có đủ lực kéo cơ học.
   - Dây màu Nâu nối với cực âm chung `GND`.
   - Dây điều khiển màu Cam nhận tín hiệu xung PWM tần số `50Hz` phát ra từ chân **GPIO 14** (`IO14`) của ESP32-CAM.

---

#### 1.2. Mã nguồn cốt lõi điều khiển cổng vào/ra (`main.c`)
Board ESP32-CAM thực hiện nhiệm vụ: đo cảm biến tiệm cận ổn định trong 1.5 giây, chụp ảnh xe, gửi yêu cầu HTTP GET lấy Presigned URL từ AWS Lambda, sau đó tải dữ liệu nhị phân ảnh JPEG lên Amazon S3 bằng phương thức HTTP PUT. Cuối cùng, thực hiện thăm dò ý kiến (Polling) nhận tín hiệu `allowOpen` từ cơ sở dữ liệu để điều khiển Servo nâng hạ barie.

##### Đoạn code yêu cầu lấy S3 Presigned URL và tải ảnh xe:
```c
// Hàm gọi Lambda lấy S3 Presigned URL và tên file ảnh ngẫu nhiên
static presigned_result_t get_presigned_data(void)
{
    presigned_result_t result = {.upload_url = NULL, .file_name = NULL};
    char *response_buffer = calloc(1, 12000);
    http_response_t response = {.buffer = response_buffer, .length = 0, .max_len = 12000};

    esp_http_client_config_t config = {
        .url = "https://4q3ukqk4mzidpcqtdmbwyvjhha0kjtbg.lambda-url.ap-southeast-1.on.aws/",
        .method = HTTP_METHOD_GET,
        .event_handler = http_event_handler,
        .user_data = &response,
        .timeout_ms = 60000,
        .crt_bundle_attach = esp_crt_bundle_attach,
    };

    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_err_t err = esp_http_client_perform(client);
    int status_code = esp_http_client_get_status_code(client);
    esp_http_client_cleanup(client);

    if (err == ESP_OK && status_code == 200) {
        cJSON *root = cJSON_Parse(response_buffer);
        cJSON *url_item = cJSON_GetObjectItem(root, "uploadUrl");
        cJSON *file_item = cJSON_GetObjectItem(root, "fileName");
        if (url_item && file_item) {
            result.upload_url = strdup(url_item->valuestring);
            result.file_name = strdup(file_item->valuestring);
        }
        cJSON_Delete(root);
    }
    free(response_buffer);
    return result;
}

// Hàm tải dữ liệu ảnh JPEG lên S3 thông qua Presigned URL bằng HTTP PUT
static esp_err_t upload_image_to_s3(const char *upload_url, uint8_t *image_data, size_t image_len)
{
    esp_http_client_config_t config = {
        .url = upload_url,
        .method = HTTP_METHOD_PUT,
        .timeout_ms = 60000,
        .crt_bundle_attach = esp_crt_bundle_attach,
    };
    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_http_client_set_header(client, "Content-Type", "image/jpeg");

    esp_err_t err = esp_http_client_open(client, image_len);
    int written = esp_http_client_write(client, (const char *) image_data, image_len);
    esp_http_client_fetch_headers(client);
    int status_code = esp_http_client_get_status_code(client);
    
    esp_http_client_close(client);
    esp_http_client_cleanup(client);

    if (status_code == 200 || status_code == 204) {
        ESP_LOGI("S3_UPLOAD", "Upload thành công ảnh lên S3 Bucket");
        return ESP_OK;
    }
    return ESP_FAIL;
}
```

##### Đoạn code điều khiển góc quay của Servo SG90 (Đóng/Mở cổng chắn):
```c
// Điều khiển xung PWM của động cơ Servo bằng Driver LEDC ESP-IDF
static void servo_write_angle(int angle)
{
    if (angle < 0) angle = 0;
    if (angle > 180) angle = 180;

    // Chuyển đổi góc quay 0-180 độ thành độ rộng xung (500us - 2500us)
    uint32_t pulse_us = 500 + ((2000) * angle / 180);
    uint32_t max_duty = (1 << 16) - 1;
    uint32_t duty = (uint32_t)((uint64_t)pulse_us * max_duty * 50 / 1000000);

    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_2, duty);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_2);
}

// Hàm mở cổng từ từ và đóng lại sau 5 giây để đảm bảo an toàn cơ học
static void gate_open_close(void)
{
    // Mở từ từ cổng chắn lên 90 độ
    for (int angle = 0; angle <= 90; angle += 3) {
        servo_write_angle(angle);
        vTaskDelay(pdMS_TO_TICKS(25));
    }
    vTaskDelay(pdMS_TO_TICKS(5000)); // Giữ cổng mở trong 5 giây

    // Đóng cổng từ từ về 0 độ
    for (int angle = 90; angle >= 0; angle -= 3) {
        servo_write_angle(angle);
        vTaskDelay(pdMS_TO_TICKS(25));
    }
}
```

---

### 2. Hệ thống giám sát vị trí đỗ (ESP32-S3 & Ultrasonic Sensors)

#### 2.1. Sơ đồ đấu nối dây phần cứng
Board điều khiển **ESP32-S3 DevKitC** giám sát cùng lúc 6 vị trí đỗ xe thông qua 6 cảm biến siêu âm HC-SR04 độc lập. Tín hiệu Echo (5V) từ cảm biến được định hướng qua IC đệm hạ áp CD74HC4050 về mức điện áp 3.3V để tránh làm hỏng các chân GPIO đầu vào của ESP32-S3.

![Sơ đồ đấu dây bãi xe](/images/2-Proposal/2.sơ%20đồ%20dây%20bãi%20xe.png)
*Minh chứng 5.6.2: Sơ đồ đấu nối dây chân linh kiện và IC đệm CD74HC4050 cho 6 cảm biến vị trí đỗ xe*

##### Phân tích chi tiết sơ đồ kết nối bãi đỗ xe:
1. **Nguồn cấp điện**: Toàn bộ 6 cảm biến siêu âm HC-SR04 và vi điều khiển ESP32-S3 hoạt động trên đường ray điện áp **5V DC (1A - 2A)**.
2. **Nguyên lý kích hoạt cảm biến siêu âm (Trig)**:
   - Các chân **Trig** của tất cả 6 cảm biến siêu âm (HC-SR04) được đấu song song vật lý nối về một đường dây chung kích phát.
   - Đường dây Trig chung này kết nối vào chân **GPIO 5** của ESP32-S3. Thiết kế này giúp tiết kiệm tối đa tài nguyên chân trên vi điều khiển, thay vì phải dùng 6 chân độc lập, hệ thống chỉ cần dùng duy nhất 1 chân GPIO phát xung kích hoạt cùng lúc cho 6 cảm biến.
3. **Mạch bảo vệ và chuyển mức logic Echo qua IC CD74HC4050**:
   - Các chân **Echo** của cảm biến siêu âm phản hồi mức điện áp `5V` tương ứng với khoảng thời gian sóng âm phản xạ. Vì ESP32-S3 chỉ nhận tín hiệu tối đa `3.3V` trên các chân GPIO, việc đấu nối trực tiếp sẽ gây nguy hại cho chip vi điều khiển.
   - Hệ thống tích hợp IC đệm chuyển đổi mức logic **CD74HC4050 (DIP-16)** chứa 6 kênh đệm độc lập. Chân nguồn tham chiếu `VCC` (chân 1) của IC được nối với ngõ ra `3V3` của ESP32-S3. Chân 8 của IC nối cực âm `GND`.
   - Cơ chế ánh xạ chuyển đổi tín hiệu Echo từ 5V về 3.3V được mô tả qua bảng sau:

| Tên cảm biến / Vị trí | Chân Echo cảm biến (5V) | Chân Input IC CD74HC4050 | Chân Output IC CD74HC4050 (3.3V) | Chân GPIO đích trên ESP32-S3 |
| :--- | :---: | :---: | :---: | :---: |
| **A1 - HC-SR04** | Echo A1 | Chân 3 (`1A`) | Chân 2 (`1Y`) | **GPIO 6** |
| **A2 - HC-SR04** | Echo A2 | Chân 5 (`2A`) | Chân 4 (`2Y`) | **GPIO 7** |
| **A3 - HC-SR04** | Echo A3 | Chân 7 (`3A`) | Chân 6 (`3Y`) | **GPIO 10** |
| **B1 - HC-SR04** | Echo B1 | Chân 9 (`4A`) | Chân 10 (`4Y`) | **GPIO 11** |
| **B2 - HC-SR04** | Echo B2 | Chân 11 (`5A`) | Chân 12 (`5Y`) | **GPIO 1** |
| **B3 - HC-SR04** | Echo B3 | Chân 14 (`6A`) | Chân 15 (`6Y`) | **GPIO 2** |

---

#### 2.2. Mã nguồn cốt lõi đọc cảm biến siêu âm (`main.c`)
Thiết bị thực hiện gửi xung kích hoạt 10 micro giây thông qua chân Trig, đo thời gian phản hồi mức cao trên chân Echo của từng cảm biến, lọc nhiễu đo đạc (lọc trung bình 3 lần đo), cập nhật bộ lọc Debounce 2 giây và gửi sự kiện cập nhật trạng thái ô đỗ về máy chủ API.

##### Đoạn code đo khoảng cách siêu âm HC-SR04:
```c
// Đo thời gian xung phản hồi siêu âm để tính khoảng cách (cm)
static float read_distance_cm(gpio_num_t echo_pin)
{
    // 1. Phát xung kích hoạt Trig dài 10us
    gpio_set_level(GPIO_NUM_5, 0);
    esp_rom_delay_us(2);
    gpio_set_level(GPIO_NUM_5, 1);
    esp_rom_delay_us(10);
    gpio_set_level(GPIO_NUM_5, 0);

    // 2. Chờ Echo bắt đầu lên mức cao (Timeout 30ms)
    int64_t start_time = esp_timer_get_time();
    int64_t timeout = start_time + 30000;
    while (gpio_get_level(echo_pin) == 0) {
        if (esp_timer_get_time() > timeout) return -1.0f;
    }
    int64_t echo_start = esp_timer_get_time();

    // 3. Đo thời gian chân Echo giữ mức cao
    timeout = echo_start + 30000;
    while (gpio_get_level(echo_pin) == 1) {
        if (esp_timer_get_time() > timeout) return -1.0f;
    }
    int64_t echo_end = esp_timer_get_time();

    // 4. Tính khoảng cách dựa trên vận tốc âm thanh: s = t * 343m/s / 2
    int64_t duration = echo_end - echo_start;
    return (float)duration / 58.2f; // Trả về khoảng cách xăng-ti-mét
}
```

##### Đoạn code đóng gói dữ liệu JSON và cập nhật trạng thái qua HTTP POST:
```c
// Hàm gửi trạng thái chỗ đỗ thay đổi về API Server cục bộ
static void send_status_update(const char *slot_id, bool occupied, float distance)
{
    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "device_id", "esp-slot-01");
    cJSON_AddStringToObject(root, "slot_id", slot_id);
    cJSON_AddBoolToObject(root, "occupied", occupied);
    cJSON_AddNumberToObject(root, "distance", distance > 0 ? (double)distance : -1.0);

    char *json_body = cJSON_PrintUnformatted(root);
    cJSON_Delete(root);

    char *response_buffer = calloc(1, 256);
    http_response_t response = {.buffer = response_buffer, .length = 0, .max_len = 256};

    esp_http_client_config_t config = {
        .url = "http://172.20.10.3:8089/device/slot/update",
        .method = HTTP_METHOD_POST,
        .event_handler = http_event_handler,
        .user_data = &response,
        .timeout_ms = 5000,
    };

    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_http_client_set_header(client, "Content-Type", "application/json");
    esp_http_client_set_header(client, "x-api-key", "smart_parking_slot_key_123");
    esp_http_client_set_post_field(client, json_body, strlen(json_body));

    esp_err_t err = esp_http_client_perform(client);
    int status_code = esp_http_client_get_status_code(client);
    
    esp_http_client_cleanup(client);
    free(json_body);
    free(response_buffer);
}
```
---

### 3. Nguyên lý chống nhiễu phần cứng và phần mềm
Để khắc phục các sai số do phản xạ sóng âm hoặc nhiễu điện từ trong môi trường công nghiệp/bãi đỗ:
1. **Lọc nhiễu cảm biến (Software Filtering)**: Cứ mỗi chu kỳ đo, thiết bị thực hiện đo 3 lần liên tiếp cách nhau 30 mili-giây. Giá trị khoảng cách cuối cùng được tính bằng trung bình cộng của các lần đo hợp lệ.
2. **Thuật toán Debounce thay đổi trạng thái**: Trạng thái cảm biến siêu âm phát hiện có xe (khoảng cách dưới ngưỡng `3.5cm`) hoặc trống phải duy trì ổn định liên tục tối thiểu trong **2 giây** thì thiết bị mới chính thức xác nhận và gửi API cập nhật, tránh trường hợp nhiễu sóng hoặc vật cản di chuyển ngang qua tạm thời.
3. **Cơ chế Heartbeat định kỳ**: Cứ sau 5 phút nếu không có thay đổi trạng thái, thiết bị vẫn tự động gửi bản tin cập nhật trạng thái hiện tại lên Cloud nhằm thông báo hệ thống cảm biến vẫn đang trực tuyến và hoạt động bình thường.
