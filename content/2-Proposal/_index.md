---
title: "Project Proposal"
date: 2026-04-27
weight: 2
pre : " <b> 2. </b> "
---

# PROJECT PROPOSAL: IoT Weather Platform for Lab Research

**A Serverless AWS Solution for Real-Time Weather Monitoring**

## 1. Executive Summary
The project aims to build an IoT platform for **ITea Lab** (Ho Chi Minh City) to optimize weather data collection and analysis. The system supports 5 existing stations and is scalable up to 15 stations, utilizing edge devices (Raspberry Pi/ESP32) connected via MQTT. By leveraging AWS Serverless infrastructure, the platform ensures real-time monitoring and predictive analytics with optimized operational costs.

## 2. Problem Statement
* **Current Challenges:** Manual data collection process, lack of centralization, management difficulties as the number of stations grows, and high costs associated with third-party platforms.
* **Solution:** Develop a centralized system using AWS IoT Core, AWS Glue ETL, and Amplify to fully automate the data pipeline from measurement stations to the analytics dashboard.
* **ROI:** Reduces manual workload, improves data reliability, and provides a stable Data Lake for AI research. The estimated payback period is 6–12 months.

## 3. Solution Architecture
The system adopts a Serverless architecture to ensure scalability and cost-efficiency.

* **Key AWS Services:**
    * **Data Ingestion:** AWS IoT Core (MQTT).
    * **Compute & Logic:** AWS Lambda, AWS Glue (ETL Jobs).
    * **Storage:** Amazon S3 (Data Lake + Analytics Bucket).
    * **User Interface:** AWS Amplify (Next.js), Amazon Cognito.
* **Data Flow:** Edge Device (Raspberry Pi) → AWS IoT Core → S3 Data Lake → AWS Glue → S3 Analytics → Web Dashboard.
* ![alt text](image.png)

## 4. Technical Implementation
* **Implementation Phases:**
    1. **Month 0 (Planning):** Legacy station assessment & architecture design.
    2. **Month 1 (Feasibility):** Cost estimation using AWS Pricing Calculator.
    3. **Month 2 (Optimization):** Architecture optimization (Lambda & Next.js).
    4. **Month 3 (Deployment):** Development (CDK/SDK), testing, and go-live.
* **Requirements:** Raspberry Pi running Docker (edge filtering), utilizing AWS CDK for Infrastructure as Code (IaC).

## 5. Budget & Cost Estimation
* **Hardware Cost:** ~265 USD (one-time investment).
* **AWS Operational Cost (Estimated):** ~0.7 USD/month (~8.40 USD/year).
    * *Main components:* MQTT messages, S3 Storage, AWS Glue, API Gateway.

## 6. Risk Assessment & Mitigation
| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Network outage | Medium | Local storage on Raspberry Pi (Docker). |
| Sensor failure | High | Periodic maintenance, spare parts. |
| Budget overrun | Low | Set Budget Alerts in AWS Billing Dashboard. |

## 7. Expected Outcomes
* **Technical:** Build an automated system to replace manual processes, scalable up to 15 stations.
* **Research:** Establish a stable Data Lake for AI model training and internal research projects for at least 1 year.