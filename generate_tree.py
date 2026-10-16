# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import os
import zipfile

def generate_tree_and_zip(startpath, output_file, zip_file):
    exclude = {
        '.git', '.vscode', '__pycache__', 'env', 'venv', '.env', 
        '.pytest_cache', 'node_modules', 'dist', 'build', 'package-lock.json',
        output_file, zip_file
    }
    
    with open(output_file, 'w', encoding='utf-8') as f, zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(startpath):
            dirs[:] = [d for d in dirs if d not in exclude and not d.startswith('.')]
            
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
            
            f.write(f'{indent}{os.path.basename(root)}/\n')
            
            subindent = '│   ' * level + '├── '
            for f_name in files:
                if not f_name.startswith('.') and f_name not in exclude:
                    f.write(f'{subindent}{f_name}\n')
                    
                    file_path = os.path.join(root, f_name)
                    arcname = os.path.relpath(file_path, startpath)
                    zf.write(file_path, arcname)

if __name__ == "__main__":
    generate_tree_and_zip('.', 'project_tree.txt', 'project_archive.zip')
    print("Clean tree structure saved to project_tree.txt and allowed files zipped to project_archive.zip")