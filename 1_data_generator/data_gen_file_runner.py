import subprocess
import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

project_root=Path(__file__).resolve().parent.parent

scripts = [
    project_root/'1_data_generator'/'1_name_gender.py',
    project_root/'1_data_generator'/'2_customer.py',
    project_root/'1_data_generator'/'3_services.py',
    
]

for script in scripts:
    print(f"Running {script.name}...")
    subprocess.run([sys.executable, str(script)], check=True)