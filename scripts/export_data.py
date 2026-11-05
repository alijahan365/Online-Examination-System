"""
Run this script on PythonAnywhere to export your data before migrating.

Usage on PythonAnywhere bash console:
  python scripts/export_data.py
  
Then download 'data_backup.json' from Files tab and import on new server:
  python manage.py loaddata data_backup.json
"""
import os
import sys
import django
import subprocess

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')

if __name__ == '__main__':
    output_file = 'data_backup.json'
    cmd = [
        sys.executable, 'manage.py', 'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '-e', 'contenttypes',
        '-e', 'auth.Permission',
        '--indent', '2',
        '-o', output_file
    ]
    print(f"Exporting data to {output_file}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Success! Data saved to: {output_file}")
        print(f"Download this file from PythonAnywhere Files tab.")
    else:
        print(f"❌ Error: {result.stderr}")
