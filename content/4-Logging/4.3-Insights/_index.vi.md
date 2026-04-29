---
title: "Truy xuất Logs với Insights"
date :  "`r Sys.Date()`"
weight: 3
chapter : false
pre: " <b> 4.3. </b> "
---


- Truy cập CloudWatch Logs Insights trong AWS Console  

- Query mẫu:
```sql
filter @type = "REPORT"
| fields @requestId, @duration, @billedDuration
| sort @timestamp desc
| limit 20