---
title: "Workshop"
date: 2026-04-26
weight: 4
chapter: false
pre: " <b> 4. </b> "
---

# Smart Parking IoT System — Detailed Implementation Guide

#### Overview

The **Smart Parking IoT System** is a comprehensive parking management automation solution built on the **AWS Serverless** architecture. It integrates edge IoT devices (ESP32 Camera and ultrasonic sensors) to recognize entering/exiting vehicles, detect empty/occupied parking slot statuses in real-time, automatically store and process data, and provide a web dashboard interface with an AI-assisted chatbot.

In this Workshop section, we will walk through all the implementation steps in detail from start to finish — including AWS infrastructure configuration, hardware flashing, user interface building, and monitoring setup.

#### Table of Contents

1. [Workshop Overview](5.1-workshop-overview/)
2. [Prerequisites](5.2-prerequisite/)
3. [AWS IoT Core & Amazon S3](5.3-iot-core-s3/)
   * 3.1. [Configure AWS IoT Core](5.3-iot-core-s3/5.3.1-iot-core-setup/)
   * 3.2. [Create S3 Bucket & Presigned URL](5.3-iot-core-s3/5.3.2-s3-presigned-url/)
4. [Lambda & Amazon Rekognition](5.4-lambda-rekognition/)
   * 4.1. [Lambda Image Processing](5.4-lambda-rekognition/5.4.1-lambda-image-processing/)
   * 4.2. [Amazon Rekognition Integration](5.4-lambda-rekognition/5.4.2-rekognition-integration/)
   * 4.3. [DynamoDB Tables Design](5.4-lambda-rekognition/5.4.3-dynamodb-setup/)
   * 4.4. [End-to-End Recognition Test](5.4-lambda-rekognition/5.4.4-end-to-end-test/)
5. [API Gateway, Cognito & Bedrock](5.5-api-cognito-bedrock/)
6. [ESP32 Hardware Setup](5.6-hardware-esp32/)
7. [Web Dashboard](5.7-web-dashboard/)
8. [Monitoring with CloudWatch](5.8-monitoring-cloudwatch/)
9. [Clean Up Resources](5.9-cleanup/)
