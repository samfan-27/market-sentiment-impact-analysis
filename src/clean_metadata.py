import json
import sys
import os

def clean_notebook(file_path):
    """
    Removes the 'widgets' entry from the metadata of a Jupyter notebook
    to fix GitHub rendering errors.
    """
    if not os.path.exists(file_path):
        print(f'  Error: File not found at {file_path}')
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cleaned = False
        if 'metadata' in data:
            if 'widgets' in data['metadata']:
                del data['metadata']['widgets']
                cleaned = True
                print(f'  Removed metadata.widgets from {os.path.basename(file_path)}')
        
        if not cleaned:
            print(f'  {os.path.basename(file_path)} was already clean.')
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1)
        
        print(f'  Successfully saved cleaned notebook.')

    except Exception as e:
        print(f'  Error processing {file_path}: {str(e)}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python src/clean_metadata.py <path_to_notebook.ipynb>')
    else:
        for path in sys.argv[1:]:
            clean_notebook(path)
            