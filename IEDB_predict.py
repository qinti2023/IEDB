import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
from tqdm import tqdm
import argparse  # 引入argparse库

def load_jobs(json_path):
    try:
        with open(json_path, 'r') as f:
            jobs = json.load(f)
        return jobs
    except Exception as e:
        print(f"cannot load JSON file: {e}")
        sys.exit(1)

def separate_jobs(jobs):
    prediction_jobs = [job for job in jobs if job['job_type'] == 'prediction']
    aggregate_jobs = [job for job in jobs if job['job_type'] == 'aggregate']
    return prediction_jobs, aggregate_jobs

def run_job(job):
    cmd = job['shell_cmd']
    job_id = job['job_id']
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return job_id, True, result.stdout.decode()
    except subprocess.CalledProcessError as e:
        print(f"job {job_id} failed, error: {e.returncode}.\nstdout: {e.stdout.decode()}\nstderr: {e.stderr.decode()}")
        return job_id, False, e.stderr.decode()

def execute_prediction_jobs(prediction_jobs, max_workers):
    completed_jobs = set()
    failed_jobs = set()
    progress_bar = tqdm(total=len(prediction_jobs), desc="Predicting", unit="jobs")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {executor.submit(run_job, job): job for job in prediction_jobs}
        for future in as_completed(future_to_job):
            job = future_to_job[future]
            job_id, success, output = future.result()
            progress_bar.update(1)
            if success:
                completed_jobs.add(job_id)
            else:
                failed_jobs.add(job_id)
                print(f"Detect the job {job_id} failed，stop remain jobs.")
                executor.shutdown(wait=False, cancel_futures=True)
                break
    progress_bar.close()
    return completed_jobs, failed_jobs

def execute_aggregate_jobs(aggregate_jobs, completed_jobs):
    for job in aggregate_jobs:
        job_id = job['job_id']
        dependencies = job.get('depends_on_job_ids', [])
        if all(dep in completed_jobs for dep in dependencies):
            print(f"Aggregating job: {job_id}")
            try:
                result = subprocess.run(job['shell_cmd'], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Aggregating job {job_id} done")
                print(result.stdout.decode())
            except subprocess.CalledProcessError as e:
                print(f"Aggregating job {job_id} failed, error: {e.returncode}.\nstdout: {e.stdout.decode()}\nstderr: {e.stderr.decode()}")
        else:
            print(f"Not all dependencies in the aggregation task have been completed.")

def main():
    parser = argparse.ArgumentParser(description="Execute prediction and aggregation jobs from a specified JSON file.")
    parser.add_argument("json_path", type=str, help="Path to the JSON file containing job descriptions.")
    args = parser.parse_args()

    jobs = load_jobs(args.json_path)
    prediction_jobs, aggregate_jobs = separate_jobs(jobs)

    if not prediction_jobs:
        print("No predictive jobs need to be executed.")
    else:
        max_workers = os.cpu_count() - 128
        print(f"Use {max_workers} threads to execute predictive jobs in parallel.")
        completed_jobs, failed_jobs = execute_prediction_jobs(prediction_jobs, max_workers)

        if failed_jobs:
            print(f"There are {len(failed_jobs)} predictive jobs that have failed, stopping the execution of the aggregation job.")
            sys.exit(1)
        else:
            print("All predictive jobs have been successfully completed.")
            if aggregate_jobs:
                execute_aggregate_jobs(aggregate_jobs, completed_jobs)
            else:
                print("There are no aggregation jobs to execute.")

if __name__ == "__main__":
    main()

