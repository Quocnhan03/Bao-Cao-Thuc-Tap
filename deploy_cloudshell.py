import time
import pyperclip
import pyautogui
import pygetwindow as gw

script = """
aws iam create-role --role-name SSMLabRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name SSMLabRole --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
aws iam create-instance-profile --instance-profile-name SSMLabProfile
aws iam add-role-to-instance-profile --instance-profile-name SSMLabProfile --role-name SSMLabRole
sleep 10
AMI_ID=$(aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64 --query 'Parameters[0].Value' --output text)
aws ec2 run-instances --image-id $AMI_ID --instance-type t2.micro --iam-instance-profile Name=SSMLabProfile --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=SSM-Lab-Instance}]'
KEY_ID=$(aws kms create-key --description "Lab 33 KMS Key" --query 'KeyMetadata.KeyId' --output text)
aws kms create-alias --alias-name alias/lab33-key --target-key-id $KEY_ID
BUCKET_NAME="lab33-kms-bucket-$(date +%s)"
aws s3api create-bucket --bucket $BUCKET_NAME --region us-east-1
aws s3api put-bucket-encryption --bucket $BUCKET_NAME --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"'$KEY_ID'"}}]}'
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws budgets create-budget --account-id $ACCOUNT_ID --budget '{"BudgetName":"Lab34-Budget","BudgetLimit":{"Amount":"10","Unit":"USD"},"CostTypes":{"IncludeTax":true,"IncludeSubscription":true,"UseBlended":false,"IncludeRefund":false,"IncludeCredit":false,"IncludeUpfront":false,"IncludeRecurring":true,"IncludeOtherSubscription":false,"IncludeSupport":false,"IncludeDiscount":true,"UseAmortized":false},"TimeUnit":"MONTHLY","TimePeriod":{"Start":"2026-07-01T00:00:00Z","End":"2087-06-15T00:00:00Z"},"BudgetType":"COST"}' --notifications-with-subscribers '[{"Notification":{"NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN","Threshold":100},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"admin@example.com"}]}]'
"""

pyperclip.copy(script)

windows = gw.getWindowsWithTitle('AWS CloudShell')
if not windows:
    windows = gw.getWindowsWithTitle('Chrome')
    
if windows:
    win = windows[0]
    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(1)
    
    # Click in middle
    pyautogui.click(win.left + win.width // 2, win.top + win.height // 2)
    time.sleep(0.5)
    
    # Paste
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    print("Script pasted and executed!")
else:
    print("Window not found")
