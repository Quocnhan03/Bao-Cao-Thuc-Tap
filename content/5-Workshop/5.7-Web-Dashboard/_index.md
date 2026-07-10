---
title: "System Administration Web Dashboard"
date: 2026-04-26
weight: 7
chapter: false
pre: " <b> 4.7. </b> "
---

To support visual monitoring, statistics, and parking lot operations, a comprehensive administration Web Dashboard was built using **React/Next.js** technology combined with modern design libraries, distributed via **Amazon CloudFront** (`https://d3imp0j8sdburp.cloudfront.net/`).

The system is divided into two Portals operating in parallel based on user authorization from Amazon Cognito: **Admin Portal** and **User Portal**.

---

### 1. AWS Infrastructure Integration Architecture of the Web Dashboard
To ensure scalability, high security, and low response times, the Web Dashboard does not use traditional servers but is deployed using a **Serverless** architecture on the AWS cloud.

{{< mermaid >}}
graph TD
    User[Customer / Admin] -->|1. HTTPS| CF[Amazon CloudFront]
    CF -->|Web distribution| S3Web[Amazon S3 Static Hosting]
    S3Web -->|Load React App to browser| WebApp[React Web Dashboard]
    
    WebApp -->|2. Login / Get JWT| Cognito[Amazon Cognito User Pool]
    WebApp -->|3. Call REST API + JWT| APIGW[Amazon API Gateway]
    WebApp -->|4. WebSocket connection| AppSync[Amazon AppSync GraphQL]
    
    APIGW -->|Trigger Lambda| Lambda[AWS Lambda Backend]
    Lambda -->|Read/Write data| DDB[Amazon DynamoDB]
    Lambda -->|RAG Prompt| Bedrock[Amazon Bedrock AI]
    
    AppSync -->|Sync messages| DDB_Chat[Amazon DynamoDB Chat Logs]
{{< /mermaid >}}

#### 1.1. Static Web Storage and Distribution (S3 + CloudFront)
The entire bundled source code of the React/Next.js application is stored in an S3 Bucket and distributed globally via Amazon CloudFront CDN.

- **S3 Bucket for web hosting**:
  - Bucket Name: `smart-parking-fe-prod-075647413376-ap-southeast-1-an`
  - Resource Region: `ap-southeast-1` (Singapore).
  - The main structure contains the bundled Vite/React source code including: the `assets/` directory with bundled JS/CSS source files, along with the `index.html` file as the entry point.

![S3 Buckets list](/images/5-Workshop/5.7-Web-Dashboard/aws-s3-list.png)
*Evidence 5.7.1a: List of S3 Buckets in the storage system*

![Web files on S3](/images/5-Workshop/5.7-Web-Dashboard/aws-s3-objects.png)
*Evidence 5.7.1b: Bundled Web App source files stored on S3*

- **Amazon CloudFront Distribution**:
  - Distribution ID: `EHS22PYCLM5X0`
  - Default distribution domain: `d3imp0j8sdburp.cloudfront.net`
  - Origin: Points directly to the S3 Bucket containing the static source code (`smart-parking-fe-prod...`).
  - Supported protocols: Automatic SSL/TLS optimization, routing redirect from `HTTP` to secure `HTTPS`, and the default root object set to `index.html`.

![CloudFront list](/images/5-Workshop/5.7-Web-Dashboard/aws-cloudfront.png)
*Evidence 5.7.1c: List of CloudFront CDN distributions in the system*

![CloudFront details](/images/5-Workshop/5.7-Web-Dashboard/aws-cloudfront-details.png)
*Evidence 5.7.1d: Detailed CloudFront configuration pointing origin to S3 hosting*

---

#### 1.2. User Authentication (Amazon Cognito)
The system uses Amazon Cognito User Pool to manage identities and implement role-based access control.

- **Cognito User Pool**:
  - User Pool Name: `User pool - ahlii`
  - ID: `ap-southeast-1_syJgrpSKt`
  - ARN: `arn:aws:cognito-idp:ap-southeast-1:075647413376:userpool/ap-southeast-1_syJgrpSKt`

![Cognito User Pool details](/images/5-Workshop/5.7-Web-Dashboard/aws-cognito-details.png)
*Evidence 5.7.2a: User Pool configuration overview on AWS*

