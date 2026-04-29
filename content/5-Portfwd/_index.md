---
title: "Secure Remote Access"
date :  "`r Sys.Date()`"
weight: 5
chapter : false
pre: " <b> 5. </b> "
---


This technique allows administrators to securely access internal resources (Private Subnets) without exposing public ports.

- **5.1. Introduction to AWS SSM Session Manager:**  
  Utilize the Port Forwarding feature of AWS Systems Manager Session Manager to establish a secure tunnel instead of using traditional SSH.

- **5.2. Setup Guide:**  
  - Install AWS CLI and the Session Manager Plugin on your local machine.  
  - Use the following CLI command:
    ```bash
    aws ssm start-session \
      --target <instance-id> \
      --document-name AWS-StartPortForwardingSession \
      --parameters '{"portNumber":["80"],"localPortNumber":["8080"]}'
    ```

- **5.3. Testing:**  
  Access `http://localhost:8080` in your browser to verify a successful connection to the service within the VPC.