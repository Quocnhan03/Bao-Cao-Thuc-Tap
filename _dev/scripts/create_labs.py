import os

base_dir = r"c:\Users\ASUS\Downloads\000000-Workshop\000058-SessionManager\content"

labs = {
    "7-Lab05": {
        "title": "Lab 05: EC2 & RDS Deployment",
        "title_vi": "Lab 05: Triển khai EC2 & RDS",
        "weight": 7,
        "content": [
            "1. Introduction",
            "2. Prerequisite Steps",
            "   2.1 Create a VPC",
            "   2.2 Create EC2 Security Group",
            "   2.3 Create RDS Security Group",
            "   2.4 Create DB Subnet Group",
            "3. Create EC2 instance",
            "4. Create RDS database instance",
            "5. Application Deployment",
            "6. Backup and Restore",
            "7. Clean up resources"
        ]
    },
    "8-Lab06": {
        "title": "Lab 06: ASG & ALB",
        "title_vi": "Lab 06: Tự động mở rộng và Cân bằng tải",
        "weight": 8,
        "content": [
            "1. Introduction",
            "2. Preparation",
            "   2.1. Setup Network Infrastructure",
            "   2.2. Launch EC2 Instance",
            "   2.3. Launch a Database Instance with RDS",
            "   2.4. Setup data for Database",
            "   2.5. Deploy Web Server",
            "   2.6. Prepare metric for Predictive scaling",
            "3. Create Launch Template",
            "4. Setting Up Load Balancer",
            "   4.1. Create Target Group",
            "   4.2. Create Load Balancer",
            "5. Test",
            "6. Create Auto Scaling Group",
            "7. Test solutions",
            "   7.1. Test manual scaling solution",
            "   7.2. Test scheduled scaling solution",
            "   7.3. Test dynamic scaling solution",
            "   7.4. Read metrics of predictive scaling solution",
            "8. Cleanup Resources"
        ]
    },
    "9-Lab07": {
        "title": "Lab 07: AWS Budgets",
        "title_vi": "Lab 07: Quản lý ngân sách (Budgets)",
        "weight": 9,
        "content": [
            "1. Create Budget",
            "2. Create Cost Budget",
            "3. Create Usage Budget",
            "4. Create RI Budget",
            "5. Create Savings Plans Budget",
            "6. Clean Up Resources"
        ]
    }
}

for folder, data in labs.items():
    lab_dir = os.path.join(base_dir, folder)
    os.makedirs(lab_dir, exist_ok=True)
    
    en_content = f"""---
title: "{data['title']}"
weight: {data['weight']}
pre: "<b> {data['weight']}. </b>"
---

# {data['title']}

"""
    for line in data['content']:
        if line.startswith("   "):
            en_content += f"### {line.strip()}\nTo be updated...\n\n"
        else:
            en_content += f"## {line}\nTo be updated...\n\n"
            
    vi_content = f"""---
title: "{data['title_vi']}"
weight: {data['weight']}
pre: "<b> {data['weight']}. </b>"
---

# {data['title_vi']}

"""
    for line in data['content']:
        if line.startswith("   "):
            vi_content += f"### {line.strip()}\nĐang cập nhật...\n\n"
        else:
            vi_content += f"## {line}\nĐang cập nhật...\n\n"
            
    with open(os.path.join(lab_dir, "_index.md"), "w", encoding="utf-8") as f:
        f.write(en_content)
    with open(os.path.join(lab_dir, "_index.vi.md"), "w", encoding="utf-8") as f:
        f.write(vi_content)

print("Created Lab 05, 06, 07 structures.")
