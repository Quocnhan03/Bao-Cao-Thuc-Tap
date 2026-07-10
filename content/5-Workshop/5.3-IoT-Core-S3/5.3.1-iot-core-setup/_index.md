---
title: "AWS IoT Core Configuration"
date: 2026-04-26
weight: 1
chapter: false
pre: " <b> 4.3.1. </b> "
---

In this section, we will configure **AWS IoT Core** to register our hardware device (ESP32 Camera) and establish the security certificates that allow the device to securely communicate with the AWS cloud via the MQTT protocol.

---

### Step 1: Create an IoT Thing (Device Registration)
1. Sign in to the **AWS Management Console** and search for the **IoT Core** service.
2. In the left navigation bar, choose **Manage** -> **All devices** -> **Things**.
3. Click **Create things** to start registering a new device:
   - Select **Create single thing** and click **Next**.
   - **Thing name**: Set the device name to `ESP32_Cam_Parking`.
   - Leave other configurations at their defaults and click **Next**.

![Register IoT Thing](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-create-thing.png)
*(Proof: Screenshot of successful Thing creation page or Things list containing ESP32_Cam_Parking)*

---

### Step 2: Set Up Security Certificates (Certificates)
AWS IoT Core requires X.509 certificate authentication to ensure absolute connection security:
1. On the **Device certificate** page, select **Auto-generate new certificate (recommended)**. Click **Next**.
2. **Download certificate files**:
   > [!IMPORTANT]
   > You must download all these files immediately because AWS will not allow you to download them a second time after you leave this page.
   - **Device certificate** (looks like `xxx.cert.pem`).
   - **Private key file** (looks like `xxx.private.key`).
   - **Amazon Root CA 1** (AWS root CA certificate).
3. Save these files in a secure directory on your computer.
4. Click **Next** (do not click *Create thing* yet as we need to create a Policy in the next step).

![Download certificates](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-certificates.png)
*(Proof: Screenshot of downloading Certificate and Key files step)*

---

### Step 3: Create and Attach an AWS IoT Policy
Policies are used to grant specific permissions to the device, defining what actions (publishing data, receiving messages, connecting) it can perform on the MQTT Broker.

1. On the Attach Policy page, click **Create policy** (this will open a new browser tab).
2. Set the Policy parameters:
   - **Policy name**: Enter `ESP32_Parking_Policy`.
   - **Policy document**: Switch to **JSON** mode and paste the following permission code:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "iot:Connect",
           "iot:Publish",
           "iot:Subscribe",
           "iot:Receive"
         ],
         "Resource": [
           "*"
         ]
       }
     ]
   }
   ```
3. Click **Create** to complete policy creation.
4. Go back to the previous register Thing tab, select the newly created Policy (`ESP32_Parking_Policy`).
5. Click **Create thing** to finish registering the device.

![Configure IoT Policy](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-iot-policy.png)
*(Proof: Screenshot of JSON Policy configuration on AWS Console)*

---

### Step 4: Get MQTT Endpoint Information
Each AWS account has a unique MQTT Endpoint for devices to connect to:
1. From the left menu of **AWS IoT Core**, scroll to the bottom and select **Settings**.
2. Under **Device data endpoint**, you will see a long string of characters structured like:
   `xxxxxxxxxxxxxx-ats.iot.ap-southeast-1.amazonaws.com`
3. Copy this Endpoint address and save it to configure in the ESP32 source code later.

![MQTT Endpoint](/images/5-Workshop/5.3-IoT-Core-S3/5.3.1-endpoint.png)
*(Proof: Screenshot of Settings page displaying the Device data endpoint)*
