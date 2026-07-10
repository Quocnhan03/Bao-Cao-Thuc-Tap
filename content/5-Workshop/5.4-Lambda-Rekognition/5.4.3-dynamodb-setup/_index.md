---
title: "DynamoDB Database Design"
date: 2026-04-26
weight: 3
chapter: false
pre: " <b> 4.4.3. </b> "
---

To store the real-time operational status of parking slots and the vehicle entry/exit history, the NoSQL database service **Amazon DynamoDB** is used as the system's central data store.

---

### 1. System Database Tables
The system provisions 3 primary database tables on Amazon DynamoDB to manage information:
- `SmartParking_Slots`: Stores the information and occupied/available status of each parking slot.
- `SmartParking_VehicleHistory`: Stores detailed logs of every vehicle entry/exit event at the parking lot.
- `SmartParking_GateCommands`: Stores the history of barrier gate control commands.

![DynamoDB Tables List](/images/5-Workshop/5.4-Lambda-Rekognition/5.4.3-dynamodb.png)
*Figure 5.4.3.1: The Parking IoT system's database tables on the Amazon DynamoDB management console*

---

### 2. Table Schema Design

#### 2.1. Parking Slot Status Table (`SmartParking_Slots`)
This table manages the list of parking slots and their current occupied/available status.
- **Partition Key**: `slot_id` (Data type: String - S)
- **Sample attribute structure**:
```json
{
  "slot_id": "slot-01",
  "occupied": true,
  "last_updated": 1783683112000
}
```

#### 2.2. Vehicle History Table (`SmartParking_VehicleHistory`)
This table records all vehicle entry/exit events at the parking lot, supporting reconciliation and display on the user interface.
- **Partition Key**: `plate_number` (Data type: String - S, license plate written as a continuous string without separators).
- **Sort Key**: `timestamp` (Data type: Number - N, Unix time in milliseconds).
- **Detailed configured attributes**:
  - `allow_open` (Boolean): Permission to open the barrier (True/False).
  - `bucket` (String): S3 bucket storing the image.
  - `camera_id` (String): Identifier of the capturing camera.
  - `confidence` (Number): Confidence score of the text recognition algorithm (percentage).
  - `created_at` (String): Human-readable timestamp format (`YYYY-MM-DD HH:MM:SS`).
  - `device_id` (String): Identifier of the gate controller device.
  - `direction` (String): Direction of movement (`IN` or `OUT`).
  - `display_plate_number` (String): Formatted license plate for display (e.g., `29A-179.38`).
  - `event_id` (String): Unique ID generated for the event.
  - `image_key` (String): Image file path on S3.

Actual data schema stored in the database:
```json
{
  "plate_number": "29A17938",
  "timestamp": 1782032316749,
  "allow_open": true,
  "bucket": "smart-parking-images-075647413376-ap-southeast-1-an",
  "camera_id": "gate-in-01",
  "confidence": 98.23297882080078,
  "created_at": "2026-06-21 14:05:16",
  "device_id": "gate-in-01",
  "direction": "IN",
  "display_plate_number": "29A-179.38",
  "event_id": "evt_29A17938_1782032316",
  "image_key": "parking/in/29A17938.jpg"
}
```

#### 2.3. Gate Command Table (`SmartParking_GateCommands`)
This table stores barrier gate control commands sent from the central control system or from manual button presses on the web interface.
- **Partition Key**: `device_id` (Data type: String - S, gate controller identifier).
- **Sort Key**: `created_at` (Data type: Number - N, command dispatch timestamp).
- **Sample attribute structure**:
```json
{
  "device_id": "gate-controller-01",
  "created_at": 1783683112000,
  "command": "OPEN",
  "status": "PENDING"
}
```

---

### 3. Rationale for Choosing This Solution
**Amazon DynamoDB** was selected as the project's database due to its technical characteristics that align well with the IoT model:
1. **High performance and low latency**: DynamoDB provides read/write response times under 10 milliseconds, enabling the checkpoint station to process barrier gate openings almost instantly when license plate analysis results are available.
2. **Fully Serverless architecture**: No database server administration is required; storage resources scale automatically and billing is based on actual read/write request volume (On-demand capacity mode).
3. **Flexible Schema-less model**: IoT data attributes (such as license plate bounding box coordinates or auxiliary RFID card numbers) can be easily added or removed without performing complex database migrations.
