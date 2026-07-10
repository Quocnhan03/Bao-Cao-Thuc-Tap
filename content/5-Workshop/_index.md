---
title: "Workshop"
weight: 5
chapter: false
pre: " <b> 5. </b> "
---

## SMART PARKING IOT SYSTEM — DETAILED IMPLEMENTATION GUIDE

### Overview

The **Smart Parking IoT System** is a comprehensive parking management automation solution built on the **AWS Serverless** architecture. It integrates edge IoT devices (ESP32 Camera and ultrasonic sensors) to recognize entering/exiting vehicles, detect empty/occupied parking slot statuses in real-time, automatically store and process data, and provide a web dashboard interface with an AI-assisted chatbot.

In this Workshop section, we will walk through all the implementation steps in detail from start to finish — including AWS infrastructure configuration, hardware flashing, user interface building, and monitoring setup.

### Table of Contents

1. [Workshop Overview](../5-workshop/1-overview/)
2. [Prerequisites](../5-workshop/2-prerequisites/)
3. [AWS IoT Core & Amazon S3](../5-workshop/3-iot-s3/)
   * [Configure AWS IoT Core](../5-workshop/3-iot-s3/1-iot-core/)
   * [Create S3 Bucket & Presigned URL](../5-workshop/3-iot-s3/2-s3/)
4. [Lambda & Amazon Rekognition](../5-workshop/4-lambda-rekognition/)
   * [Lambda Image Processing](../5-workshop/4-lambda-rekognition/1-lambda-image/)
   * [Amazon Rekognition Integration](../5-workshop/4-lambda-rekognition/2-rekognition/)
   * [DynamoDB Tables Design](../5-workshop/4-lambda-rekognition/3-dynamodb/)
   * [End-to-End Recognition Test](../5-workshop/4-lambda-rekognition/4-end-to-end/)
5. [API Gateway, Cognito & Bedrock](../5-workshop/5-api-cognito-bedrock/)
6. [ESP32 Hardware Setup](../5-workshop/6-esp32/)
7. [Web Dashboard](../5-workshop/7-dashboard/)
8. [Monitoring with CloudWatch](../5-workshop/8-monitoring/)
9. [Clean Up Resources](../5-workshop/9-cleanup/)
