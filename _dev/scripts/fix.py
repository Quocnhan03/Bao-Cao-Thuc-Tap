import os
import re

for root, _, files in os.walk('content/1-Worklog'):
    for file in files:
        if file.endswith('.vi.md'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Replace any title containing a number in .vi.md files with 'Tuần X'
            new_content = re.sub(r'title:\s*"[^"]*?(\d+)[^"]*?"', r'title: "Tuần \1"', content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {path}")
