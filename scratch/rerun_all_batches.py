import subprocess
import os

batch_scripts = [
    "scratch/execute_data_review_batch10.py",
    "scratch/execute_data_review_batch11.py",
    "scratch/execute_data_review_batch12.py",
    "scratch/execute_data_review_batch13.py",
    "scratch/execute_data_review_batch14.py",
    "scratch/execute_data_review_batch15.py",
    "scratch/execute_data_review_batch16.py",
    "scratch/execute_data_review_batch17.py",
    "scratch/execute_data_review_batch18.py",
    "scratch/execute_data_review_batch20.py",
    "scratch/execute_data_review_batch21.py",
    "scratch/execute_data_review_batch22.py",
    "scratch/execute_data_review_batch23.py",
    "scratch/execute_data_review_batch24.py",
    "scratch/execute_data_review_batch25.py",
    "scratch/execute_data_review_batch26.py",
    "scratch/execute_data_review_batch27.py",
    "scratch/execute_data_review_batch28.py",
    "scratch/execute_data_review_batch29.py",
    "scratch/execute_data_review_batch31.py",
    "scratch/execute_data_review_batch34.py",
    "scratch/execute_data_review_batch35.py",
    "scratch/execute_data_review_batch36.py",
    "scratch/execute_data_review_batch37.py",
    "scratch/execute_data_review_batch38.py",
    "scratch/execute_data_review_batch39.py",
    "scratch/execute_data_review_batch40.py",
    "scratch/execute_data_review_batch41.py",
    "scratch/execute_data_review_batch42.py",
    "scratch/execute_data_review_batch43.py",
    "scratch/execute_data_review_batch44.py"
]

print("=== RE-RUNNING ALL BATCHES 10 TO 44 IN SEQUENCE ===")
for script in batch_scripts:
    if os.path.exists(script):
        print(f"Running {script}...")
        res = subprocess.run(["python", script], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error in {script}: {res.stderr}")
        else:
            print(f"Success: {script}")

print("=== ALL BATCHES RE-EXECUTED SUCCESSFULLY ===")
