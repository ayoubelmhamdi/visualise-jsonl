#!/usr/bin/env python3
import os
import sys

RED    = '\033[31m'
YELLOW = '\033[33m'
GREEN  = '\033[32m'
RESET  = '\033[0m'

SQUARE = '■'

def generate_csv():
    try:
        with open('input.txt', 'r') as f:
            directories = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        sys.exit("Error: input.txt not found")
    
    result = []
    for directory in directories:
        if not os.path.exists(directory):
            sys.exit(f"Error: Directory {directory} does not exist")
        
        subdirs = []
        for root, dirs, files in os.walk(directory):
            if root != directory:
                subdirs.append(root)
        
        for subdir in sorted(subdirs):
            for filename in ['input.md', 'metadata.md', 'output.md']:
                filepath = os.path.join(subdir, filename)
                if os.path.isfile(filepath):
                    flag = 'A' if os.path.getsize(filepath) > 0 else 'B'
                else:
                    flag = 'C'
                result.append(f"{flag}, {filepath}")
            result.append("")
    
    return '\n'.join(result)

def foo(status):
    if status == -1:
        return f"{RED}{SQUARE}{RESET}"
    if status == 0:
        return f"{YELLOW}{SQUARE}{RESET}"
    if status == 1:
        return f"{GREEN}{SQUARE}{RESET}"
    return SQUARE

def render_csv(csv_content):
    lines = csv_content.strip().split('\n')
    
    root_groups = {}
    
    for i in range(0, len(lines), 4):
        if i + 2 >= len(lines):
            break
        
        statuses = []
        directory = None
        
        for j in range(3):
            line = lines[i + j]
            if not line.strip():
                continue
            parts = line.split(', ', 1)
            if len(parts) == 2:
                flag, filepath = parts
                if directory is None:
                    directory = os.path.dirname(filepath)
                
                statuses.append(1 if flag == 'A' else 0 if flag == 'B' else -1)
        
        if directory and len(statuses) == 3:
            try:
                with open('input.txt', 'r') as f:
                    roots = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                continue
            
            for root in roots:
                if directory.startswith(root):
                    if root not in root_groups:
                        root_groups[root] = []
                    relative = directory[len(root):].lstrip('/')
                    boxes = ''.join([foo(s) for s in statuses])
                    root_groups[root].append((relative, boxes))
                    break
    
    for root in root_groups:
        print(f"    {root}/")
        subdirs = root_groups[root]
        for idx, (relative, boxes) in enumerate(subdirs):
            prefix = "└──" if idx == len(subdirs) - 1 else "├──"
            print(f"{boxes} {prefix} /{relative}")

if __name__ == '__main__':
    csv_content = generate_csv()
    render_csv(csv_content)


