import time
import pyperclip
import pyautogui
import pygetwindow as gw

script = """
OLD_INSTANCE=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=SSM-Lab-Instance" "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].InstanceId' --output text)
if [ ! -z "$OLD_INSTANCE" ] && [ "$OLD_INSTANCE" != "None" ]; then
    aws ec2 terminate-instances --instance-ids $OLD_INSTANCE
fi

WINDOWS_AMI_ID=$(aws ssm get-parameters --names /aws/service/ami-windows-latest/Windows_Server-2022-English-Full-Base --query 'Parameters[0].Value' --output text)
aws ec2 run-instances --image-id $WINDOWS_AMI_ID --instance-type t2.micro --iam-instance-profile Name=SSMLabProfile --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Windows-Lab-SSM-1}]'
aws ec2 run-instances --image-id $WINDOWS_AMI_ID --instance-type t2.micro --iam-instance-profile Name=SSMLabProfile --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Windows-Lab-SSM-2}]'

CT_BUCKET_NAME="lab33-cloudtrail-bucket-$(date +%s)"
aws s3api create-bucket --bucket $CT_BUCKET_NAME --region us-east-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
cat <<EOF > bucket_policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::$CT_BUCKET_NAME"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::$CT_BUCKET_NAME/AWSLogs/$ACCOUNT_ID/*",
            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
        }
    ]
}
EOF
aws s3api put-bucket-policy --bucket $CT_BUCKET_NAME --policy file://bucket_policy.json

aws cloudtrail create-trail --name Lab33-Trail --s3-bucket-name $CT_BUCKET_NAME --is-multi-region-trail
aws cloudtrail start-logging --name Lab33-Trail
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
    time.sleep(10)
    
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
