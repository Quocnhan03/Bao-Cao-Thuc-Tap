#!/bin/bash
echo "Deploying Lab 31 - Systems Manager setup..."
# Usually SSM is pre-enabled for Amazon Linux 2, nothing much to deploy via CLI for basic lab

echo "Deploying Lab 33 - KMS Key..."
aws kms create-key --description "Worklog 6 KMS Key"

echo "Deploying Lab 34 - Cost Budgets..."
# Budgets usually created via console in labs.

echo "Finished Worklog 6 dummy deployment!"
