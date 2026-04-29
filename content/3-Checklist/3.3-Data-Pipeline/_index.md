---
title : "Raw Data Storage"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 3.3. </b> "
---

- **3.3.1. Raw Data Storage:**  
  - Create an S3 bucket as a "Data Lake" and configure an IoT Rule to automatically store MQTT messages in S3.

- **3.3.2. Automated Processing (ETL Pipeline):**  
  - Configure a Lambda trigger to process new incoming data.  
  - Use a Glue Crawler to infer the data schema and Glue ETL Jobs to transform and standardize the data format (e.g., Parquet).

- **3.3.3. Analytical Data Storage:**  
  - Create a dedicated S3 bucket for storing cleaned and processed data.