import os

base_dir = r"c:\Users\ASUS\Downloads\000000-Workshop\000058-SessionManager\content\1-Worklog\Worklog T3"

labs = {
    "Lab08": {
        "title": "Lab 08: System Monitoring with Amazon CloudWatch",
        "title_vi": "Lab 08: Giam sat he thong voi Amazon CloudWatch",
        "weight": 1,
        "content": [
            "1. Introduction",
            "2. Preparatory steps",
            "3. CloudWatch Metrics",
            "   3.1 Viewing Metrics",
            "   3.2 Search expressions",
            "   3.3 Math expressions",
            "   3.4 Dynamic Labels",
            "4. CloudWatch Logs",
            "   4.1 CloudWatch Logs",
            "   4.2 CloudWatch Logs Insights",
            "   4.3 CloudWatch Metric Filter",
            "5. CloudWatch Alarms",
            "6. CloudWatch Dashboards",
            "7. Clean up resources"
        ]
    },
    "Lab10": {
        "title": "Lab 10: Active Directory and RD Gateway Connection",
        "title_vi": "Lab 10: Active Directory va ket noi RD Gateway",
        "weight": 2,
        "content": [
            "1. Introduction",
            "2. Preparation",
            "   2.1 Generate Key Pair",
            "   2.2 Initialize CloudFormation Template",
            "   2.3 Configuring Security Group",
            "3. Connecting to RDGW",
            "4. Microsoft AD Deployment",
            "5. Setup DNS",
            "   5.1 Create Route 53 Outbound Endpoint",
            "   5.2 Create Route 53 Resolver Rules",
            "   5.3 Create Route 53 Inbound Endpoints",
            "   5.4 Test results",
            "6. Clean up resources"
        ]
    },
    "Lab11": {
        "title": "Lab 11: Resource Management via AWS CLI",
        "title_vi": "Lab 11: Quan ly tai nguyen qua AWS CLI",
        "weight": 3,
        "content": [
            "1. Introduction",
            "2. Preparation",
            "3. Install AWS CLI",
            "4. View resource via CLI",
            "5. AWS CLI with Amazon S3",
            "6. AWS CLI with Amazon SNS",
            "7. AWS CLI with IAM",
            "8. AWS CLI with VPC",
            "   8.1 AWS CLI with VPC",
            "   8.2 AWS CLI with Internet Gateway",
            "9. Creating EC2 Using AWS CLI",
            "10. Troubleshooting",
            "11. Clean up resources"
        ]
    }
}

for folder, data in labs.items():
    lab_dir = os.path.join(base_dir, folder)
    os.makedirs(lab_dir, exist_ok=True)
    
    en_content = f"---\ntitle: \"{data['title']}\"\nweight: {data['weight']}\n---\n\n# {data['title']}\n\n"
    for line in data['content']:
        if line.startswith("   "):
            en_content += f"### {line.strip()}\n![Screenshot](/images/WorklogT3/{folder.lower()}-{line.strip().replace(' ', '-').replace('.', '').lower()}.png)\n\n"
        else:
            en_content += f"## {line}\n"
            if "Introduction" not in line and "Clean up" not in line:
                if not any(sub in data['content'] for sub in data['content'] if sub.startswith(f"   {line.split('.')[0]}.")):
                    en_content += f"![Screenshot](/images/WorklogT3/{folder.lower()}-{line.strip().replace(' ', '-').replace('.', '').lower()}.png)\n\n"
                else:
                    en_content += "\n"
            else:
                en_content += "\n"
            
    vi_content = f"---\ntitle: \"{data['title_vi']}\"\nweight: {data['weight']}\n---\n\n# {data['title_vi']}\n\n"
    for line in data['content']:
        if line.startswith("   "):
            vi_content += f"### {line.strip()}\n![Screenshot](/images/WorklogT3/{folder.lower()}-{line.strip().replace(' ', '-').replace('.', '').lower()}.png)\n\n"
        else:
            vi_content += f"## {line}\n"
            if "Introduction" not in line and "Clean up" not in line:
                if not any(sub in data['content'] for sub in data['content'] if sub.startswith(f"   {line.split('.')[0]}.")):
                    vi_content += f"![Screenshot](/images/WorklogT3/{folder.lower()}-{line.strip().replace(' ', '-').replace('.', '').lower()}.png)\n\n"
                else:
                    vi_content += "\n"
            else:
                vi_content += "\n"
            
    with open(os.path.join(lab_dir, "_index.md"), "w", encoding="utf-8") as f:
        f.write(en_content)
    with open(os.path.join(lab_dir, "_index.vi.md"), "w", encoding="utf-8") as f:
        f.write(vi_content)

print("Created Lab 08, 10, 11 markdown structures.")
