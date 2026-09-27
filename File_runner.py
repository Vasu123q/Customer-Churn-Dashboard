import subprocess
import warnings
import sys
from pathlib import Path

warnings.filterwarnings("ignore", category=RuntimeWarning)

project_root = Path(__file__).resolve().parent

scripts = [
    project_root / "1_data_generator" / "data_gen_file_runner.py",
    project_root / "2_Data_Cleaning" / "mapper.py"
]

jupyter_books = [
    project_root / "Models" / "model_training.ipynb",
    project_root / "unsupervised" / "customer_segmentation.ipynb"

]

for script in scripts:
    print(f"Running {script.name}...")
    subprocess.run(
        [sys.executable, str(script)],
        check=True
    )

for notebook in jupyter_books:
    print(f"Running {notebook.name}...")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            str(notebook)
        ],
        check=True,
        cwd=project_root
    )

print("All scripts executed successfully.")         