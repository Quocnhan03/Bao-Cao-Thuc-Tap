---
title: "API Gateway, Cognito & Bedrock"
date: 2026-04-26
weight: 5
chapter: false
pre: " <b> 4.5. </b> "
---

To provide endpoints for the Web Dashboard application and the IoT edge system, while ensuring information security and artificial intelligence integration, three services — **AWS API Gateway**, **Amazon Cognito**, and **Amazon Bedrock** — have been tightly integrated.

---

### 1. Request Processing Flow & Security Architecture (API Architecture)
The system employs a multi-layered sequential security architecture to control access, authenticate, and orchestrate requests from the user side when communicating with backend and AI services:

{{< mermaid >}}
sequenceDiagram
    participant User as Web Dashboard
    participant Cognito as Amazon Cognito
    participant APIGW as AWS API Gateway
    participant Lambda as AWS Lambda (ai-assistant)
    participant Dynamo as Amazon DynamoDB
    participant Bedrock as Amazon Bedrock
    
    User->>Cognito: 1. Submit login credentials
    Cognito-->>User: 2. Return JWT Token upon successful authentication
    User->>APIGW: 3. Send question / data request (with JWT Token)
    APIGW->>Lambda: 4. Validate token and forward request
    Lambda->>Dynamo: 5. Query parking lot status and vehicle history (RAG context)
    Dynamo-->>Lambda: 6. Return raw real-time data from parking lot
    Lambda->>Bedrock: 7. Send question with parking lot data (Claude LLM)
    Bedrock-->>Lambda: 8. Respond in natural Vietnamese language
    Lambda-->>APIGW: 9. Return processed result (HTTP 200 OK)
    APIGW-->>User: 10. Respond and display results on Dashboard
{{< /mermaid >}}

---

### 2. Authentication Configuration with Amazon Cognito
To prevent unauthorized access to the parking lot management Dashboard, the system deploys the **Amazon Cognito User Pool** service to manage user identities (Administrators and parking lot staff):
- **User Pool Name**: `User pool - ahlii`
- **User Pool ID**: `ap-southeast-1_syJgrpSKt`
- **Authentication channel**: Login via username/email and a strong password. Upon successful login, Cognito issues a **JSON Web Token (JWT)** security identifier to the browser, which is attached to the header of every API request.

![Cognito User Pool Configuration](/images/5-Workshop/5.5-API-Cognito-Bedrock/5.5-cognito.png)
*Figure 5.5.1: Amazon Cognito User Pool management interface for user authentication*

---

### 3. API Route Design on AWS API Gateway
**AWS API Gateway** serves as the central communication gateway (API Gateway), receiving and routing HTTP API calls from the Web Dashboard to the corresponding backend Lambda handler functions.

#### 3.1. List of Routes configured on `smart-parking-api` (ID: `ebhguaykmc`):
- **Route `/parking/status` (Method `GET`)**:
  - *Function*: Query the current occupied/available status of parking spaces in the lot.
  - *Integration*: Invokes a Lambda handler function to read data from the `SmartParking_Slots` table.
- **Route `/vehicle/history` (Method `GET`)**:
  - *Function*: Retrieve the log of vehicle entry/exit events for statistical purposes.
  - *Integration*: Invokes a Lambda handler function to query the `SmartParking_VehicleHistory` history table.
- **Route `/chat` (Method `ANY` - CORS enabled)**:
  - *Function*: Communicate directly with the Smart Parking AI Virtual Assistant.
  - *Integration*: Connects to the `smart-parking-ai-assistant` Lambda function.

![API Gateway Route List](/images/5-Workshop/5.5-API-Cognito-Bedrock/5.5-routes.png)
*Figure 5.5.2: Route definitions on AWS API Gateway for the parking system*

---

### 4. AI Virtual Assistant Integration with Amazon Bedrock

#### 4.1. AI Orchestration Lambda Function (`smart-parking-ai-assistant`)
The Lambda function running on a **Node.js 20** runtime receives natural language questions from users on the Web Dashboard, then automatically collects parking lot context and sends it to a large language model for a response.

![Lambda AI Assistant Source Code](/images/5-Workshop/5.5-API-Cognito-Bedrock/5.5-bedrock-lambda.png)
*Figure 5.5.3: Source code structure of the parking lot AI assistant orchestrator linked with API Gateway*

#### 4.2. RAG (Retrieval-Augmented Generation) Processing Pipeline and Bedrock Integration
To enable the AI assistant to accurately answer questions about current vehicle counts or entry/exit history without retraining the model, a context processing pipeline (RAG) is implemented as follows:

1. **Receive question**: The Lambda function receives the user's Vietnamese-language question (e.g., *"Are there any available spaces in the lot right now?"*).
2. **Real-time context retrieval (Context Retrieval)**: Lambda performs a Scan/Query on two DynamoDB tables — `SmartParking_Slots` and `SmartParking_VehicleHistory` — to retrieve the list of currently available parking spaces and the most recent vehicle entries/exits.
3. **Construct data-enriched prompt**: Lambda embeds the actual data retrieved from the database into the prompt template to be sent to the AI:
   ```text
   You are the intelligent Virtual Assistant for Smart Parking.
   Real-time data from the parking lot database:
   - Total parking spaces: 10 spaces.
   - Current status: slot-01 is OCCUPIED, slot-02 is AVAILABLE, slot-03 is AVAILABLE.
   - Recent vehicle entry/exit log: Vehicle 30E-922.91 entered at 14:05.

   Please answer the following user question concisely and politely in Vietnamese:
   [User question]
   ```
4. **Invoke model via Amazon Bedrock**: Uses the AWS SDK to call the Amazon Bedrock service (using a foundation model such as Anthropic Claude 3.5 Sonnet or Claude 3 Haiku) via the `InvokeModel` API:
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
5. **Return result**: Extracts the text content from the Bedrock response and sends it back to the Web Dashboard user interface via API Gateway.
