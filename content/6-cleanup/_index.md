---
title: "Resource Cleanup"
date :  "`r Sys.Date()`"
weight: 6
chapter : false
pre: " <b> 6. </b> "
---


This step is essential to properly terminate the system and optimize AWS costs after completing the project.

- **6.1. Destroy Infrastructure using CDK:**  
  - Navigate to the CDK project directory  
  - Run the following command:
    ```bash
    cdk destroy --all
    ```

- **6.2. Manual Resource Cleanup:**  
  - Remove any remaining S3 buckets that still contain data  
  - Delete unused IAM Roles or Cognito User Pools  

- **6.3. Cost Verification:**  
  - Access: https://console.aws.amazon.com/billing/  
  - Ensure that no resources are still running to avoid unexpected charges