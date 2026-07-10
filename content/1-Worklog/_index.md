---
title: "Worklog"
date: 2026-04-27
weight: 1
pre : " <b> 1. </b> "
---


**Student Information:** Pham Quoc Nhan  
**Major:** Computer Networking  
**Team:** First Cloud Journey

---

### Week 1: IAM, VPC/VPN & EC2 Web Applications Hands-on
* **Objective:** Complete Lab 02 (IAM), Lab 03 (VPC & Site-to-Site VPN), and Lab 04 (EC2, Web Applications, and Cost Governance).
* **Tasks completed:**
    * **Lab 02 (IAM):** Configured IAM Groups, Users, Policies, and Roles; performed secure Role Switching for OperatorUser and cleaned up resources.
    * **Lab 03 (VPC/VPN):** Built VPC infrastructure (Subnets, Route Tables, IGW, NAT Gateway), tested connectivity via Session Manager and CloudWatch, and set up Site-to-Site VPN using Strongswan with Transit Gateway.
    * **Lab 04 (EC2 & Apps):** Launched EC2 Windows/Linux instances, managed custom AMIs and snapshots, deployed the User Management web application (LAMP, Node.js), and implemented AWS cost governance & security policy restrictions via IAM.

### Week 2: System Administration with AWS Systems Manager (SSM)
* **Objective:** Optimize secure instance access.
* **Tasks completed:**
    * Implemented **Session Manager** as a secure alternative to traditional SSH (securing port 22).
    * Configured IAM Roles for EC2 to grant necessary permissions to the SSM Agent.
    * Established centralized log management using Amazon CloudWatch.

### Week 3: Monitoring, Templating and Identity Management
* **Objective:** Learn and practice system monitoring, infrastructure automation, and permissions management.
* **Tasks completed:**
    * **Lab 08 (CloudWatch):** Configured Dashboards, Metrics, Logs, and Alarms to monitor EC2 instances.
    * **Lab 10 (CloudFormation & AD):** Deployed infrastructure as code with CloudFormation, configured AWS Managed Microsoft AD and Route 53 Resolver.
    * **Lab 11 (AWS CLI):** Managed AWS resources including EC2, S3, and IAM using the AWS Command Line Interface.

### Week 4: Organizations, Storage, and Backup
* **Objective:** Secure and expand multi-account infrastructure, and ensure safe data management.
* **Tasks completed:**
    * **Lab 12 (Organizations & Identity Center):** Built a multi-account structure using AWS Organizations and enabled SSO with IAM Identity Center.
    * **Lab 13 (AWS Backup):** Configured Backup Plans and Vaults to automate EC2 and EBS backups.
    * **Lab 24 (Storage Gateway):** Set up a hybrid storage connection to sync on-premises data to S3.

### Week 5: Web Security, Resource Management & Least Privilege
* **Objective:** Deploy WAF, Resource Groups, and restrictive IAM Policies.
* **Tasks completed:**
    * **Lab 26 (AWS WAF):** Deployed Web ACL with Managed Rules to protect web applications, logging requests to S3.
    * **Lab 27 (Tags & Resource Groups):** Tagged and filtered EC2 resources, managing them efficiently using Resource Groups.
    * **Lab 30 (IAM):** Designed JSON Policies for least privilege access and assigned them to a restricted IAM User.

### Week 6: Systems Management, KMS & Cost Management
* **Objective:** Master remote server management with SSM, encryption with KMS, and cost visualization with Cost Explorer.
* **Tasks completed:**
    * **Lab 31 (SSM):** Configured Session Manager to control servers directly from the browser.
    * **Lab 33 (KMS):** Created a Symmetric Customer Managed Key (CMK) and applied it to encrypt an S3 bucket.
    * **Lab 34 (Cost Explorer):** Used Cost Explorer to filter costs by service and created AWS Budgets.

### Week 7: CloudFormation, Lightsail & IAM Roles
* **Objective:** Deploy infrastructure as code, explore Lightsail architecture, and configure IAM roles.
* **Tasks completed:**
    * **Lab 37 (CloudFormation):** Successfully created a CloudFormation Stack.
    * **Lab 45 (Lightsail):** Successfully launched an Amazon Lightsail WordPress instance.
    * **Lab 48 (EC2 & IAM):** Configured an EC2 instance with an appropriate IAM Role.

### Week 8: QuickSight, Macie & Secrets Manager
* **Objective:** Implement data analytics services, S3 data security, and application credentials management.
* **Tasks completed:**
    * **Lab 73 (QuickSight):** Signed up for an Enterprise account and configured Dataset/Dashboard.
    * **Lab 90 (Macie):** Enabled Amazon Macie to automatically discover sensitive data in S3.
    * **Lab 96 (Secrets Manager):** Created and managed secrets for RDS/Fargate credentials retrieval.

---

> **Note:** This worklog will be continuously updated to reflect the ongoing progress of the internship project.