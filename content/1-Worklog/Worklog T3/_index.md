---
title: "Week 3"
date: 2026-05-04
weight: 3
pre : " <b> 1.3. </b> "
---

# WORKLOG - WEEK 3

**Period:** 04/05/2026 - 10/05/2026  
**Major:** Computer Networking  
**Team:** First Cloud Journey

---

## 1. Weekly Objectives
* Implement AWS CloudWatch for resource monitoring, log management, and automated alerting (Lab 8).
* Deploy Microsoft AD and configure Route 53 DNS for secure connections via RD Gateway (Lab 10).
* Practice using AWS CLI to manage services like S3, SNS, IAM, VPC, and deploy EC2 instances (Lab 11).

## 2. Tasks & Schedule
| Day | Task | Start Date | Completion | Source |
| :--- | :--- | :--- | :--- | :--- |
| Mon | Explore AWS CloudWatch (Metrics, Logs, Alarms) | 04/05/2026 | 04/05/2026 | [AWS Study Group - Lab 08](https://000008.awsstudygroup.com/) |
| Tue | Practice Lab 8: Resource Monitoring with CloudWatch | 05/05/2026 | 05/05/2026 | [AWS Study Group - Lab 08](https://000008.awsstudygroup.com/) |
| Wed | Prepare Lab 10: Initialize CloudFormation for RDGW | 06/05/2026 | 06/05/2026 | [AWS Study Group - Lab 10](https://000010.awsstudygroup.com/) |
| Thu | Practice Lab 10: Deploy Microsoft AD & Setup DNS | 07/05/2026 | 07/05/2026 | [AWS Study Group - Lab 10](https://000010.awsstudygroup.com/) |
| Fri | Learn AWS CLI & Practice with S3, SNS, IAM, VPC (Lab 11) | 08/05/2026 | 08/05/2026 | [AWS Study Group - Lab 11](https://000011.awsstudygroup.com/) |
| Sat | Practice Lab 11: Create EC2 via CLI & Troubleshooting | 09/05/2026 | 09/05/2026 | [AWS Study Group - Lab 11](https://000011.awsstudygroup.com/) |
| Sun | Finalize Worklog, cleanup resources | 10/05/2026 | 10/05/2026 | Internal |

## 3. Key Achievements

### 3.1. Lab 8 - System Monitoring with Amazon CloudWatch
* Monitored and analyzed resource metrics via CloudWatch Metrics.
* Searched and analyzed event logs using CloudWatch Logs.
* Set up CloudWatch Alarms to alert when resources exceed thresholds.
* Built CloudWatch Dashboards for visual tracking of key metrics.

### 3.2. Lab 10 - Active Directory and RD Gateway Connection
* Initialized CloudFormation template to build the basic infrastructure.
* Successfully deployed AWS Managed Microsoft AD (Directory Service).
* Configured Endpoints and Resolver Rules on Route 53 for internal DNS resolution.

### 3.3. Lab 11 - Resource Management via AWS CLI
* Successfully installed and configured AWS CLI on local/CloudShell environment.
* Executed interactive commands with Amazon S3, SNS, IAM, and VPC.
* Created an EC2 instance entirely via CLI commands.

> **Note:** All resources created during Lab 8, 10, 11 practices will be cleaned up immediately after completion to avoid unwanted charges.

{{% expand "Lab 08: System Monitoring with Amazon CloudWatch" %}}

## 1. CloudWatch Metrics
![Viewing Metrics](/images/WorklogT3/lab08-31-viewing-metrics.png)
![Search expressions](/images/WorklogT3/lab08-32-search-expressions.png)

## 2. CloudWatch Logs
![CloudWatch Logs](/images/WorklogT3/lab08-41-cloudwatch-logs.png)

## 3. CloudWatch Alarms
![CloudWatch Alarms](/images/WorklogT3/lab08-5-cloudwatch-alarms.png)

## 4. CloudWatch Dashboards
![CloudWatch Dashboards](/images/WorklogT3/lab08-6-cloudwatch-dashboards.png)
{{% /expand %}}

{{% expand "Lab 10: Active Directory and RD Gateway Connection" %}}

## 1. Preparation
![Key Pair](/images/WorklogT3/lab10-21-generate-key-pair.png)
![Upload Template](/images/WorklogT3/lab10-22-initialize-cloudformation-template-upload.png)
![Review](/images/WorklogT3/lab10-22-initialize-cloudformation-template-review.png)
![In Progress](/images/WorklogT3/lab10-22-initialize-cloudformation-template-inprogress.png)
![Security Group](/images/WorklogT3/lab10-23-configuring-security-group.png)

## 2. Connecting to RDGW
![Connecting to RDGW](/images/WorklogT3/lab10-3-connecting-to-rdgw.png)

## 3. Microsoft AD Deployment
![AD Deployment](/images/WorklogT3/lab10-4-microsoft-ad-deployment.png)

## 4. Setup DNS
![Outbound Endpoint](/images/WorklogT3/lab10-51-create-route-53-outbound-endpoint.png)
![Resolver Rules](/images/WorklogT3/lab10-52-create-route-53-resolver-rules.png)
![Inbound Endpoints](/images/WorklogT3/lab10-53-create-route-53-inbound-endpoints.png)
![Test Results](/images/WorklogT3/lab10-54-test-results.png)
{{% /expand %}}

{{% expand "Lab 11: Resource Management via AWS CLI" %}}

## 1. View resource via CLI
![View Resource](/images/WorklogT3/lab11-04-view-resource-cli.png)

## 2. AWS CLI with Amazon S3
![S3 Output](/images/WorklogT3/lab11-05-aws-cli-with-s3.png)

## 3. AWS CLI with Amazon SNS
![SNS Output](/images/WorklogT3/lab11-06-aws-cli-with-sns.png)

## 4. AWS CLI with IAM
![IAM Output](/images/WorklogT3/lab11-07-aws-cli-with-iam.png)

## 5. AWS CLI with VPC
![VPC Output](/images/WorklogT3/lab11-08-aws-cli-with-vpc.png)
![IGW Output](/images/WorklogT3/lab11-082-aws-cli-with-internet-gateway.png)

## 6. Creating EC2 Using AWS CLI
![EC2 Output](/images/WorklogT3/lab11-09-creating-ec2-using-aws-cli.png)
{{% /expand %}}
