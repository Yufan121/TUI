"""

Slurm job management tool

"""

import subprocess
import time

# Class: Slurm, stores information about a list of my slurm jobs
# features: 
#          should support delayed loading of job information
#          uses a dictionary to store job information that is loaded on demand
# functions: 
#          get_jobs, get_jobs_using_dir, get_jobs_using_file, get_job_info, get_job_info_using_dir, get_job_info_using_file

class Slurm:

    def __init__(self):
        self.jobs = {}
        self.current_dir = ""
        self.jobs_in_current_dir = []

    def get_my_jobs(self):
        p = subprocess.Popen(["squeue", "--me", '-o%.7i %.11b %.16R %.30j %.2t %.10M %.6D %.3C %.8Q %Z'], stdout=subprocess.PIPE)
        for line in p.stdout:
            line = line.decode("utf-8")
            self.jobs[line.split()[0]] = line
        return self.jobs
        
        
    def get_jobs_using_dir(self):
        jobs = []
        for job in self.jobs.values():
            if self.current_dir in job:
                jobs.append(job)
        # update jobs_in_current_dir; may be slow
        self.jobs_in_current_dir = jobs
        return 
    
    def update_jobs_periodically(self, interval=1, stop_event=None):
        # update jobs every one second
        while True:
            self.get_my_jobs()
            time.sleep(interval)
            if stop_event.is_set():
                break
            
    def update_jobs_by_dir_periodically(self, interval=2, stop_event=None):
        # update jobs every one second
        while True:
            self.get_jobs_using_dir()
            time.sleep(interval)
            if stop_event.is_set():
                break
        
        return jobs
    
    def submit_job(self, job_script, job_name=None):
        # if job_name is not specified, dont use the -J flag
        if job_name is None:
            p = subprocess.Popen(["sbatch", job_script], stdout=subprocess.PIPE)
        elif job_name is not None:
            p = subprocess.Popen(["sbatch", "-J", job_name, job_script], stdout=subprocess.PIPE)
        return 0