- **App client integration**:
  - App Client Name: `OTP GMAIL`
  - Client ID: `5mvc3hhro0ic13s6c1sm2dd9o2`
  - Description: This Client ID is configured directly in the frontend application to call the login API and obtain JWT Tokens for authentication when calling edge REST APIs.

![Cognito App Client details](/images/5-Workshop/5.7-Web-Dashboard/aws-cognito-clients.png)
*Evidence 5.7.2b: App Client ID configuration for frontend web integration*

---

#### 1.3. Real-time Support Conversation Synchronization (AWS AppSync)
The real-time customer support chat page uses **AWS AppSync** (GraphQL API) with WebSocket Subscription mechanism to transmit and receive messages instantly without maintaining a traditional EC2 server.

- **GraphQL API AppSync**:
  - API Name: `smart-parking-chat-api`
  - API ID: `5dlkezm2rbdgfl6k2oprzh5m4m`
  - Primary authorization mode: `API_KEY`
  - Real-time Endpoint (WebSocket): `wss://lospzfnpsvbwdcd34p3cubphvm.appsync-realtime-api.ap-southeast-1.amazonaws.com/graphql`

![AppSync API list](/images/5-Workshop/5.7-Web-Dashboard/aws-appsync-list.png)
*Evidence 5.7.3a: List of integrated GraphQL APIs on AWS AppSync*

![AppSync settings configuration](/images/5-Workshop/5.7-Web-Dashboard/aws-appsync-settings.png)
*Evidence 5.7.3b: GraphQL Endpoint configuration and API Key security authentication for the Chat station*

---

#### 1.4. Real-time Parking Slot Status Processing and Synchronization Flow (Slots Flow)
To display a visual parking lot map with slots colored Green (Available) / Red (Occupied), the system performs a synchronization flow from ultrasonic sensors through the database management system to the user interface:

{{< mermaid >}}
sequenceDiagram
    participant Sensor as ESP32-S3 (Parking Lot)
    participant local as Local Backend Server
    participant DDB as Amazon DynamoDB
    participant Web as Web Dashboard (Client)
    participant APIGW as AWS API Gateway
    participant Lambda as AWS Lambda
    
    Sensor->>local: 1. POST /device/slot/update (Send measured distance)
    local->>DDB: 2. Update occupied status (true/false) in SmartParking_Slots table
    loop Periodic UI polling update
        Web->>APIGW: 3. GET /parking/status (Request parking lot status)
        APIGW->>Lambda: 4. Authenticate and forward request
        Lambda->>DDB: 5. Scan/Query SmartParking_Slots table
        DDB-->>Lambda: 6. Return slot status list (A1-A3, B1-B3)
        Lambda-->>APIGW: 7. Return JSON data (HTTP 200 OK)
        APIGW-->>Web: 8. Update slot colors: Red (Occupied) / Green (Available)
    end
{{< /mermaid >}}

---

#### 1.5. Registered Vehicle Information and Personal Parking History Query Flow (User Vehicle & History Flow)
For the User Portal, to display registered license plates and the 5 most recent entry/exit records of that vehicle, the system performs a secure authentication and query flow:

{{< mermaid >}}
sequenceDiagram
    participant Web as Web Dashboard (User Portal)
    participant Cognito as Amazon Cognito
    participant APIGW as AWS API Gateway
    participant Lambda as AWS Lambda
    participant DDB as Amazon DynamoDB
    
    Web->>Cognito: 1. Customer account login
    Cognito-->>Web: 2. Return JWT ID Token (containing user email)
    Web->>APIGW: 3. GET /vehicle/history (send JWT Token in Authorization Header)
    APIGW->>Cognito: 4. Verify JWT Token signature & expiration
    Cognito-->>APIGW: 5. Confirm Token is valid
    APIGW->>Lambda: 6. Forward request (with email extracted from Token)
    Lambda->>DDB: 7. Query history in SmartParking_VehicleHistory table by email/license plate
    DDB-->>Lambda: 8. Return list of entry/exit records
    Lambda-->>APIGW: 9. Return JSON history array result (HTTP 200 OK)
    APIGW-->>Web: 10. Display registered license plate, current vehicle location, and history list
{{< /mermaid >}}


