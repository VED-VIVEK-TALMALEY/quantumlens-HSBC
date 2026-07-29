# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import os

def generate_tree(startpath, output_file):
    # Added 'node_modules', 'dist', 'build', and 'package-lock.json' to exclusions
    exclude = {
        '.git', '.vscode', '__pycache__', 'env', 'venv', '.env', 
        '.pytest_cache', 'node_modules', 'dist', 'build'
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            # Exclude folders
            dirs[:] = [d for d in dirs if d not in exclude and not d.startswith('.')]
            
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            
            f.write(f'{indent}{os.path.basename(root)}/\n')
            
            subindent = '│   ' * level + '├── '
            for f_name in files:
                # Exclude hidden files and specific file patterns
                if not f_name.startswith('.') and f_name not in exclude:
                    f.write(f'{subindent}{f_name}\n')

if __name__ == "__main__":
    generate_tree('.', 'project_tree.txt')
    print("Clean tree structure (including node_modules exclusion) saved to project_tree.txt")