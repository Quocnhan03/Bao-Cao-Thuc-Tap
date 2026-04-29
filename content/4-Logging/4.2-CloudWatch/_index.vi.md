---
title: "Cấu hình CloudWatch Logs"
date :  "`r Sys.Date()`"
weight: 2
chapter : false
pre: " <b> 4.2. </b> "
---


- **Lambda:**  
  Trong AWS CDK:
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