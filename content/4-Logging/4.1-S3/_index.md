---
title: "S3 Bucket Setup for Logs"
date :  "`r Sys.Date()`"
weight: 1
chapter : false
pre: " <b> 4.1. </b> "
---


- Create an S3 bucket: `itealab-system-logs-2026`  
- Configure a Lifecycle Policy:  
  - Transition data to S3 Glacier after 90 days  
  - Optimize long-term storage costs  

Amazon S3 serves as the long-term storage layer for logs (acting as a data lake for log data).