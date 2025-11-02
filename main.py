#!/usr/bin/env python3

# How to test this code:
# create a test directoies
# mkdir -p datasete/s5/examens/2010/{exercice,prob1} datasete/s5/serie_6/{exercice1/{1,2},ex2/{prob,qcm},exercice2/{1,3},ex1/{prob,qcm}}
# touch datasete/s5/examens/2010/exercice/{input.md,metadata.md} datasete/s5/serie_6/exercice1/2/{input.md,output.md} datasete/s5/serie_6/ex1/prob/{input.md,output.md}

# and put this lines on input.txt
# datasete/s5/examens/2010
# datasete/s5/serie_6

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
        
        subdirs = [directory]
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
                        root_groups[root] = {}
                    
                    if directory == root:
                        relative = "."
                    else:
                        relative = directory[len(root):].lstrip('/')
                    
                    boxes = ''.join([foo(s) for s in statuses])
                    root_groups[root][relative] = boxes
                    break
    
    for root in root_groups:
        tree_data = root_groups[root]
        
        if list(tree_data.keys()) == ["."]:
            print(f"{tree_data['.']} {root}/")
            continue
        
        print(f"    {root}/")
        
        paths = sorted([p for p in tree_data.keys() if p != "."])
        
        if not paths:
            continue
        
        def build_hierarchy():
            hierarchy = {}
            for path in paths:
                parts = path.split('/')
                current = hierarchy
                for part in parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
            return hierarchy
        
        def print_node(node, path_prefix="", tree_prefix="", is_last=True):
            items = sorted(node.items())
            for idx, (name, children) in enumerate(items):
                is_last_child = idx == len(items) - 1
                
                current_path = f"{path_prefix}/{name}" if path_prefix else name
                has_data = current_path in tree_data
                boxes = tree_data.get(current_path, "")
                
                connector = "└──" if is_last_child else "├──"
                
                if has_data and not children:
                    print(f"{boxes} {tree_prefix}{connector} /{name}")
                elif children:
                    print(f"    {tree_prefix}{connector} /{name}")
                    continuation = "    " if is_last_child else "│   "
                    print_node(children, current_path, tree_prefix + continuation, is_last_child)
                else:
                    print(f"{boxes} {tree_prefix}{connector} /{name}")
        
        hierarchy = build_hierarchy()
        print_node(hierarchy)

if __name__ == '__main__':
    csv_content = generate_csv()
    render_csv(csv_content)
