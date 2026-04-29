---
title: "Log Analysis with CloudWatch Insights"
date :  "`r Sys.Date()`"
weight: 3
chapter : false
pre: " <b> 4.3. </b> "
---


- Access CloudWatch Logs Insights in the AWS Management Console.  

- Example query:
```sql
filter @type = "REPORT"
| fields @requestId, @duration, @billedDuration
| sort @timestamp desc
| limit 20