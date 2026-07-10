---
title: "ESP32 Hardware Programming and Configuration"
date: 2026-04-26
weight: 6
chapter: false
pre: " <b> 4.6. </b> "
---

This chapter presents a detailed account of the wiring diagrams and firmware source code for controlling the edge hardware devices. The system is divided into two independent processing zones using ESP32 microcontrollers running on the **ESP-IDF** platform combined with the FreeRTOS library to optimize real-time performance.

---

### 1. Entry/Exit Gate Control Station (ESP32-CAM & Gate Control)

#### 1.1. Hardware Wiring Diagram
The gate control device uses an **ESP32-CAM** development board with an integrated OV2640 camera, connected to an E18-D80NK infrared proximity sensor for detecting vehicles stopped in front of the gate barrier, and controls an SG90 servo motor to open/close the barrier.

![Gate Wiring Diagram](/images/2-Proposal/1.sơ%20đồ%20đấu%20dây%20cổng.png)
*Figure 5.6.1: Component pin connection diagram at the entry/exit gate control station*

##### Detailed Analysis of the Entry/Exit Gate Wiring Diagram:
1. **System Power Supply**: The system uses a central **5V DC (4A–5A)** power supply to provide sufficient current for stable SG90 servo motor operation and to power the ESP32-CAM microcontroller (connected to the `5V` pin). The entire system shares a common ground (**GND**).
2. **E18-D80NK Infrared Proximity Sensor**:
   - The Brown wire connects directly to the positive `+5V` power supply.
   - The Blue wire connects to the common `GND`.
   - The Black signal wire outputs a voltage level of `5V` (High when no object is detected and Low when an obstacle is detected). This signal cannot be connected directly to the ESP32-CAM because the maximum GPIO operating voltage on the ESP32 chip is only `3.3V`.
3. **Logic Level Shifter Circuit (5V -> 3.3V)**:
   - **High-Voltage Side (HV Side)**: The `HV` pin connects to the `5V` supply, the `GND` pin connects to ground. The `HV1` signal pin receives the `5V` input signal from the Black wire of the E18-D80NK sensor.
   - **Low-Voltage Side (LV Side)**: The `LV` pin connects to the `3V3` output from the ESP32-CAM board as the reference voltage. The corresponding `LV1` signal pin outputs a safe stepped-down `3.3V` voltage level and connects to **GPIO 13** (`IO13`) of the ESP32-CAM.
4. **SG90 Servo Motor**:
   - The Red power wire connects directly to the system's `+5V` positive supply to provide sufficient mechanical torque.
   - The Brown wire connects to the common `GND`.
   - The Orange control wire receives a PWM signal at `50Hz` frequency generated from **GPIO 14** (`IO14`) of the ESP32-CAM.

---

#### 1.2. Core Gate Control Source Code (`main.c`)
The ESP32-CAM board performs the following tasks: reads the proximity sensor with stable detection over 1.5 seconds, captures a vehicle photo, sends an HTTP GET request to obtain a Presigned URL from AWS Lambda, then uploads the JPEG image binary data to Amazon S3 via an HTTP PUT method. Finally, it performs polling to receive the `allowOpen` signal from the database to control the servo barrier raise/lower action.

##### Code segment for requesting S3 Presigned URL and uploading vehicle image:
```c
// Function to call Lambda to get S3 Presigned URL and random image filename
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

// Function to upload JPEG image data to S3 via Presigned URL using HTTP PUT
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
        ESP_LOGI("S3_UPLOAD", "Successfully uploaded image to S3 Bucket");
        return ESP_OK;
    }
    return ESP_FAIL;
}
```

##### Code segment for controlling SG90 servo rotation angle (Open/Close gate barrier):
```c
// Control servo motor PWM pulse using ESP-IDF LEDC Driver
static void servo_write_angle(int angle)
{
    if (angle < 0) angle = 0;
    if (angle > 180) angle = 180;

    // Convert rotation angle 0-180 degrees to pulse width (500us - 2500us)
    uint32_t pulse_us = 500 + ((2000) * angle / 180);
    uint32_t max_duty = (1 << 16) - 1;
    uint32_t duty = (uint32_t)((uint64_t)pulse_us * max_duty * 50 / 1000000);

    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_2, duty);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_2);
}

// Function to gradually open the gate and close it after 5 seconds for mechanical safety
static void gate_open_close(void)
{
    // Gradually open the barrier gate to 90 degrees
    for (int angle = 0; angle <= 90; angle += 3) {
        servo_write_angle(angle);
        vTaskDelay(pdMS_TO_TICKS(25));
    }
    vTaskDelay(pdMS_TO_TICKS(5000)); // Keep gate open for 5 seconds

    // Gradually close the gate back to 0 degrees
    for (int angle = 90; angle >= 0; angle -= 3) {
        servo_write_angle(angle);
        vTaskDelay(pdMS_TO_TICKS(25));
    }
}
```

---

### 2. Parking Space Monitoring System (ESP32-S3 & Ultrasonic Sensors)

#### 2.1. Hardware Wiring Diagram
The **ESP32-S3 DevKitC** controller board simultaneously monitors 6 parking spaces through 6 independent HC-SR04 ultrasonic sensors. The Echo signal (5V) from the sensors is routed through a CD74HC4050 level-shifting buffer IC to step down the voltage to 3.3V, preventing damage to the ESP32-S3 input GPIO pins.

