---
title: "Lambda Image Processing & Event Triggering"
date: 2026-04-26
weight: 1
chapter: false
pre: " <b> 4.4.1. </b> "
---

To automate the workflow when a new vehicle image is uploaded to the S3 storage system, a serverless **AWS Lambda** function was built and configured with event-driven triggering (Event-Driven Architecture).

---

### 1. Lambda Function & Trigger Configuration
The deployed Lambda function is named `smart-parking-detect-plate` and runs on the **Python 3.12** runtime:
- **Trigger**: Configured with a direct link to the Amazon S3 Bucket `smart-parking-images-075647413376-ap-southeast-1-an`.
- **Event Type**: `s3:ObjectCreated:*` (Triggered whenever any image file is successfully uploaded).
- **Filter Rules**: 
  - Prefix: `parking/` (Only triggers when images are in the vehicle entry/exit monitoring folder).

![Lambda Trigger Configuration](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.1-lambda-code.png)
*Figure 5.4.1.1: The smart-parking-detect-plate Lambda function linked to the Amazon S3 Trigger*

---

### 2. Lambda Image Processing Source Code Design
When an image upload event occurs on S3, a JSON document containing the bucket information and image file path (S3 Object Key) is sent to the Lambda function as the `event` parameter.

Below is the main source code structure of the Lambda function (`lambda_function.py`), which is responsible for receiving the event, calling the Rekognition service for license plate recognition, and recording the entry/exit history:

```python
import json
import boto3
import urllib.parse
import re
from datetime import datetime

# Initialize AWS SDK Clients
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

# Declare DynamoDB data tables
VEHICLE_HISTORY_TABLE = 'SmartParking_VehicleHistory'
SLOTS_TABLE = 'SmartParking_Slots'

def lambda_handler(event, context):
    # 1. Extract image file information from S3 Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. Call Amazon Rekognition service to detect text in the image
        response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
        
        # 3. Analyze text results to find a license plate matching the expected format
        text_detections = response.get('TextDetections', [])
        plate_number = extract_plate_number(text_detections)
        
        if not plate_number:
            print(f"No valid license plate detected in file: {key}")
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'NO_PLATE_DETECTED', 'allowOpen': False})
            }
            
        # 4. Determine vehicle direction (entering or exiting) based on the storage path
        direction = 'IN' if 'parking/in/' in key else 'OUT'
        timestamp = int(datetime.utcnow().timestamp() * 1000)
        
        # 5. Record vehicle history in the SmartParking_VehicleHistory table
        history_table = dynamodb.Table(VEHICLE_HISTORY_TABLE)
        history_table.put_item(
            Item={
                'plate_number': plate_number,
                'timestamp': timestamp,
                'direction': direction,
                'image_url': f"https://{bucket}.s3-ap-southeast-1.amazonaws.com/{key}"
            }
        )
        
        # 6. Update parking slot status in the SmartParking_Slots table
        # (Default configuration updates the controlled slot)
        slot_id = 'slot-01'
        slots_table = dynamodb.Table(SLOTS_TABLE)
        slots_table.update_item(
            Key={'slot_id': slot_id},
            UpdateExpression="SET occupied = :val",
            ExpressionAttributeValues={':val': True if direction == 'IN' else False}
        )
        
        # 7. Check barrier gate opening permission
        # If the license plate is valid, allow the barrier gate to open automatically
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
        print(f"Image processing error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'ERROR', 'error': str(e), 'allowOpen': False})
        }

def extract_plate_number(text_detections):
    # Regular expression to find common Vietnamese license plate formats
    # Examples: 29A12345, 30F99999, 51K1234
    plate_pattern = re.compile(r'^[0-9]{2}[A-Z][0-9]{4,5}$')
    
    for detection in text_detections:
        detected_text = detection.get('DetectedText', '').replace(" ", "").replace("-", "").replace(".", "")
        if plate_pattern.match(detected_text):
            return detected_text
            
    # Fallback if no perfect match: pick the highest-confidence text with a number+letter structure
    for detection in text_detections:
        text = detection.get('DetectedText', '').strip()
        if len(text) >= 7 and len(text) <= 10 and any(c.isdigit() for c in text) and any(c.isalpha() for c in text):
            return text.upper()
            
    return None
```
---

### 3. Operating Principle and Routing
The sequence diagram below illustrates how this Lambda function receives information from S3 and orchestrates the processing services:

{{< mermaid >}}
sequenceDiagram
    participant S3 as Amazon S3
    participant Lambda as AWS Lambda (detect-plate)
    participant Rekog as Amazon Rekognition
    participant Dynamo as Amazon DynamoDB
    
    S3->>Lambda: 1. s3:ObjectCreated event (Image path)
    Lambda->>Rekog: 2. Request text analysis in image (DetectText)
    Rekog-->>Lambda: 3. Return list of recognized words
    Lambda->>Lambda: 4. Regex analysis and license plate extraction
    Lambda->>Dynamo: 5. Write vehicle history to SmartParking_VehicleHistory
    Lambda->>Dynamo: 6. Update slot status in SmartParking_Slots
    Lambda-->>S3: 7. Processing complete (HTTP 200 OK)
{{< /mermaid >}}
