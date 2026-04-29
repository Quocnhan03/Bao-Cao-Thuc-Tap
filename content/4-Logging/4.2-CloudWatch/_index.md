---
title: "CloudWatch Logs Configuration"
date :  "`r Sys.Date()`"
weight: 2
chapter : false
pre: " <b> 4.2. </b> "
---

## 4.2 CloudWatch Logs Configuration

- **Lambda:**  
  In AWS CDK, configure log retention:
  ```ts
  logRetention: logs.RetentionDays.ONE_WEEK
  --enable-cloudwatch-logs
  {
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ],
  "Resource": "arn:aws:logs:*:*:*"
  }