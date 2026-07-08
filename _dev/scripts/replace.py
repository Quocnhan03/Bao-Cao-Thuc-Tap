import os
import re

for root, _, files in os.walk('content/1-Worklog'):
    for file in files:
        if file.endswith('.md'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Match title line: title: "Tu[any characters] n [number]"
            # Actually, I can just match: title: "Tu* n (\d+)" and replace with Tuần
            new_content = re.sub(r'title:\s*"Tu[^0-9]+(\d+)"', r'title: "Tuần \1"', content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {path}")
