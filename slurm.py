"""

Slurm job management tool

"""

import subprocess


# Class: Slurm, stores information about a list of my slurm jobs
# features: 
#          should support delayed loading of job information
#          uses a dictionary to store job information that is loaded on demand
# functions: 
#          get_jobs, get_jobs_using_dir, get_jobs_using_file, get_job_info, get_job_info_using_dir, get_job_info_using_file

class Slurm:

    def __init__(self, jobs):
        self.jobs = {}
        
        

    def get_my_jobs(self):
        p = subprocess.Popen(["squeue", "--me", '-o%.7i %.11b %.16R %.30j %.2t %.10M %.6D %.3C %.8Q %Z'], stdout=subprocess.PIPE)
        for line in p.stdout:
            line = line.decode("utf-8")
            self.jobs[line.split()[0]] = line
        return self.jobs
        
        
    def get_jobs_using_dir(self, dir):
        jobs = []
        for job in self.jobs:
            if dir in job:
                jobs.append(job)
        return jobs
    
    def submit_job(self, job_script, job_name=None):
        # if job_name is not specified, dont use the -J flag
        if job_name is None:
            p = subprocess.Popen(["sbatch", job_script], stdout=subprocess.PIPE)
        elif job_name is not None:
            p = subprocess.Popen(["sbatch", "-J", job_name, job_script], stdout=subprocess.PIPE)
        return 0