---

### 2. Admin Portal Subsystem
Designed for operations staff and parking lot managers to monitor the system globally.

#### 2.1. Overview Dashboard (Admin Dashboard)
Provides real-time operational KPI metrics including: remaining available slots, occupancy rate, total vehicle entries/exits for the day, and a visual parking slot map (`A1-A3`, `B1-B3`) with automatic green/red status transitions based on sensor signals.
![Main Dashboard interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-dashboard.png)
*Evidence 5.7.4: Admin overview dashboard and real-time parking lot map*

#### 2.2. Parking Lot Vehicle Log (Vehicles Log)
Records vehicle entry/exit history, integrated with search by license plate, vehicle direction (entry/exit), surveillance camera snapshots, Rekognition confidence scores, and links to view original images stored on S3.
![Vehicle log interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-vehicles.png)
*Evidence 5.7.5: Full parking lot vehicle log lookup page*

#### 2.3. Traffic Statistics & Forecasting (Analytics)
Analyzes vehicle traffic by month/hour using visual charts and integrates a 7-day traffic forecasting feature powered by Amazon Bedrock.
![Analytics and charts interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-analytics.png)
*Evidence 5.7.6: Vehicle traffic statistics charts and AI forecasting page*

#### 2.4. AI Parking Virtual Assistant (AI Assistant - Admin)
The **ParkAI** chatbot (powered by Amazon Bedrock) assists administrators in querying parking lot information using natural Vietnamese language through RAG data.
![AI virtual assistant interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-ai-assistant.png)
*Evidence 5.7.7: ParkAI virtual assistant chatbot on the admin interface*

#### 2.5. Member Role Management (Role Management)
Manages staff accounts, assigns roles (`admin` / `user`), locks/unlocks accounts, and provides secure password changes.
![Role management interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-roles.png)
*Evidence 5.7.8: Account management and member role assignment interface*

#### 2.6. Real-time Customer Support (Support Chat - Admin)
Receives a list of support requests and enables real-time live chat with customers through AWS AppSync and Amplify infrastructure.
![Admin realtime support chat interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-support.png)
*Evidence 5.7.9: Real-time synchronized customer support system on the Admin interface*

---

### 3. User Portal Subsystem
Designed for parking customers to log in and manage their personal vehicles and request assistance.

#### 3.1. Status Overview (User Dashboard)
Displays the current parking lot status (available or full), overall number of available slots, and occupancy rate of each zone so customers can proactively choose a parking area.
![User overview interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-dashboard.png)
*Evidence 5.7.10: Customer-facing parking lot status overview interface*

#### 3.2. My Vehicle (My Vehicle Status)
Displays the current status of the customer's vehicle — whether it is inside or outside the lot, last seen location, recording camera, and the 5 most recent entry/exit records.
![My vehicle management interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-mycar.png)
*Evidence 5.7.11: Customer's current vehicle status tracking page*

#### 3.3. Online Incident Support (Support Chat - User)
Allows customers to create support tickets directly and exchange real-time messages with parking lot administrators when issues arise.
![User support chat interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-support.png)
*Evidence 5.7.12: Customer's real-time online support chat window*

#### 3.4. AI Parking Spot Advisor (AI Assistant - User)
An intelligent virtual assistant that answers questions about available parking spots and parking lot services for users using natural language.
![User AI assistant interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-ai.png)
*Evidence 5.7.13: Real-time AI chatbot advising users on available parking spots*

#### 3.5. Personal Parking History (User History)
A lookup table for the customer's complete personal parking history with supporting images and Rekognition confidence scores.
![User parking history interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-history.png)
*Evidence 5.7.14: Detailed vehicle entry/exit history for the customer account*

#### 3.6. Account Settings & Registered License Plate (User Profile Settings)
A page for managing customer profiles, updating the officially registered license plate to activate the automatic recognition mechanism, and changing the personal login password.
![User account settings interface](/images/5-Workshop/5.7-Web-Dashboard/5.7-user-profile.png)
*Evidence 5.7.15: Personal information settings and license plate registration page*
