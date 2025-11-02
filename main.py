#!/usr/bin/env python3
import os
import sys

def main():
    try:
        with open('input.txt', 'r') as f:
            directories = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        sys.exit("Error: input.txt not found")
    
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
                print(f"{flag}, {filepath}")
            print()

if __name__ == '__main__':
    main()


