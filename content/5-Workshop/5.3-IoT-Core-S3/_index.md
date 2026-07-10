---
title: "AWS IoT Core & Amazon S3"
date: 2026-04-26
weight: 3
chapter: false
pre: " <b> 4.3. </b> "
---

# Device Communication & Image Storage Setup

In this chapter, we begin building the physical layer of the smart parking system by connecting our device to the AWS cloud and preparing the storage repository for vehicle license plate images.

### Interaction Architecture

1. **AWS IoT Core**: Acts as the central MQTT Broker, responsible for receiving parking space status data from ultrasonic sensors via secure MQTT protocol, and managing edge device credentials via X.509 certificates.
2. **Amazon S3**: Stores the license plate images captured by the camera. To ensure security and optimize edge device resources, the system employs the **Presigned URL** mechanism, allowing the camera to upload images directly to S3 without storing AWS access keys on the hardware.

---

### Detailed Subsections:

* **5.3.1.** [AWS IoT Core Configuration](5.3.1-iot-core-setup/)
* **5.3.2.** [Create S3 Bucket & Presigned URL](5.3.2-s3-presigned-url/)
