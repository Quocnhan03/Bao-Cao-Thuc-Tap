---
title: "Session Logs Management"
date :  "`r Sys.Date()`"
weight: 4
chapter : false
pre: " <b> 4. </b> "
---

This section establishes a centralized monitoring mechanism that enables tracking and auditing of all system activities and incidents.  

The system leverages a combination of Amazon S3, CloudWatch, and Amazon SNS to store, analyze, and generate alerts from logs.

### Deployment Contents:

4.1. [S3 Bucket Setup for Logs (Long-term Archiving)](4.1-s3/) \
4.2. [CloudWatch Logs Configuration](4.2-cloudwatch/) \
4.3. [Log Analysis with CloudWatch Logs Insights](4.3-insights/) \
4.4. [Alert Setup with Amazon SNS](4.4-alert/)