![Parking Lot Wiring Diagram](/images/2-Proposal/2.sơ%20đồ%20dây%20bãi%20xe.png)
*Figure 5.6.2: Wiring diagram showing component pin connections and CD74HC4050 buffer IC for 6 parking space sensors*

##### Detailed Analysis of the Parking Lot Wiring Diagram:
1. **Power Supply**: All 6 HC-SR04 ultrasonic sensors and the ESP32-S3 microcontroller operate on a **5V DC (1A–2A)** power rail.
2. **Ultrasonic Sensor Trigger Principle (Trig)**:
   - The **Trig** pins of all 6 ultrasonic sensors (HC-SR04) are physically wired in parallel to a common trigger line.
   - This common Trig line connects to **GPIO 5** of the ESP32-S3. This design maximizes pin resource savings on the microcontroller — instead of requiring 6 independent pins, the system uses only 1 GPIO pin to simultaneously trigger all 6 sensors.
3. **Echo Logic Level Shifting and Protection Circuit via CD74HC4050 IC**:
   - The **Echo** pins of the ultrasonic sensors return a `5V` voltage level corresponding to the ultrasonic wave reflection time. Since the ESP32-S3 can only accept a maximum of `3.3V` on its GPIO pins, direct connection would damage the microcontroller chip.
   - The system integrates a **CD74HC4050 (DIP-16)** logic level shifting buffer IC containing 6 independent buffer channels. The reference `VCC` pin (Pin 1) of the IC is connected to the `3V3` output of the ESP32-S3. Pin 8 of the IC is connected to `GND`.
   - The Echo signal level conversion mapping from 5V to 3.3V is described in the following table:

| Sensor Name / Position | Sensor Echo Pin (5V) | CD74HC4050 IC Input Pin | CD74HC4050 IC Output Pin (3.3V) | Target GPIO Pin on ESP32-S3 |
| :--- | :---: | :---: | :---: | :---: |
| **A1 - HC-SR04** | Echo A1 | Pin 3 (`1A`) | Pin 2 (`1Y`) | **GPIO 6** |
| **A2 - HC-SR04** | Echo A2 | Pin 5 (`2A`) | Pin 4 (`2Y`) | **GPIO 7** |
| **A3 - HC-SR04** | Echo A3 | Pin 7 (`3A`) | Pin 6 (`3Y`) | **GPIO 10** |
| **B1 - HC-SR04** | Echo B1 | Pin 9 (`4A`) | Pin 10 (`4Y`) | **GPIO 11** |
| **B2 - HC-SR04** | Echo B2 | Pin 11 (`5A`) | Pin 12 (`5Y`) | **GPIO 1** |
| **B3 - HC-SR04** | Echo B3 | Pin 14 (`6A`) | Pin 15 (`6Y`) | **GPIO 2** |

---

#### 2.2. Core Ultrasonic Sensor Reading Source Code (`main.c`)
The device sends a 10-microsecond trigger pulse through the Trig pin, measures the high-level echo duration on each sensor's Echo pin, applies measurement noise filtering (averaging 3 consecutive readings), updates a 2-second debounce filter, and sends parking space status update events to the API server.

##### Code segment for HC-SR04 ultrasonic distance measurement:
```c
// Measure ultrasonic echo pulse duration to calculate distance (cm)
static float read_distance_cm(gpio_num_t echo_pin)
{
    // 1. Send a 10us trigger pulse
    gpio_set_level(GPIO_NUM_5, 0);
    esp_rom_delay_us(2);
    gpio_set_level(GPIO_NUM_5, 1);
    esp_rom_delay_us(10);
    gpio_set_level(GPIO_NUM_5, 0);

    // 2. Wait for Echo to go HIGH (Timeout 30ms)
    int64_t start_time = esp_timer_get_time();
    int64_t timeout = start_time + 30000;
    while (gpio_get_level(echo_pin) == 0) {
        if (esp_timer_get_time() > timeout) return -1.0f;
    }
    int64_t echo_start = esp_timer_get_time();

    // 3. Measure how long the Echo pin stays HIGH
    timeout = echo_start + 30000;
    while (gpio_get_level(echo_pin) == 1) {
        if (esp_timer_get_time() > timeout) return -1.0f;
    }
    int64_t echo_end = esp_timer_get_time();

    // 4. Calculate distance based on speed of sound: s = t * 343m/s / 2
    int64_t duration = echo_end - echo_start;
    return (float)duration / 58.2f; // Return distance in centimeters
}
```

##### Code segment for JSON data packaging and status update via HTTP POST:
```c
// Function to send changed parking space status to the local API Server
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

### 3. Hardware and Software Noise Reduction Principles
To address measurement errors caused by acoustic wave reflections or electromagnetic interference in industrial/parking lot environments:
1. **Sensor Noise Filtering (Software Filtering)**: In each measurement cycle, the device takes 3 consecutive readings spaced 30 milliseconds apart. The final distance value is calculated as the arithmetic average of the valid readings.
2. **State Change Debounce Algorithm**: The ultrasonic sensor state indicating vehicle presence (distance below the `3.5cm` threshold) or vacancy must remain stable continuously for a minimum of **2 seconds** before the device officially confirms and sends an API status update, preventing false triggers from temporary wave noise or objects passing through momentarily.
3. **Periodic Heartbeat Mechanism**: Every 5 minutes, if no state change has occurred, the device automatically sends a status update message with the current state to the Cloud to indicate that the sensor system is still online and operating normally.
