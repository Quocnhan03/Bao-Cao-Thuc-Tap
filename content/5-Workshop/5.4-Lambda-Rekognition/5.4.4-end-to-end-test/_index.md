---
title: "Vehicle Recognition Flow Testing (End-to-End Test)"
date: 2026-04-26
weight: 4
chapter: false
pre: " <b> 4.4.4. </b> "
---

To evaluate the accuracy and performance of the automatic recognition system, a comprehensive End-to-End Test was conducted by simulating vehicles entering the parking lot (IN direction) and exiting the parking lot (OUT direction), thereby verifying the coordinated operation of Amazon S3, AWS Lambda, Amazon Rekognition, and Amazon DynamoDB.

---

### 1. Vehicle Entry Test (IN Flow Test)

#### 1.1. Actual Vehicle Image as Input Data
A photograph of a black Mercedes at the entry gate was used to test the system's text recognition capability:

![Mercedes test image](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-mercedes-car.jpg)
*Figure 5.4.4.1: Image of a Mercedes with license plate 30E-922.91 used as input data for the recognition flow*

#### 1.2. Uploading the Image to Amazon S3
The Mercedes image file was uploaded to the entry gate folder partition on S3 (`parking/in/`) to trigger the processing event:

![Upload image to S3 entry gate](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-s3-upload.png)
*Figure 5.4.4.2: The mercedes.jpg image file successfully uploaded to the directory s3://smart-parking-images-075647413376-ap-southeast-1-an/parking/in/*

#### 1.3. Result Record Automatically Created on Amazon DynamoDB
After the image was pushed to S3, the event automatically triggered the Lambda processing function. The result record in the `SmartParking_VehicleHistory` table on the AWS Console confirms a successful entry event:

![DynamoDB test result for entry](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-dynamodb-record.png)
*Figure 5.4.4.3: The event record for vehicle 30E-922.91 entering the parking lot (IN) was automatically created successfully in DynamoDB*

---

### 2. Vehicle Exit Test (OUT Flow Test)

#### 2.1. Uploading Image to the S3 Exit Folder (parking/out/) & DynamoDB Result Record
Similar to the entry flow, to test the exit flow, the Mercedes image file was uploaded to the exit gate folder partition (`parking/out/`). The event automatically triggered the Lambda function to extract the license plate and record the vehicle exit event (OUT) in the database:

![Vehicle exit test](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.4-s3-dynamodb-out.png)
*Figure 5.4.4.4: Successful upload of mercedes.jpg to the exit gate (top) and the corresponding vehicle exit event (OUT) record saved in DynamoDB (bottom)*

---

### 3. Actual Results Analysis
Based on the data evidence collected from the DynamoDB database in both the vehicle entry and exit scenarios:
- **OCR accuracy**: Amazon Rekognition successfully analyzed the Mercedes vehicle image and extracted the license plate as the continuous character string `30E92291` with a high confidence score.
- **Automatic vehicle flow classification**:
  - **Vehicle entry (IN)**: Since the file was located in the `parking/in/` directory, the `direction` attribute was saved as `IN` and the `allow_open` field was set to `true` to send an automatic barrier gate opening signal for the vehicle to enter the parking lot.
  - **Vehicle exit (OUT)**: Since the file was located in the `parking/out/` directory, the `direction` attribute was correctly saved as `OUT` to record the vehicle departure event and calculate the parking duration.
- **Display formatting**: The string processing algorithm in Lambda correctly reformatted the raw string `30E92291` into the standard display format with hyphens and dots as `30E-922.91` (stored in the `display_plate_number` attribute) for visual presentation on the client application.
- **Processing latency**: The entire process from image upload to S3 until the record appeared in DynamoDB took less than **1.5 seconds**, meeting the real-time operational requirements at the checkpoint station.
