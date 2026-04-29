---
title: "Thiết lập S3 Bucket cho Logs"
date :  "`r Sys.Date()`"
weight: 1
chapter : false
pre: " <b> 4.1. </b> "
---


- Tạo S3 bucket: `itealab-system-logs-2026`  
- Thiết lập Lifecycle Policy:
  - Chuyển dữ liệu sang S3 Glacier sau 90 ngày  
  - Giúp tối ưu chi phí lưu trữ dài hạn  

S3 đóng vai trò là nơi lưu trữ log lâu dài (Data Lake cho logs).