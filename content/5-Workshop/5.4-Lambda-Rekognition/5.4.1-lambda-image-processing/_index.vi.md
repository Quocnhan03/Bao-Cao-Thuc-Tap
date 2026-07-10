---
title: "Lambda xử lý ảnh và kích hoạt sự kiện"
date: 2026-04-26
weight: 1
chapter: false
pre: " <b> 4.4.1. </b> "
---

Để tự động hóa quy trình khi có ảnh phương tiện mới tải lên hệ thống lưu trữ S3, một hàm tính toán không máy chủ **AWS Lambda** đã được xây dựng và cấu hình kích hoạt dựa trên sự kiện (Event-Driven Architecture).

---

### 1. Cấu hình Hàm Lambda & Trình kích hoạt (Trigger)
Hàm Lambda được triển khai có tên gọi là `smart-parking-detect-plate` chạy trên môi trường **Python 3.12**:
- **Trình kích hoạt (Trigger)**: Cấu hình liên kết trực tiếp với Amazon S3 Bucket `smart-parking-images-075647413376-ap-southeast-1-an`.
- **Loại sự kiện (Event Type)**: `s3:ObjectCreated:*` (Kích hoạt khi có bất kỳ file ảnh nào được tải lên thành công).
- **Quy tắc bộ lọc (Filters)**: 
  - Prefix: `parking/` (Chỉ kích hoạt khi ảnh nằm trong thư mục giám sát xe vào/ra).

![Cấu hình Lambda Trigger](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.1-lambda-code.png)
*Minh chứng 5.4.1.1: Hàm Lambda smart-parking-detect-plate liên kết với Trigger từ Amazon S3*

---

### 2. Thiết kế mã nguồn xử lý ảnh của Lambda
Khi sự kiện tải ảnh lên S3 xảy ra, một tài liệu JSON chứa thông tin về bucket và đường dẫn file ảnh (S3 Object Key) được gửi tới hàm Lambda dưới dạng tham số `event`. 

Dưới đây là cấu trúc mã nguồn chính của hàm Lambda (`lambda_function.py`) chịu trách nhiệm tiếp nhận sự kiện, gọi dịch vụ Rekognition để nhận diện biển số xe và ghi nhận lịch sử ra vào bãi đỗ:

```python
import json
import boto3
import urllib.parse
import re
from datetime import datetime

# Khởi tạo các AWS SDK Clients
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

# Khai báo các bảng dữ liệu DynamoDB
VEHICLE_HISTORY_TABLE = 'SmartParking_VehicleHistory'
SLOTS_TABLE = 'SmartParking_Slots'

def lambda_handler(event, context):
    # 1. Trích xuất thông tin file ảnh từ S3 Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. Gọi dịch vụ Amazon Rekognition nhận diện chữ viết trong ảnh
        response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
        
        # 3. Phân tích kết quả chữ để tìm biển số xe khớp định dạng
        text_detections = response.get('TextDetections', [])
        plate_number = extract_plate_number(text_detections)
        
        if not plate_number:
            print(f"Không phát hiện biển số xe hợp lệ trong file: {key}")
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'NO_PLATE_DETECTED', 'allowOpen': False})
            }
            
        # 4. Xác định chiều xe chạy (vào bãi hay ra bãi) dựa trên đường dẫn lưu trữ
        direction = 'IN' if 'parking/in/' in key else 'OUT'
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        
        # 5. Ghi lịch sử phương tiện vào bảng SmartParking_VehicleHistory
        history_table = dynamodb.Table(VEHICLE_HISTORY_TABLE)
        history_table.put_item(
            Item={
                'plate_number': plate_number,
                'timestamp': timestamp,
                'direction': direction,
                'image_url': f"https://{bucket}.s3-ap-southeast-1.amazonaws.com/{key}"
            }
        )
        
        # 6. Cập nhật trạng thái chỗ đỗ xe trong bảng SmartParking_Slots
        # (Ví dụ cấu hình mặc định cập nhật cho slot kiểm soát)
        slot_id = 'slot-01'
        slots_table = dynamodb.Table(SLOTS_TABLE)
        slots_table.update_item(
            Key={'slot_id': slot_id},
            UpdateExpression="SET occupied = :val",
            ExpressionAttributeValues={':val': True if direction == 'IN' else False}
        )
        
        # 7. Kiểm tra quyền mở cổng chắn (Barrier Gate)
        # Nếu biển số xe hợp lệ, cho phép mở cổng chắn tự động
        allow_open = True 
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'SUCCESS',
                'plate_number': plate_number,
                'direction': direction,
                'allowOpen': allow_open
            })
        }
        
    except Exception as e:
        print(f"Lỗi xử lý ảnh: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'ERROR', 'error': str(e), 'allowOpen': False})
        }

def extract_plate_number(text_detections):
    # Biểu thức chính quy tìm định dạng biển số xe Việt Nam phổ biến
    # Ví dụ: 29A12345, 30F99999, 51K1234
    plate_pattern = re.compile(r'^[0-9]{2}[A-Z][0-9]{4,5}$')
    
    for detection in text_detections:
        detected_text = detection.get('DetectedText', '').replace(" ", "").replace("-", "").replace(".", "")
        if plate_pattern.match(detected_text):
            return detected_text
            
    # Dự phòng nếu không khớp hoàn hảo, lấy dòng chữ có độ tin cậy cao nhất có cấu trúc số + chữ
    for detection in text_detections:
        text = detection.get('DetectedText', '').strip()
        if len(text) >= 7 and len(text) <= 10 and any(c.isdigit() for c in text) and any(c.isalpha() for c in text):
            return text.upper()
            
    return None
```
---

### 3. Nguyên lý Vận hành và Định tuyến
Sơ đồ tuần tự dưới đây làm rõ cách hàm Lambda này nhận thông tin từ S3 và điều phối dịch vụ xử lý:

{{< mermaid >}}
sequenceDiagram
    participant S3 as Amazon S3
    participant Lambda as AWS Lambda (detect-plate)
    participant Rekog as Amazon Rekognition
    participant Dynamo as Amazon DynamoDB
    
    S3->>Lambda: 1. Sự kiện s3:ObjectCreated (Đường dẫn ảnh)
    Lambda->>Rekog: 2. Yêu cầu phân tích chữ trong ảnh (DetectText)
    Rekog-->>Lambda: 3. Trả danh sách từ nhận diện được
    Lambda->>Lambda: 4. Regex phân tích và trích xuất Biển số xe
    Lambda->>Dynamo: 5. Ghi lịch sử xe vào SmartParking_VehicleHistory
    Lambda->>Dynamo: 6. Cập nhật trạng thái slot vào SmartParking_Slots
    Lambda-->>S3: 7. Hoàn tất xử lý (HTTP 200 OK)
{{< /mermaid >}}
